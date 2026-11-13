/* Liquid jungle loops, generated in the browser with Web Audio (no audio files).
   window.Jungle = { presets, build(ctx, dest, preset) -> { schedule(bar, time), barLength, out }, play(ctx, dest, index) -> stop() }.
   Each preset: tempo, a four-chord progression (two bars per chord), a break, a bass line, chords (pad / keys / strings) and a lead.
   Used by the sound lab (tools/build-sound-lab.py); the pick goes onto the record in the 3D face. */
(() => {
  const mtof = (m) => 440 * Math.pow(2, (m - 69) / 12);
  // chord shapes (semitones above the root)
  const m7 = [0, 3, 7, 10], m9 = [0, 3, 7, 10, 14], M7 = [0, 4, 7, 11], M9 = [0, 4, 7, 11, 14], six = [0, 4, 7, 9], sus = [0, 5, 7, 10], maj = [0, 4, 7, 12];
  // breaks: two bars each. x = hit, g = ghost note
  const TWO = { k: ['x.........x.....', 'x.........x..x..'], s: ['....x.......x...', '....x.......x..g'] };
  const AMEN = { k: ['x.x.......xx....', 'x.x.......x.....'], s: ['....x..g.g..x..g', '....x..g.g....x.'] };
  const ROLL = { k: ['x.....x...x.....', 'x.....x..x......'], s: ['....x..g....x...', '....x..g..g.x.g.'] };
  const SOFT = { k: ['x.........x.....', 'x......x..x.....'], s: ['....x.......x...', '....x.......x...'] };
  const CHOP = { k: ['x..x......x.....', 'x.x....x..x.....'], s: ['....x.g..g..x...', '....x....g..x.gg'] };
  // hats: x = closed, - = soft, o = open
  const H8 = ['x.x.x.x.x.x.x.x.'], H16 = ['x-x-x-x-x-x-x-x-'], HOFF = ['..x...x...x...o.'], HRIDE = ['x..-x.-.x..-x.o.'], HSHUF = ['x-.-x-.-x-.-x-o-'];
  // bass lines over two bars: [step 0-31, length in steps, semitones from the root]
  const LONG = [[0, 13, 0], [14, 2, 0], [16, 10, 0], [28, 4, 7]], PULSE = [[0, 6, 0], [6, 4, 0], [10, 6, 0], [16, 6, 0], [22, 4, -2], [26, 6, 0]],
    ROLLB = [[0, 3, 0], [3, 3, 0], [6, 4, 0], [10, 6, 0], [16, 3, 0], [19, 3, 0], [22, 4, 7], [26, 6, 5]], DEEP = [[0, 16, 0], [16, 12, 0], [28, 4, -5]], WALK = [[0, 8, 0], [8, 6, 7], [14, 2, 10], [16, 8, 0], [24, 4, 5], [28, 4, 7]];
  const presets = [
    { name: 'Morning Mist', bpm: 170, key: 'F major', note: 'Two-step break, warm pad, a few soft bells.', brk: TWO, hat: H8, swing: .06, chords: [[53, M9], [52, m7], [50, m9], [48, M7]], bass: LONG, pad: 'pad', cut: 1000,
      lead: 'bell', mel: [[4, 2, 12, 2], [10, 3, 12, 2], [20, 4, 12, 2], [26, 2, 12, 4]], rev: .34, crackle: .5 },
    { name: 'Canal Drift', bpm: 168, key: 'A minor', note: 'A light amen break under electric piano chords.', brk: AMEN, hat: H16, swing: .05, chords: [[57, m9], [53, M7], [48, M9], [55, six]], bass: PULSE, pad: 'keys', keys: [0, 6, 14, 22], cut: 1400,
      lead: 'pluck', mel: [[2, 3, 12, 2], [8, 2, 12, 2], [12, 4, 12, 2], [18, 3, 12, 2], [24, 1, 24, 4]], rev: .3, crackle: .4 },
    { name: 'Night Bus', bpm: 172, key: 'D minor', note: 'Rolling break and a deep sub, slow dark pad.', brk: ROLL, hat: HOFF, swing: .04, chords: [[50, m9], [46, M7], [43, m7], [45, sus]], bass: ROLLB, pad: 'pad', cut: 760,
      lead: 'flute', mel: [[0, 2, 12, 6], [8, 3, 12, 4], [16, 4, 12, 8], [28, 3, 12, 4]], rev: .4, crackle: .35 },
    { name: 'Tan Wall', bpm: 174, key: 'E minor', note: 'The busiest one: full amen, pads and a plucked arpeggio.', brk: AMEN, hat: HSHUF, swing: .05, chords: [[52, m7], [48, M7], [45, m9], [47, m7]], bass: PULSE, pad: 'pad', cut: 1200,
      lead: 'pluck', mel: [[0, 0, 12, 2], [3, 1, 12, 2], [6, 2, 12, 2], [9, 3, 12, 2], [12, 2, 12, 2], [16, 0, 12, 2], [19, 1, 12, 2], [22, 2, 12, 2], [25, 3, 12, 2], [28, 4, 12, 2]], rev: .3, crackle: .3 },
    { name: 'Stroop', bpm: 164, key: 'C major', note: 'The calmest: a sparse break, warm keys, lots of space.', brk: SOFT, hat: HRIDE, swing: .07, chords: [[48, M9], [45, m7], [53, M7], [55, six]], bass: DEEP, pad: 'keys', keys: [0, 10, 20], cut: 1100,
      lead: 'bell', mel: [[6, 4, 12, 2], [14, 2, 12, 2], [22, 3, 12, 6]], rev: .42, crackle: .6 },
    { name: 'Dune Walk', bpm: 170, key: 'F♯ minor', note: 'Shuffling hats, a walking bass and a soft flute line.', brk: TWO, hat: HSHUF, swing: .06, chords: [[54, m7], [50, M7], [47, m7], [52, maj]], bass: WALK, pad: 'strings', cut: 1500,
      lead: 'flute', mel: [[0, 3, 12, 4], [6, 2, 12, 2], [10, 1, 12, 6], [18, 2, 12, 4], [24, 4, 12, 6]], rev: .38, crackle: .3 },
    { name: 'Rain on Glass', bpm: 168, key: 'G minor', note: 'Rain in the background, bells over minor ninths.', brk: ROLL, hat: H8, swing: .05, chords: [[55, m9], [51, M7], [48, m7], [50, sus]], bass: LONG, pad: 'pad', cut: 900,
      lead: 'bell', mel: [[2, 4, 12, 2], [5, 3, 12, 2], [8, 2, 12, 4], [18, 3, 12, 2], [21, 4, 12, 2], [24, 1, 24, 6]], rev: .44, rain: .5, crackle: .2 },
    { name: 'First Light', bpm: 172, key: 'D major', note: 'The brightest: major sevenths, strings and a rising arpeggio.', brk: CHOP, hat: H16, swing: .04, chords: [[50, M7], [47, m7], [43, M9], [45, six]], bass: PULSE, pad: 'strings', cut: 1900,
      lead: 'pluck', mel: [[0, 0, 12, 2], [2, 1, 12, 2], [4, 2, 12, 2], [6, 3, 12, 2], [8, 0, 24, 4], [16, 3, 12, 2], [18, 2, 12, 2], [20, 1, 12, 2], [24, 2, 12, 6]], rev: .32, crackle: .3 },
    { name: 'Low Tide', bpm: 160, key: 'B♭ minor', note: 'The slowest and deepest: long sub notes, very slow pad.', brk: SOFT, hat: HOFF, swing: .06, chords: [[46, m9], [42, M7], [39, m7], [41, sus]], bass: DEEP, pad: 'pad', cut: 640,
      lead: 'flute', mel: [[4, 2, 12, 10], [20, 3, 12, 10]], rev: .46, crackle: .5 },
    { name: 'Roller', bpm: 174, key: 'A minor', note: 'Chopped break that keeps rolling, keys stabs, a busier bass.', brk: CHOP, hat: HSHUF, swing: .04, chords: [[57, m7], [52, m7], [53, M7], [55, maj]], bass: ROLLB, pad: 'keys', keys: [0, 3, 10, 16, 19, 26], cut: 1300,
      lead: 'bell', mel: [[7, 3, 12, 2], [15, 2, 12, 2], [23, 4, 12, 2], [30, 3, 12, 2]], rev: .3, crackle: .3 },
  ];
  const kits = new WeakMap();
  const kit = (ctx) => { let k = kits.get(ctx); if (k) return k; const sr = ctx.sampleRate;
    const noise = ctx.createBuffer(1, sr * 2, sr), nd = noise.getChannelData(0); for (let i = 0; i < nd.length; i++) nd[i] = Math.random() * 2 - 1;
    const ir = ctx.createBuffer(2, Math.floor(sr * 2.6), sr); for (let c = 0; c < 2; c++) { const d = ir.getChannelData(c); for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / d.length, 2.8); }
    const crackle = ctx.createBuffer(1, sr * 4, sr), cd = crackle.getChannelData(0); for (let i = 0; i < cd.length; i++) cd[i] = (Math.random() * 2 - 1) * .012 + (Math.random() < .0005 ? (Math.random() * 2 - 1) * .8 : 0);
    k = { noise, ir, crackle }; kits.set(ctx, k); return k; };
  function build(ctx, dest, P) {
    const K = kit(ctx), step = 60 / P.bpm / 4, out = ctx.createGain(), comp = ctx.createDynamicsCompressor(); out.gain.value = .62; comp.threshold.value = -16; comp.ratio.value = 3; comp.attack.value = .004; comp.release.value = .18; comp.connect(out); out.connect(dest);
    const drums = ctx.createGain(), music = ctx.createGain(), rev = ctx.createConvolver(), revG = ctx.createGain(), dly = ctx.createDelay(1), fb = ctx.createGain(), dlp = ctx.createBiquadFilter();
    drums.gain.value = .9; music.gain.value = 1; rev.buffer = K.ir; revG.gain.value = P.rev; drums.connect(comp); music.connect(comp); rev.connect(revG).connect(comp);
    dly.delayTime.value = step * 3; fb.gain.value = .36; dlp.type = 'lowpass'; dlp.frequency.value = 2400; dly.connect(dlp).connect(fb).connect(dly); dlp.connect(comp); dlp.connect(rev);
    const env = (g, t, peak, a, d, floor) => { g.gain.setValueAtTime(.0001, t); g.gain.exponentialRampToValueAtTime(Math.max(.0002, peak), t + a); g.gain.exponentialRampToValueAtTime(floor || .0001, t + a + d); };
    const nz = (t, len) => { const s = ctx.createBufferSource(); s.buffer = K.noise; s.start(t, Math.random() * 1.6, len); return s; };
    const kick = (t, v) => { const o = ctx.createOscillator(), g = ctx.createGain(); o.frequency.setValueAtTime(140, t); o.frequency.exponentialRampToValueAtTime(46, t + .09); env(g, t, v * .5, .003, .2); o.connect(g).connect(drums); o.start(t); o.stop(t + .26); };
    const snare = (t, v) => { const s = nz(t, .2), bp = ctx.createBiquadFilter(), hp = ctx.createBiquadFilter(), g = ctx.createGain(); bp.type = 'bandpass'; bp.frequency.value = 1900 + Math.random() * 300; bp.Q.value = .6; hp.type = 'highpass'; hp.frequency.value = 500;
      env(g, t, v * .85, .002, .13); s.connect(bp).connect(hp).connect(g).connect(drums); if (v > .5) g.connect(rev);
      const o = ctx.createOscillator(), og = ctx.createGain(); o.type = 'triangle'; o.frequency.setValueAtTime(215, t); o.frequency.exponentialRampToValueAtTime(150, t + .07); env(og, t, v * .3, .002, .08); o.connect(og).connect(drums); o.start(t); o.stop(t + .12); };
    const hat = (t, v, open) => { const s = nz(t, open ? .22 : .06), hp = ctx.createBiquadFilter(), g = ctx.createGain(); hp.type = 'highpass'; hp.frequency.value = 7200; env(g, t, v * .34, .002, open ? .17 : .03); s.connect(hp).connect(g).connect(drums); };
    const bass = (t, dur, m, v) => { const o = ctx.createOscillator(), o2 = ctx.createOscillator(), g2 = ctx.createGain(), lp = ctx.createBiquadFilter(), g = ctx.createGain(), f = mtof(m); o.frequency.value = f; o2.type = 'triangle'; o2.frequency.value = f * 2; g2.gain.value = .12; lp.type = 'lowpass'; lp.frequency.value = 240;
      g.gain.setValueAtTime(.0001, t); g.gain.exponentialRampToValueAtTime(v * .17, t + .015); g.gain.setValueAtTime(v * .17, t + Math.max(.02, dur - .05)); g.gain.exponentialRampToValueAtTime(.0001, t + dur + .03);
      o.connect(lp); o2.connect(g2).connect(lp); lp.connect(g).connect(comp); o.start(t); o2.start(t); o.stop(t + dur + .06); o2.stop(t + dur + .06); };
    const padNote = (t, dur, m, bright) => { const lp = ctx.createBiquadFilter(), g = ctx.createGain(), att = bright ? .9 : .5; lp.type = 'lowpass'; lp.frequency.setValueAtTime(P.cut * .6, t); lp.frequency.linearRampToValueAtTime(P.cut, t + dur * .5); lp.frequency.linearRampToValueAtTime(P.cut * .7, t + dur); lp.Q.value = .4;
      g.gain.setValueAtTime(.0001, t); g.gain.linearRampToValueAtTime(bright ? .075 : .09, t + att); g.gain.setValueAtTime(bright ? .075 : .09, t + dur - .1); g.gain.linearRampToValueAtTime(.0001, t + dur + 1.1);
      for (const det of [-8, 7]) { const o = ctx.createOscillator(); o.type = 'sawtooth'; o.frequency.value = mtof(m); o.detune.value = det; o.connect(lp); o.start(t); o.stop(t + dur + 1.2); }
      lp.connect(g); g.connect(music); g.connect(rev); };
    const keys = (t, dur, m, v) => { const c = ctx.createOscillator(), mo = ctx.createOscillator(), mg = ctx.createGain(), g = ctx.createGain(), f = mtof(m); c.frequency.value = f; mo.frequency.value = f; mg.gain.setValueAtTime(f * 1.4, t); mg.gain.exponentialRampToValueAtTime(f * .25, t + .35);
      g.gain.setValueAtTime(.0001, t); g.gain.exponentialRampToValueAtTime(v * .2, t + .006); g.gain.exponentialRampToValueAtTime(v * .09, t + .4); g.gain.exponentialRampToValueAtTime(.0001, t + dur + .5);
      mo.connect(mg).connect(c.frequency); c.connect(g); g.connect(music); g.connect(rev); c.start(t); mo.start(t); c.stop(t + dur + .6); mo.stop(t + dur + .6); };
    const bell = (t, m, v) => { const c = ctx.createOscillator(), mo = ctx.createOscillator(), mg = ctx.createGain(), g = ctx.createGain(), f = mtof(m); c.frequency.value = f; mo.frequency.value = f * 3.5; mg.gain.setValueAtTime(f * 1.6, t); mg.gain.exponentialRampToValueAtTime(f * .05, t + .3);
      env(g, t, v * .17, .003, 1.1); mo.connect(mg).connect(c.frequency); c.connect(g); g.connect(music); g.connect(dly); g.connect(rev); c.start(t); mo.start(t); c.stop(t + 1.3); mo.stop(t + 1.3); };
    const pluck = (t, m, v) => { const o = ctx.createOscillator(), lp = ctx.createBiquadFilter(), g = ctx.createGain(); o.type = 'triangle'; o.frequency.value = mtof(m); lp.type = 'lowpass'; lp.frequency.setValueAtTime(3200, t); lp.frequency.exponentialRampToValueAtTime(600, t + .2);
      env(g, t, v * .24, .003, .28); o.connect(lp).connect(g); g.connect(music); g.connect(dly); o.start(t); o.stop(t + .4); };
    const flute = (t, dur, m, v) => { const o = ctx.createOscillator(), l = ctx.createOscillator(), lg = ctx.createGain(), g = ctx.createGain(); o.frequency.value = mtof(m); l.frequency.value = 5.2; lg.gain.value = mtof(m) * .006; l.connect(lg).connect(o.frequency);
      g.gain.setValueAtTime(.0001, t); g.gain.linearRampToValueAtTime(v * .14, t + .08); g.gain.setValueAtTime(v * .14, t + Math.max(.1, dur - .08)); g.gain.linearRampToValueAtTime(.0001, t + dur + .25);
      o.connect(g); g.connect(music); g.connect(rev); g.connect(dly); o.start(t); l.start(t); o.stop(t + dur + .3); l.stop(t + dur + .3); };
    const loops = [];   // background textures: record crackle, rain
    const texture = (buf, vol, type, freq) => { const s = ctx.createBufferSource(), f = ctx.createBiquadFilter(), g = ctx.createGain(); s.buffer = buf; s.loop = true; f.type = type; f.frequency.value = freq; g.gain.value = vol; s.connect(f).connect(g).connect(out); s.start(); loops.push(s); };
    if (P.crackle) texture(K.crackle, P.crackle * .5, 'highpass', 900); if (P.rain) texture(K.noise, P.rain * .05, 'bandpass', 3800);
    const tones = (ch) => ch[1].map((i) => ch[0] + i);
    function schedule(bar, t0) { const b2 = bar % 2, ch = P.chords[Math.floor(bar / 2) % P.chords.length], T = tones(ch), cyc = Math.floor(bar / 8);
      for (let s = 0; s < 16; s++) { const t = t0 + s * step + (s % 2 ? P.swing * step : 0), k = P.brk.k[b2][s], sn = P.brk.s[b2][s], h = P.hat[b2 % P.hat.length][s];
        if (k === 'x') kick(t, s === 0 ? 1 : .8); if (sn === 'x') snare(t, .95); else if (sn === 'g') snare(t, .28 + Math.random() * .1);
        if (h === 'x') hat(t, .9); else if (h === '-') hat(t, .4); else if (h === 'o') hat(t, .7, true); }
      for (const [s, len, off] of P.bass) if (Math.floor(s / 16) === b2) bass(t0 + (s % 16) * step, len * step * .96, ch[0] - 24 + off, 1);
      if (b2 === 0 && P.pad !== 'keys') for (const m of T) padNote(t0, 32 * step, m, P.pad === 'strings');
      if (P.pad === 'keys') for (const s of P.keys) if (Math.floor(s / 16) === b2) T.forEach((m, i) => keys(t0 + (s % 16) * step + i * .012, step * 5, m, s === 0 ? 1 : .75));
      for (const [s, idx, oct, len] of P.mel) { if (Math.floor(s / 16) !== b2) continue; if (cyc % 2 === 1 && (s + idx) % 3 === 0) continue;   // every other pass leaves a few notes out, so it breathes
        const m = T[idx % T.length] + oct + (idx >= T.length ? 12 : 0), t = t0 + (s % 16) * step;
        if (P.lead === 'bell') bell(t, m, .9); else if (P.lead === 'pluck') pluck(t, m, .9); else flute(t, len * step, m, .9); } }
    return { schedule, barLength: step * 16, out, loops };
  }
  function play(ctx, dest, index) { const P = presets[index], e = build(ctx, dest, P); let bar = 0, next = ctx.currentTime + .08;
    const pump = () => { while (next < ctx.currentTime + .6) { e.schedule(bar++, next); next += e.barLength; } }; pump(); const id = setInterval(pump, 120);
    return () => { clearInterval(id); const t = ctx.currentTime; e.out.gain.cancelScheduledValues(t); e.out.gain.setValueAtTime(e.out.gain.value, t); e.out.gain.linearRampToValueAtTime(0, t + .18);
      setTimeout(() => { e.loops.forEach((s) => { try { s.stop(); } catch (err) { /* already stopped */ } }); e.out.disconnect(); }, 400); }; }
  window.Jungle = { presets, build, play };
})();
