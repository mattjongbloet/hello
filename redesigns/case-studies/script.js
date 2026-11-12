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
})();

// Contents menu: highlight the section currently being read (works from the top of the page and on anchor jumps).
(() => {
  const links = [...document.querySelectorAll('.toc a')];
  const secs = links.map((a) => document.getElementById(a.getAttribute('href').slice(1))).filter(Boolean);
  if (!secs.length) return;
  const set = () => {
    let cur = secs[0];
    for (const s of secs) if (s.getBoundingClientRect().top <= 180) cur = s;
    links.forEach((l) => l.classList.toggle('on', l.getAttribute('href') === '#' + cur.id));
  };
  addEventListener('scroll', set, { passive: true }); addEventListener('resize', set); set();
})();
