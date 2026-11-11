// Ring field: one ring per step; the step nearest the middle of the screen lights its ring and sets the big label.
(() => {
  const steps = [...document.querySelectorAll('.step[data-big]')];
  const svg = document.querySelector('.field svg');
  const big = document.querySelector('.field .exp b'), unit = document.querySelector('.field .exp span');
  if (!svg || !steps.length) return;
  const NS = 'http://www.w3.org/2000/svg', n = steps.length;
  const core = document.createElementNS(NS, 'circle'); core.setAttribute('class', 'core'); core.setAttribute('cx', 0); core.setAttribute('cy', 0); core.setAttribute('r', 6);
  const rings = steps.map((_, i) => {
    const c = document.createElementNS(NS, 'circle');
    c.setAttribute('cx', 0); c.setAttribute('cy', 0); c.setAttribute('r', 14 + (i + 1) * (86 / n));
    svg.appendChild(c); return c;
  });
  svg.appendChild(core);
  // Phones: each step's mini scale shows how far along the magnitude it is
  steps.forEach((s, i) => s.style.setProperty('--p', Math.round(((i + 1) / n) * 100) + '%'));
  let last = -1;
  const pick = () => {
    const mid = innerHeight / 2; let best = 0, bd = Infinity;
    steps.forEach((s, i) => { const r = s.getBoundingClientRect(); const d = Math.abs((r.top + r.bottom) / 2 - mid); if (d < bd) { bd = d; best = i; } });
    if (best === last) return; last = best;
    rings.forEach((c, i) => { c.classList.toggle('lit', i < best); c.classList.toggle('on', i === best); });
    big.innerHTML = steps[best].dataset.big; unit.textContent = steps[best].dataset.unit || '';
  };
  addEventListener('scroll', pick, { passive: true }); addEventListener('resize', pick); pick();
})();
