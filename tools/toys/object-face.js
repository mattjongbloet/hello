// 2 · Object face. Hover states are CSS; this adds what each piece opens, a little parallax, and the record's music.
(() => {
  const root = document.querySelector('.toy-face'); if (!root) return;
  const face = root.querySelector('[data-face]'), pop = root.querySelector('.face-pop');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (matchMedia('(hover: none)').matches) pop.querySelector('.toy-hint').textContent = 'Tap the face';
  const CARDS = {
    music: ['Music', 'The needle’s down. This loop is made in your browser; your playlist goes here.'],
    cycle: ['Cycling', 'Amsterdam by bike. A favourite route goes here.'],
    hike: ['Hiking', 'On a ridge in Nepal.', '../assets/nepal.jpeg'],
    pencil: ['The pencil', 'My logo: a pencil that spells MJ. <a href="about.html">More about me →</a>'],
    choc: ['Chocolate &amp; coffee', 'The fuel. A favourite goes here.'],
  };
  const show = (k) => {
    const [title, text, img] = CARDS[k];
    pop.innerHTML = `<div class="face-card">${img ? `<img src="${img}" alt="">` : ''}<div><b>${title}</b><span>${text}</span></div></div>`;
    face.className = 'toy-stage face on-' + k;
  };

  // A small lo-fi loop, made with Web Audio so there is nothing to download. Starts only on click.
  let ac = null, stop = null;
  const play = () => {
    ac = ac || new (window.AudioContext || window.webkitAudioContext)();
    const master = ac.createGain(), lp = ac.createBiquadFilter();
    master.gain.setValueAtTime(.0001, ac.currentTime); master.gain.exponentialRampToValueAtTime(.16, ac.currentTime + .4);
    lp.type = 'lowpass'; lp.frequency.value = 1300; lp.connect(master); master.connect(ac.destination);
    const chords = [[220, 261.63, 329.63], [174.61, 220, 261.63], [196, 246.94, 293.66], [164.81, 207.65, 246.94]];
    let step = 0; const beat = 1.5;
    const tick = () => {
      const now = ac.currentTime;
      chords[step++ % 4].forEach((f, i) => {
        const o = ac.createOscillator(), g = ac.createGain(); o.type = 'triangle'; o.frequency.value = f;
        g.gain.setValueAtTime(.0001, now + i * .09); g.gain.exponentialRampToValueAtTime(.2, now + i * .09 + .06); g.gain.exponentialRampToValueAtTime(.0001, now + beat * .95);
        o.connect(g).connect(lp); o.start(now + i * .09); o.stop(now + beat);
      });
    };
    tick(); const timer = setInterval(tick, beat * 1000);
    stop = () => { clearInterval(timer); master.gain.exponentialRampToValueAtTime(.0001, ac.currentTime + .3); setTimeout(() => master.disconnect(), 400); stop = null; };
  };

  root.querySelectorAll('.fo').forEach((b) => b.addEventListener('click', () => {
    const k = b.dataset.k; show(k);
    if (k === 'music') { const on = !stop; if (on) play(); else stop(); b.setAttribute('aria-pressed', String(on)); }
  }));

  if (!reduce) addEventListener('pointermove', (e) => {
    if (e.pointerType === 'touch') return;
    const r = face.getBoundingClientRect();
    const nx = Math.max(-1, Math.min(1, (e.clientX - (r.left + r.width / 2)) / innerWidth * 2)), ny = Math.max(-1, Math.min(1, (e.clientY - (r.top + r.height / 2)) / innerHeight * 2));
    face.style.transform = `translate(${(nx * 10).toFixed(1)}px, ${(ny * 8).toFixed(1)}px) rotate(${(nx * 2).toFixed(2)}deg)`;
  }, { passive: true });
})();
