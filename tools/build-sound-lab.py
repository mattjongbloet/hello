"""Sound lab: ten generated liquid jungle loops to audition for the record on the home page's 3D face.
The loops are made in the browser by tools/toys/jungle.js (Web Audio, no audio files).
Output: redesigns/sound-lab/index.html   Re-run: python3 tools/build-sound-lab.py"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = os.path.join(ROOT, "redesigns", "sound-lab")
ENGINE = open(os.path.join(ROOT, "tools", "toys", "jungle.js")).read()
CSS = """
:root { --paper: #fff; --mist: #f6f6f4; --line: #e4e4df; --ink: #15171a; --ink-2: #5f636b; --signal: #b28550; --signal-soft: #f6efe4; --body: "Roobert", "Hanken Grotesk", system-ui, sans-serif; }
* { box-sizing: border-box; } body { margin: 0; font: 400 16px/1.5 var(--body); color: var(--ink); background: var(--mist); }
a { color: inherit; } :focus-visible { outline: 2px solid var(--signal); outline-offset: 3px; border-radius: 8px; }
.page { max-width: 1080px; margin: 0 auto; padding: 28px 20px 80px; }
.back { display: inline-block; padding: 12px 0; color: var(--ink-2); text-decoration: none; } .back:hover { color: var(--ink); }
h1 { font: 650 clamp(28px, 3.4vw, 40px)/1.1 var(--body); letter-spacing: -.025em; margin: 6px 0 8px; }
.intro { color: var(--ink-2); max-width: 66ch; margin: 0 0 22px; }
.bar { display: flex; flex-wrap: wrap; align-items: center; gap: 12px 20px; margin-bottom: 22px; font-size: 15px; color: var(--ink-2); }
.bar label { display: inline-flex; align-items: center; gap: 10px; min-height: 44px; } .bar input { width: 160px; height: 28px; accent-color: var(--ink); }
.stop { min-height: 44px; padding: 0 18px; border-radius: 999px; border: 0; background: color-mix(in srgb, var(--ink) 6%, transparent); color: var(--ink); font: 500 15px var(--body); cursor: pointer; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 320px), 1fr)); gap: 14px; }
.card { background: var(--paper); border: 1px solid #ebebe8; border-radius: 20px; padding: 20px; display: grid; grid-template-columns: 56px minmax(0, 1fr); column-gap: 16px; align-items: start; }
.card.on { border-color: var(--signal); box-shadow: 0 0 0 3px var(--signal-soft); }
.play { width: 56px; height: 56px; border-radius: 50%; border: 0; background: var(--ink); color: #fff; cursor: pointer; display: grid; place-items: center; }
.play svg { width: 22px; height: 22px; } .play .i-pause, .card.on .play .i-play { display: none; } .card.on .play .i-pause { display: block; } .card.on .play { background: var(--signal); color: #15171a; }
.card h2 { font: 600 18px/1.25 var(--body); margin: 0; display: flex; align-items: baseline; gap: 8px; } .card h2 b { font-weight: 500; color: var(--ink-2); font-size: 15px; }
.meta { font-size: 14px; color: var(--ink-2); margin: 2px 0 8px; } .desc { font-size: 15px; color: var(--ink-2); margin: 0; }
.eq { display: none; gap: 3px; align-items: flex-end; height: 14px; margin-left: 4px; } .card.on .eq { display: inline-flex; }
.eq i { width: 3px; background: var(--signal); border-radius: 2px; animation: eq .7s ease-in-out infinite alternate; } .eq i:nth-child(2) { animation-delay: -.25s; } .eq i:nth-child(3) { animation-delay: -.5s; }
@keyframes eq { from { height: 3px; } to { height: 14px; } } @media (prefers-reduced-motion: reduce) { .eq i { animation: none; height: 9px; } }
"""
JS = """
(() => {
  const grid = document.querySelector('.grid'), vol = document.querySelector('#vol'); let ctx = null, master = null, stop = null, current = -1;
  Jungle.presets.forEach((p, i) => { const el = document.createElement('article'); el.className = 'card';
    el.innerHTML = `<button class="play" type="button" aria-label="Play ${p.name}" aria-pressed="false"><svg class="i-play" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M8 5.5v13l11-6.5z"/></svg><svg class="i-pause" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M7 5h4v14H7zM13 5h4v14h-4z"/></svg></button>
      <div><h2><b>${i + 1}</b> ${p.name}<span class="eq" aria-hidden="true"><i></i><i></i><i></i></span></h2><p class="meta">${p.bpm} BPM · ${p.key}</p><p class="desc">${p.note}</p></div>`;
    el.querySelector('.play').addEventListener('click', () => toggle(i)); grid.appendChild(el); });
  const cards = [...grid.children];
  const halt = () => { if (stop) stop(); stop = null; current = -1; cards.forEach((c) => { c.classList.remove('on'); c.querySelector('.play').setAttribute('aria-pressed', 'false'); }); };
  const toggle = (i) => { const was = current; halt(); if (was === i) return;
    Jungle.unmute(); ctx = ctx || new (window.AudioContext || window.webkitAudioContext)(); if (ctx.state === 'suspended') ctx.resume();
    if (!master) { master = ctx.createGain(); master.connect(ctx.destination); } master.gain.value = +vol.value;
    stop = Jungle.play(ctx, master, i); current = i; cards[i].classList.add('on'); cards[i].querySelector('.play').setAttribute('aria-pressed', 'true'); };
  vol.addEventListener('input', () => { if (master) master.gain.value = +vol.value; });
  document.querySelector('.stop').addEventListener('click', halt); addEventListener('keydown', (e) => { if (e.key === 'Escape') halt(); });
})();
"""
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, "index.html"), "w").write(f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="../assets/mj-logo.svg" type="image/svg+xml">
<title>Liquid jungle: 10 loops</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;650;700&display=swap">
<link rel="stylesheet" href="../fonts/fonts.css">
<style>{CSS}</style>
</head>
<body>
<main class="page">
  <a class="back" href="../site/index.html">← Home page</a>
  <h1>Liquid jungle: 10 loops</h1>
  <p class="intro">Ten loops for the record on the home page, each generated in your browser from code: a break, a sub bass, chords and a lead. Nothing is downloaded. Press play on one; pressing another switches to it.</p>
  <div class="bar"><label>Volume <input id="vol" type="range" min="0" max="1" step="0.01" value="0.8"></label><button class="stop" type="button">Stop</button></div>
  <div class="grid"></div>
</main>
<script>{ENGINE}</script>
<script>{JS}</script>
</body>
</html>
""")
print("built sound-lab")
