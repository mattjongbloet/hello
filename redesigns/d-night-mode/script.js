// Amsterdam clock, count-up numbers, and a reading-progress bar styled like the PMI removal goal.
(() => {
  const clock = document.querySelector('[data-clock]');
  if (clock) {
    const fmt = new Intl.DateTimeFormat('en-GB', { hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Amsterdam' });
    const tick = () => { clock.textContent = fmt.format(new Date()); };
    tick(); setInterval(tick, 20000);
  }

  const motionOK = matchMedia('(prefers-reduced-motion: no-preference)').matches;
  if (motionOK && 'IntersectionObserver' in window) {
    // Numbers render final values first; below-the-fold ones count up once when they scroll in.
    const els = [...document.querySelectorAll('[data-count]')].filter((el) => el.getBoundingClientRect().top > innerHeight);
    const io = new IntersectionObserver((es) => es.forEach((e) => {
      if (!e.isIntersecting) return;
      io.unobserve(e.target);
      const el = e.target, end = parseFloat(el.dataset.count), dec = (el.dataset.count.split('.')[1] || '').length;
      const pre = el.dataset.pre || '', suf = el.dataset.suf || '', t0 = performance.now();
      const step = (t) => {
        const k = Math.min(1, (t - t0) / 1100), v = end * (1 - Math.pow(1 - k, 3));
        el.textContent = pre + v.toFixed(dec) + suf;
        if (k < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    }), { threshold: 0.6 });
    els.forEach((el) => io.observe(el));
  }

  const fill = document.querySelector('.readbar .fill');
  if (fill) {
    const upd = () => {
      const max = document.documentElement.scrollHeight - innerHeight;
      const p = Math.round(Math.max(0, Math.min(1, scrollY / (max || 1))) * 100);
      fill.style.width = p + '%'; fill.textContent = p + '%';
    };
    addEventListener('scroll', upd, { passive: true }); upd();
  }
})();
