// Amsterdam clock in the masthead, and a cursor-following preview on the work index.
(() => {
  const clock = document.querySelector('[data-clock]');
  if (clock) {
    const fmt = new Intl.DateTimeFormat('en-GB', { hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Amsterdam' });
    const tick = () => { clock.textContent = fmt.format(new Date()) + ' in Amsterdam'; };
    tick(); setInterval(tick, 30000);
  }
  const peek = document.querySelector('.peek');
  if (!peek || !matchMedia('(hover: hover) and (min-width: 961px)').matches) return;
  const img = peek.querySelector('img');
  document.querySelectorAll('.index a[data-img]').forEach((a) => {
    a.addEventListener('mouseenter', () => { img.src = a.dataset.img; peek.classList.add('on'); });
    a.addEventListener('mouseleave', () => peek.classList.remove('on'));
    a.addEventListener('mousemove', (e) => { peek.style.left = (e.clientX + 200) + 'px'; peek.style.top = e.clientY + 'px'; });
  });
})();
