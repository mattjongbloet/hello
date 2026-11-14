// Header border on scroll, gentle reveal, active contents link.
(() => {
  const top = document.querySelector('.top');
  const onScroll = () => top && top.classList.toggle('scrolled', scrollY > 8);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  const motionOK = matchMedia('(prefers-reduced-motion: no-preference)').matches;
  if (motionOK && 'IntersectionObserver' in window) {
    const els = [...document.querySelectorAll('.reveal')].filter((el) => el.getBoundingClientRect().top > innerHeight);
    els.forEach((el) => el.classList.add('pre'));
    const io = new IntersectionObserver((entries) => entries.forEach((e) => {
      if (e.isIntersecting) { e.target.classList.remove('pre'); io.unobserve(e.target); }
    }), { rootMargin: '0px 0px -8% 0px' });
    els.forEach((el) => io.observe(el));
  }

  const links = [...document.querySelectorAll('.toc a')];
  if (links.length) {
    const map = new Map(links.map((a) => [a.getAttribute('href').slice(1), a]));
    const io2 = new IntersectionObserver((entries) => entries.forEach((e) => {
      if (e.isIntersecting) { links.forEach((l) => l.classList.remove('on')); map.get(e.target.id)?.classList.add('on'); }
    }), { rootMargin: '-30% 0px -60% 0px' });
    map.forEach((_, id) => { const s = document.getElementById(id); if (s) io2.observe(s); });
  }
})();

// Light / dark theme: remembers the choice, swaps mockups that have a dark version.
(() => {
  const root = document.documentElement; let theme = root.dataset.theme || 'light';
  const apply = () => {
    root.dataset.theme = theme;
    document.querySelectorAll('.theme-toggle').forEach((b) => { b.setAttribute('aria-pressed', String(theme === 'dark')); b.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'); });
    document.querySelectorAll('img[data-dark]').forEach((img) => { if (!img.dataset.light) img.dataset.light = img.getAttribute('src'); const src = theme === 'dark' ? img.dataset.dark : img.dataset.light; if (img.getAttribute('src') !== src) img.setAttribute('src', src); });
  };
  apply();
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.theme-toggle')) return;
    theme = theme === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem('mj-theme', theme); } catch (err) { /* private mode: the choice just won't persist */ }
    apply();
  });
})();
// Phone menu: the hamburger next to the theme toggle opens Work / About / Resume as a panel under the header.
(() => {
  const top = document.querySelector('.top'), btn = top && top.querySelector('.menu-toggle'); if (!btn) return;
  const set = (open) => { top.classList.toggle('menu-open', open); btn.setAttribute('aria-expanded', String(open)); btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu'); };
  btn.addEventListener('click', () => set(!top.classList.contains('menu-open')));
  top.querySelectorAll('.nav a').forEach((a) => a.addEventListener('click', () => set(false)));
  document.addEventListener('click', (e) => { if (!e.target.closest('.top')) set(false); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && top.classList.contains('menu-open')) { set(false); btn.focus(); } });
  matchMedia('(min-width: 561px)').addEventListener('change', (e) => { if (e.matches) set(false); });
})();
