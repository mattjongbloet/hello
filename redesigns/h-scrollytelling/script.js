// Swap the pinned scene (and the progress dot) to match the step nearest the middle of the screen.
(() => {
  const steps = [...document.querySelectorAll('.step[data-scene]')];
  const scenes = new Map([...document.querySelectorAll('.scene')].map((s) => [s.dataset.scene, s]));
  const dots = [...document.querySelectorAll('.progress i')];
  const show = (i) => {
    const id = steps[i].dataset.scene;
    scenes.forEach((s, k) => s.classList.toggle('on', k === id));
    dots.forEach((d, j) => d.classList.toggle('on', j === i));
  };
  const pick = () => {
    const mid = innerHeight / 2; let best = 0, bd = Infinity;
    steps.forEach((s, i) => { const r = s.getBoundingClientRect(); const d = Math.abs((r.top + r.bottom) / 2 - mid); if (d < bd) { bd = d; best = i; } });
    show(best);
  };
  addEventListener('scroll', pick, { passive: true }); addEventListener('resize', pick); pick();
})();
