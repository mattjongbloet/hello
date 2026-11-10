// Deck controls: arrows / Space / PageUp-Down / Home / End move between slides, N toggles speaker notes.
(() => {
  const slides = [...document.querySelectorAll('.slide')];
  const count = document.querySelector('.count'), bar = document.querySelector('.progress');
  const notesBtn = document.querySelector('.notes-btn');
  let cur = 0;
  const pad = (n) => String(n).padStart(2, '0');
  const current = () => {
    const mid = innerHeight * 0.4; let best = 0;
    slides.forEach((s, i) => { if (s.getBoundingClientRect().top <= mid) best = i; });
    return best;
  };
  const update = () => {
    cur = current();
    if (count) count.textContent = `${pad(cur + 1)} / ${pad(slides.length)}`;
    if (bar) bar.style.width = ((cur + 1) / slides.length * 100) + '%';
  };
  const go = (i) => { i = Math.max(0, Math.min(slides.length - 1, i)); slides[i].scrollIntoView({ block: 'start' }); };
  document.querySelector('.prev')?.addEventListener('click', () => go(current() - 1));
  document.querySelector('.next')?.addEventListener('click', () => go(current() + 1));
  const toggleNotes = () => {
    const on = document.body.classList.toggle('show-notes');
    notesBtn?.setAttribute('aria-pressed', on);
  };
  notesBtn?.addEventListener('click', toggleNotes);
  addEventListener('keydown', (e) => {
    if (e.metaKey || e.ctrlKey || e.altKey || e.target.closest('input, textarea')) return;
    const k = e.key;
    if (['ArrowRight', 'ArrowDown', 'PageDown'].includes(k) || (k === ' ' && !e.shiftKey && !e.target.closest('button, a'))) { e.preventDefault(); go(current() + 1); }
    else if (['ArrowLeft', 'ArrowUp', 'PageUp'].includes(k) || (k === ' ' && e.shiftKey)) { e.preventDefault(); go(current() - 1); }
    else if (k === 'Home') { e.preventDefault(); go(0); }
    else if (k === 'End') { e.preventDefault(); go(slides.length - 1); }
    else if (k.toLowerCase() === 'n') toggleNotes();
  });
  addEventListener('scroll', update, { passive: true }); addEventListener('resize', update); update();
})();
