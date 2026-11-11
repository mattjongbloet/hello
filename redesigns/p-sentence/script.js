// Keycap shortcuts (H W A C), gentle reveal, draggable stickers, active contents link.
(() => {
  const here = location.pathname.split('/').pop() || 'index.html';
  const onHome = here === 'index.html';
  const behavior = matchMedia('(prefers-reduced-motion: no-preference)').matches ? 'smooth' : 'auto';
  const go = {
    h: () => (onHome ? scrollTo({ top: 0, behavior }) : (location.href = 'index.html')),
    w: () => (onHome ? document.getElementById('work')?.scrollIntoView({ behavior }) : (location.href = 'index.html#work')),
    a: () => (here === 'about.html' ? scrollTo({ top: 0, behavior }) : (location.href = 'about.html')),
    c: () => document.getElementById('contact')?.scrollIntoView({ behavior }),
  };
  addEventListener('keydown', (e) => {
    if (e.metaKey || e.ctrlKey || e.altKey || e.shiftKey || e.repeat) return;
    const t = e.target;
    if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;
    const k = e.key.toLowerCase();
    if (!go[k]) return;
    e.preventDefault();
    document.querySelectorAll(`.key[data-k="${k}"]`).forEach((el) => {
      el.classList.add('pressed');
      setTimeout(() => el.classList.remove('pressed'), 140);
    });
    go[k]();
  });

  const motionOK = matchMedia('(prefers-reduced-motion: no-preference)').matches;
  if (motionOK && 'IntersectionObserver' in window) {
    const els = [...document.querySelectorAll('.reveal')].filter((el) => el.getBoundingClientRect().top > innerHeight);
    els.forEach((el) => el.classList.add('pre'));
    const io = new IntersectionObserver((entries) => entries.forEach((e) => {
      if (e.isIntersecting) { e.target.classList.remove('pre'); io.unobserve(e.target); }
    }), { rootMargin: '0px 0px -8% 0px' });
    els.forEach((el) => io.observe(el));
    // Fallback for fast jumps (anchor links, screenshot tools): reveal anything at or above the viewport.
    addEventListener('scroll', () => {
      document.querySelectorAll('.pre').forEach((el) => { if (el.getBoundingClientRect().top < innerHeight) { el.classList.remove('pre'); io.unobserve(el); } });
    }, { passive: true });
  }

  // Stickers: drag them around. Position is an offset added on top of their own rotation.
  document.querySelectorAll('.sticker').forEach((el) => {
    const base = getComputedStyle(el).transform;
    const rot = base && base !== 'none' ? base : '';
    let x = 0, y = 0, sx = 0, sy = 0, id = null;
    el.addEventListener('pointerdown', (e) => {
      id = e.pointerId; sx = e.clientX - x; sy = e.clientY - y;
      el.setPointerCapture(id); el.style.zIndex = 5;
    });
    el.addEventListener('pointermove', (e) => {
      if (e.pointerId !== id) return;
      x = e.clientX - sx; y = e.clientY - sy;
      el.style.transform = `translate(${x}px, ${y}px) ${rot}`;
    });
    const end = (e) => { if (e.pointerId === id) id = null; };
    el.addEventListener('pointerup', end);
    el.addEventListener('pointercancel', end);
  });

  const links = [...document.querySelectorAll('.toc a')];
  if (links.length) {
    const map = new Map(links.map((a) => [a.getAttribute('href').slice(1), a]));
    const io2 = new IntersectionObserver((entries) => entries.forEach((e) => {
      if (e.isIntersecting) { links.forEach((l) => l.classList.remove('on')); map.get(e.target.id)?.classList.add('on'); }
    }), { rootMargin: '-30% 0px -60% 0px' });
    map.forEach((_, id) => { const s = document.getElementById(id); if (s) io2.observe(s); });
  }
})();
