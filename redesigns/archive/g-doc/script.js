// Keyboard shortcuts (H home, C case study, A about, S sources) and the sources toggle.
(() => {
  const btn = document.getElementById('sources');
  const set = (on) => {
    document.body.classList.toggle('sources', on);
    if (btn) btn.setAttribute('aria-pressed', on);
    try { localStorage.setItem('g-sources', on ? '1' : '0'); } catch (e) {}
  };
  if (btn) {
    let on = false; try { on = localStorage.getItem('g-sources') === '1'; } catch (e) {}
    set(on);
    btn.addEventListener('click', () => set(!document.body.classList.contains('sources')));
  }
  addEventListener('keydown', (e) => {
    if (e.metaKey || e.ctrlKey || e.altKey || e.target.closest('input, textarea, [contenteditable]')) return;
    const k = e.key.toLowerCase();
    if (k === 'h') location.href = 'index.html';
    else if (k === 'c') location.href = 'case-pmi.html';
    else if (k === 'a') location.href = 'about.html';
    else if (k === 's' && btn) set(!document.body.classList.contains('sources'));
  });
})();
