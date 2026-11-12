// 4 · Face follows the cursor. Each layer moves by its own depth, the pupils a little more; the head tilts.
// It blinks on its own, looks around when the cursor is idle, and says hello on click. Reduced motion: it stays still.
(() => {
  const root = document.querySelector('.toy-follow'); if (!root) return;
  const btn = root.querySelector('.ff'), layers = [...root.querySelectorAll('.ff-l')], pupils = [...root.querySelectorAll('.ff-pupil')], head = root.querySelector('.ff-head');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let tx = 0, ty = 0, x = 0, y = 0, last = -1e9, visible = true, raf = null;
  if (matchMedia('(hover: none)').matches) root.querySelector('.toy-hint').textContent = 'Tap to say hello';

  const frame = (time) => {
    raf = null; if (!visible) return;
    if (time - last > 2800) { tx = Math.sin(time * .0007) * .55; ty = Math.cos(time * .0011) * .3; }   // idle: look around
    x += (tx - x) * .09; y += (ty - y) * .09;
    for (const l of layers) { const d = +l.dataset.d; l.setAttribute('transform', `translate(${(x * d).toFixed(2)} ${(y * d * .8).toFixed(2)})`); }
    for (const p of pupils) p.setAttribute('transform', `translate(${(x * 6).toFixed(2)} ${(y * 4.5).toFixed(2)})`);
    head.style.transform = `rotate(${(x * 5).toFixed(2)}deg)`;
    raf = requestAnimationFrame(frame);
  };
  const kick = () => { if (!raf && visible && !reduce) raf = requestAnimationFrame(frame); };

  addEventListener('pointermove', (e) => {
    const r = btn.getBoundingClientRect();
    tx = Math.max(-1, Math.min(1, (e.clientX - (r.left + r.width / 2)) / (innerWidth * .45)));
    ty = Math.max(-1, Math.min(1, (e.clientY - (r.top + r.height / 2)) / (innerHeight * .45)));
    last = performance.now();
  }, { passive: true });
  btn.addEventListener('click', () => { btn.classList.add('hi'); clearTimeout(btn._t); btn._t = setTimeout(() => btn.classList.remove('hi'), 1600); });
  if (!reduce) (function blink() { setTimeout(() => { btn.classList.add('blink'); setTimeout(() => btn.classList.remove('blink'), 130); blink(); }, 2600 + Math.random() * 3200); })();
  new IntersectionObserver(([en]) => { visible = en.isIntersecting; kick(); }).observe(btn);
  kick();
})();
