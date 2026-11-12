// 1 · Untangle. One closed line: a tangle of harmonics far from the cursor, a clean circle up close.
// Idle: it slowly demonstrates itself. Touch: tap to toggle. Reduced motion: it rests as the circle.
(() => {
  const root = document.querySelector('.toy-untangle'); if (!root) return;
  const cv = root.querySelector('canvas'), ctx = cv.getContext('2d'), hint = root.querySelector('.toy-hint');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const css = getComputedStyle(document.documentElement);
  const INK = css.getPropertyValue('--ink').trim() || '#15171a';
  const SIGNAL = css.getPropertyValue('--signal').trim() || '#ff5a1f';
  const N = 520, TAU = Math.PI * 2;
  const K = [[1, .26, 0], [2, .21, 1.3], [3, .22, 2.1], [5, .19, .7], [7, .15, 4.2], [11, .11, 5.5], [16, .05, 2.9]];
  let W = 0, H = 0, dpr = 1, t = reduce ? 1 : 0, goal = t, visible = true, raf = null;
  let px = null, py = null, lastPointer = -1e9, tapGoal = null, tapAt = -1e9;

  const resize = () => {
    const r = cv.getBoundingClientRect(); dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = r.width; H = r.height; cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
  };
  const tangled = (s, time) => {
    let x = 0, y = 0;
    for (const [f, a, p] of K) { x += a * Math.sin(f * s + p + time * .00016 * f); y += a * Math.cos(f * s * 1.0 + p * 1.9 - time * .00013 * f); }
    return [x, y];
  };
  const ease = (v) => v * v * (3 - 2 * v);

  const draw = (time) => {
    const e = ease(Math.max(0, Math.min(1, t))), R = Math.min(W, H) * .46, cx = W / 2, cy = H / 2;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, W, H);
    const pts = [];
    for (let i = 0; i < N; i++) {
      const s = (i / N) * TAU, [tx, ty] = tangled(s, time);
      const sx = .62 * Math.cos(s - Math.PI / 2), sy = .62 * Math.sin(s - Math.PI / 2);
      pts.push([cx + R * ((1 - e) * tx + e * sx), cy + R * ((1 - e) * ty + e * sy)]);
    }
    ctx.beginPath();
    for (let i = 0; i <= N; i++) {
      const a = pts[i % N], b = pts[(i + 1) % N], mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2;
      if (i === 0) ctx.moveTo(mx, my); else ctx.quadraticCurveTo(a[0], a[1], mx, my);
    }
    ctx.closePath(); ctx.lineJoin = 'round'; ctx.lineCap = 'round';
    ctx.lineWidth = 2 + 2.5 * e; ctx.strokeStyle = INK; ctx.stroke();
    ctx.beginPath(); ctx.arc(pts[0][0], pts[0][1], 6 + 3 * e, 0, TAU); ctx.fillStyle = SIGNAL; ctx.fill();
    const label = e > .93 ? 'Simple' : e < .12 ? 'Complex' : 'Simplifying';
    if (hint.textContent !== label) hint.textContent = label;
  };

  const frame = (time) => {
    raf = null; if (!visible) return;
    if (time - tapAt < 6000 && tapGoal !== null) goal = tapGoal;                 // touch: tap toggles
    else if (time - lastPointer < 3500 && px !== null) {                          // mouse: closer = simpler
      const r = cv.getBoundingClientRect(), d = Math.hypot(px - (r.left + r.width / 2), py - (r.top + r.height / 2));
      goal = 1 - Math.max(0, Math.min(1, (d - r.width * .42) / (r.width * 1.5)));
    } else goal = .5 - .5 * Math.cos(time * .00055);                              // idle: show what it does
    t += (goal - t) * .07;
    draw(time); raf = requestAnimationFrame(frame);
  };
  const kick = () => { if (!raf && visible && !reduce) raf = requestAnimationFrame(frame); };

  addEventListener('pointermove', (e) => { if (e.pointerType === 'touch') return; px = e.clientX; py = e.clientY; lastPointer = performance.now(); }, { passive: true });
  cv.addEventListener('pointerdown', (e) => { if (e.pointerType === 'mouse') return; tapGoal = t > .5 ? 0 : 1; tapAt = performance.now(); });
  new IntersectionObserver(([en]) => { visible = en.isIntersecting; kick(); }).observe(cv);
  addEventListener('resize', () => { resize(); if (reduce) draw(0); });
  resize(); if (reduce) draw(0); else kick();
})();
