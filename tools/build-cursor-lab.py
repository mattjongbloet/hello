"""Cursor lab: a playground for hover cursors on the 3D face. Five ideas for each object (record, wheel, framed art,
stroopwafel), three drawing styles, and two modes (replace the pointer, or sit beside the hand).
Uses the home page's face (redesigns/site/toy.js), so run after build-hero-toys.py.
Output: redesigns/cursor-lab/index.html   Re-run: python3 tools/build-cursor-lab.py"""
import os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = os.path.join(ROOT, "redesigns", "cursor-lab")
C = lambda cx, cy, r: f'<circle cx="{cx}" cy="{cy}" r="{r}"/>'
P = lambda d: f'<path d="{d}"/>'
# ---- Round 3: Matt is set on play/pause, spin arrow, magnifier and chomper. Five high-fidelity line drawings of each,
# built from exact geometry on a 24px grid (round caps and joins, optically centred), so they stay crisp at cursor size.
import math
INK = "#15171a"
f = lambda v: f"{v:.2f}".rstrip("0").rstrip(".")
pt = lambda cx, cy, r, deg: (cx + r * math.cos(math.radians(deg)), cy + r * math.sin(math.radians(deg)))
def arc(cx, cy, r, a0, a1):                      # clockwise on screen from a0 to a1 (degrees, 0 = right, 90 = down)
    (x0, y0), (x1, y1) = pt(cx, cy, r, a0), pt(cx, cy, r, a1)
    return f"M{f(x0)} {f(y0)}A{f(r)} {f(r)} 0 {1 if (a1 - a0) % 360 > 180 else 0} 1 {f(x1)} {f(y1)}"
def head(cx, cy, r, a, L=3.3, spread=32):        # arrowhead at the end of a clockwise arc
    x, y = pt(cx, cy, r, a); d = a + 90 - 8      # direction of travel, tucked in a touch so it sits on the curve
    (ax, ay), (bx, by) = pt(x, y, L, d + 180 - spread), pt(x, y, L, d + 180 + spread)
    return f"M{f(ax)} {f(ay)}L{f(x)} {f(y)}L{f(bx)} {f(by)}"
dot = lambda cx, cy, r=1: f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{INK}" stroke="none"/>'
tint = 'fill="rgba(21,23,26,.12)"'
# play: a triangle with eased corners, nudged right so it looks centred in the chip; pause: two rounded bars
TRI = "M9 6.3a1 1 0 0 1 1.53-.85l9.05 5.7a1 1 0 0 1 0 1.7l-9.05 5.7A1 1 0 0 1 9 17.7z"
BARS = '<rect x="7.25" y="5.5" width="3.25" height="13" rx="1.1"{0}/><rect x="13.5" y="5.5" width="3.25" height="13" rx="1.1"{0}/>'
RING = '<circle cx="12" cy="12" r="9.25"/>'
SMALLTRI = "M10.3 8.6a.7.7 0 0 1 1.07-.6l4.7 2.96a.7.7 0 0 1 0 1.18l-4.7 2.96a.7.7 0 0 1-1.07-.6z"
def chomp(half=32, r=8.5, cx=11.4, cy=12):       # a round head with a wedge mouth opening to the right
    (ux, uy), (lx, ly) = pt(cx, cy, r, -half), pt(cx, cy, r, half)
    return f"M{f(cx)} {f(cy)}L{f(ux)} {f(uy)}A{f(r)} {f(r)} 0 1 0 {f(lx)} {f(ly)}Z"
def teeth(half=34, r=8.5, cx=11.4, cy=12):       # two small solid teeth on each jaw, pointing into the mouth
    out = ""
    for sign in (-1, 1):
        for t in (.5, .78):
            (ax, ay), (bx, by) = pt(cx, cy, r * (t - .11), sign * half), pt(cx, cy, r * (t + .11), sign * half)
            mx, my = pt(cx, cy, r * t, sign * half); tx, ty = pt(mx, my, 2.1, sign * half - sign * 90)
            out += f'<path d="M{f(ax)} {f(ay)}L{f(tx)} {f(ty)}L{f(bx)} {f(by)}Z" fill="{INK}" stroke-width="1"/>'
    return out
EYE = dot(12.3, 7.5, 1.05)
LENS, HANDLE, PLUS = '<circle cx="10.5" cy="10.5" r="6.25"{0}/>', "M15.1 15.1l5.15 5.15", "M10.5 7.9v5.2M7.9 10.5h5.2"
# (name, stroke width, drawing, drawing while the record plays)
IDEAS = {
 "music": ("Record: play / pause", [
  ("Outline", 1.75, P(TRI), BARS.format("")),
  ("Solid", 1.75, f'<path d="{TRI}" fill="{INK}"/>', BARS.format(f' fill="{INK}"')),
  ("Soft fill", 1.75, f'<path d="{TRI}" {tint}/>', BARS.format(f" {tint}")),
  ("Light, in a ring", 1.5, RING + P(SMALLTRI), RING + '<path d="M10 8.75v6.5M14 8.75v6.5"/>'),
  ("Bold", 2.1, P(TRI), BARS.format(""))]),
 "cycle": ("Wheel: spin", [
  ("Single arrow", 1.75, P(arc(12, 12, 7.5, -48, 250) + head(12, 12, 7.5, 250)), None),
  ("Two arrows", 1.75, P(arc(12, 12, 7.5, 200, 338) + head(12, 12, 7.5, 338) + arc(12, 12, 7.5, 20, 158) + head(12, 12, 7.5, 158)), None),
  ("Arrow round a hub", 1.75, P(arc(12, 12, 8, -48, 250) + head(12, 12, 8, 250)) + '<circle cx="12" cy="12" r="1.9"/>', None),
  ("Arrow round a wheel", 1.6, '<circle cx="11.5" cy="12.5" r="5.25"/>' + dot(11.5, 12.5, 1.05) + P(arc(11.5, 12.5, 8.9, 205, 318) + head(11.5, 12.5, 8.9, 318, 3)), None),
  ("Bold", 2.1, P(arc(12, 12, 7.25, -44, 246) + head(12, 12, 7.25, 246, 3.6)), None)]),
 "nose": ("Framed art: magnifier", [
  ("Plus", 1.75, LENS.format("") + P(HANDLE + PLUS), None),
  ("Plus, heavy handle", 1.75, LENS.format("") + P(PLUS) + '<path d="M15.3 15.3l4.6 4.6" stroke-width="3"/>', None),
  ("Glint, no plus", 1.75, LENS.format("") + P(HANDLE + arc(10.5, 10.5, 3.5, 190, 262)), None),
  ("Soft fill", 1.75, LENS.format(f" {tint}") + P(HANDLE + PLUS), None),
  ("Bold", 2.1, '<circle cx="10.5" cy="10.5" r="6"/>' + P("M15 15l5 5M10.5 8v5M8 10.5h5"), None)]),
 "mouth": ("Stroopwafel: chomper", [
  ("Chomper", 1.75, P(chomp()) + EYE, None),
  ("With teeth", 1.75, P(chomp(34)) + teeth() + EYE, None),
  ("With crumbs", 1.75, P(chomp(34, 8.2, 10.6)) + dot(11.5, 7.6, 1.05) + dot(18.6, 12, .8) + dot(21.4, 10.2, .7) + dot(21.6, 13.6, .7), None),
  ("About to eat", 1.75, P(chomp(36, 8, 10.2)) + dot(11.1, 7.7, 1.05) + '<circle cx="19.6" cy="12" r="2.3"/>', None),
  ("Soft fill", 1.75, f'<path d="{chomp()}" {tint}/>' + EYE, None)]),
}
PAUSE = ""
DATA = json.dumps({k: {"label": v[0], "ideas": [{"name": n, "w": w, "svg": s, "alt": alt} for n, w, s, alt in v[1]]} for k, v in IDEAS.items()}, ensure_ascii=False)
CSS = """
:root { --paper: #fff; --mist: #f6f6f4; --line: #e4e4df; --ink: #15171a; --ink-2: #5f636b; --signal: #b28550; --signal-soft: #f6efe4; --body: "Roobert", "Hanken Grotesk", system-ui, sans-serif; --mono: var(--body); }
* { box-sizing: border-box; } body { margin: 0; font: 400 16px/1.5 var(--body); color: var(--ink); background: var(--mist); }
a { color: inherit; } :focus-visible { outline: 2px solid var(--signal); outline-offset: 3px; border-radius: 8px; }
.page { max-width: 1200px; margin: 0 auto; padding: 28px 20px 80px; }
.back { display: inline-block; padding: 12px 0; color: var(--ink-2); text-decoration: none; } .back:hover { color: var(--ink); }
h1 { font: 650 clamp(28px, 3.4vw, 40px)/1.1 var(--body); letter-spacing: -.025em; margin: 6px 0 8px; }
.intro { color: var(--ink-2); max-width: 68ch; margin: 0 0 24px; }
.play { display: grid; grid-template-columns: minmax(0, 520px) minmax(0, 1fr); gap: 28px; align-items: start; }
.face { position: sticky; top: 16px; background: var(--paper); border: 1px solid #ebebe8; border-radius: 24px; padding: 20px 20px 16px; }
.face .hero-toy { max-width: none; } .face .toy-hint { font: 400 14px/1.4 var(--body); letter-spacing: 0; text-transform: none; }
.pick { margin: 12px 0 0; font-size: 14px; color: var(--ink-2); text-align: center; min-height: 42px; }
.big { display: flex; flex-wrap: wrap; justify-content: center; gap: 10px 14px; margin-top: 6px; padding-top: 14px; border-top: 1px solid var(--line); }
.big figure { margin: 0; display: grid; grid-auto-flow: column; grid-template-rows: auto auto; gap: 6px 6px; justify-items: center; } .big img { width: 72px; height: 72px; grid-row: 1; } .big figcaption { grid-row: 2; grid-column: 1 / -1; font-size: 13px; color: var(--ink-2); }
.panel { display: grid; gap: 14px; }
.box { background: var(--paper); border: 1px solid #ebebe8; border-radius: 20px; padding: 18px 20px; }
.box h2 { font: 600 16px/1.2 var(--body); margin: 0 0 12px; }
.seg { display: flex; flex-wrap: wrap; gap: 8px; } .row { display: flex; flex-wrap: wrap; gap: 14px 28px; } .row > div > span { display: block; font-size: 13px; color: var(--ink-2); margin-bottom: 6px; }
button.opt { display: inline-flex; align-items: center; gap: 8px; min-height: 44px; padding: 0 14px 0 10px; border-radius: 999px; border: 0; background: color-mix(in srgb, var(--ink) 6%, transparent); color: var(--ink); font: 500 14px var(--body); cursor: pointer; }
button.opt.plain { padding: 0 16px; }
button.opt[aria-pressed="true"] { background: var(--ink); color: #fff; }
button.opt img { width: 28px; height: 28px; border-radius: 50%; background: #fff; flex: none; }
.badge { position: fixed; left: 0; top: 0; z-index: 50; width: 34px; height: 34px; pointer-events: none; display: none; filter: drop-shadow(0 3px 6px rgb(0 0 0 / .25)); } .badge img { width: 100%; height: 100%; display: block; }
@media (max-width: 900px) { .play { grid-template-columns: 1fr; } .face { position: static; } }
"""
JS = """
(() => {
  const DATA = %%DATA%%, PAUSE = %%PAUSE%%, KEYS = Object.keys(DATA);
  const state = { style: 'chip', mode: 'replace', size: 32, pick: { music: 0, cycle: 0, nose: 0, mouth: 0 }, playing: false };
  const esc = (s) => encodeURIComponent(s).replace(/'/g, '%27').replace(/\\(/g, '%28').replace(/\\)/g, '%29');
  // Build one icon as an SVG string in the chosen style.
  const icon = (key, i, style, px, still) => { const idea = DATA[key].ideas[i], art = idea.alt && state.playing && !still ? idea.alt : idea.svg, W = idea.w || 1.75;
    const strokes = (w, col) => `<g fill="none" stroke="${col}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round">${art}</g>`;
    if (style === 'chip') return `<svg xmlns="http://www.w3.org/2000/svg" width="${px}" height="${px}" viewBox="-5 -5 34 34"><circle cx="12" cy="12" r="16" fill="#fff" stroke="rgba(21,23,26,.18)" stroke-width="1"/>${strokes(W, '#15171a')}</svg>`;
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${px}" height="${px}" viewBox="-2 -2 28 28">${strokes(W + 2.8, '#fff')}${strokes(W, '#15171a')}</svg>`; };
  const uri = (svg) => `data:image/svg+xml,${esc(svg)}`;
  const stage = document.querySelector('.toy-stage'), badge = document.querySelector('.badge'), badgeImg = badge.querySelector('img'), pickEl = document.querySelector('.pick'), big = document.querySelector('.big');
  const apply = (e) => { const key = stage.dataset.hover, i = key && key in state.pick ? state.pick[key] : -1;
    if (i < 0) { badge.style.display = 'none'; return; }                                     // not over an object, or "hand" chosen: leave the face's own cursor
    if (state.mode === 'replace') { badge.style.display = 'none'; const h = Math.round(state.size / 2); stage.style.cursor = `url("${uri(icon(key, i, state.style, state.size))}") ${h} ${h}, pointer`; }
    else { stage.style.cursor = 'pointer'; badgeImg.src = uri(icon(key, i, state.style, 68)); badge.style.width = badge.style.height = (state.size + 2) + 'px'; badge.style.display = 'block'; if (e) badge.style.transform = `translate(${e.clientX + 14}px, ${e.clientY + 16}px)`; } };
  stage.addEventListener('pointermove', apply); stage.addEventListener('pointerleave', () => { badge.style.display = 'none'; });
  stage.addEventListener('click', (e) => { if (stage.dataset.hover === 'music') { state.playing = !state.playing; apply(e); } });
  // controls
  const panel = document.querySelector('.panel');
  const seg = (title, items, get, set) => { const d = document.createElement('div'); d.innerHTML = `<span>${title}</span><div class="seg"></div>`;
    items.forEach(([val, label]) => { const b = document.createElement('button'); b.type = 'button'; b.className = 'opt plain'; b.textContent = label; b.dataset.val = val; b.addEventListener('click', () => { set(val); render(); }); d.querySelector('.seg').appendChild(b); });
    d._sync = () => d.querySelectorAll('button').forEach((b) => b.setAttribute('aria-pressed', String(String(get()) === b.dataset.val))); return d; };
  const top = document.createElement('section'); top.className = 'box'; top.innerHTML = '<h2>How it shows</h2><div class="row"></div>';
  const segs = [seg('Style', [['chip', 'Chip'], ['line', 'Line only']], () => state.style, (v) => { state.style = v; }),
    seg('Mode', [['replace', 'Replaces the cursor'], ['badge', 'Beside the hand']], () => state.mode, (v) => { state.mode = v; }),
    seg('Size', [['32', 'Small'], ['44', 'Large']], () => state.size, (v) => { state.size = +v; })];
  segs.forEach((s) => top.querySelector('.row').appendChild(s)); panel.appendChild(top);
  const groups = KEYS.map((key) => { const box = document.createElement('section'); box.className = 'box'; box.innerHTML = `<h2>${DATA[key].label}</h2><div class="seg"></div>`;
    [...DATA[key].ideas.map((d, i) => [i, d.name])].forEach(([i, name]) => { const b = document.createElement('button'); b.type = 'button'; b.className = 'opt' + (i < 0 ? ' plain' : ''); b.dataset.i = i;
      b.innerHTML = (i < 0 ? '' : '<img alt="">') + `<span>${i < 0 ? name : (i + 1) + '. ' + name}</span>`; b.addEventListener('click', () => { state.pick[key] = i; render(); }); box.querySelector('.seg').appendChild(b); });
    panel.appendChild(box); return [key, box]; });
  const render = () => { segs.forEach((s) => s._sync());
    groups.forEach(([key, box]) => box.querySelectorAll('button').forEach((b) => { const i = +b.dataset.i; b.setAttribute('aria-pressed', String(state.pick[key] === i)); const im = b.querySelector('img'); if (im) im.src = uri(icon(key, i, 'line', 56, true)); }));
    big.innerHTML = KEYS.map((k) => `<figure><img alt="" src="${uri(icon(k, state.pick[k], state.style, 192, true))}">${DATA[k].ideas[state.pick[k]].alt ? `<img alt="" src="${uri(icon(k, state.pick[k], state.style, 192, true).replace(DATA[k].ideas[state.pick[k]].svg, DATA[k].ideas[state.pick[k]].alt))}">` : ''}<figcaption>${DATA[k].label.split(':')[0]}</figcaption></figure>`).join('');
    pickEl.textContent = 'Your picks: ' + KEYS.map((k) => DATA[k].label.split(':')[0] + ' ' + (state.pick[k] + 1)).join(', ') + ' · ' + { chip: 'Chip', line: 'Line only' }[state.style] + ' · ' + (state.mode === 'replace' ? 'replaces the cursor' : 'beside the hand') + ' · ' + (state.size > 32 ? 'large' : 'small');
    apply(); };
  render();
})();
""".replace("%%DATA%%", DATA).replace("%%PAUSE%%", json.dumps(PAUSE))
FACE = open(os.path.join(ROOT, "tools", "toys", "face-home.html")).read()
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, "index.html"), "w").write(f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="../assets/mj-logo.svg" type="image/svg+xml">
<title>Hover cursors: playground</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;650;700&display=swap">
<link rel="stylesheet" href="../fonts/fonts.css">
<link rel="stylesheet" href="../site/toy.css">
<style>{CSS}</style>
</head>
<body>
<main class="page">
  <a class="back" href="../site/index.html">← Home page</a>
  <h1>Hover cursors: playground</h1>
  <p class="intro">Five refined line drawings of each chosen icon: play / pause, spin, magnifier and chomper. Pick one per object, then move your pointer over the face to try it. Your picks are shown enlarged under the face. Needs a mouse or trackpad: there is no hover on a touch screen.</p>
  <div class="play">
    <div class="face">
{FACE}
      <p class="pick" aria-live="polite"></p>
      <div class="big" aria-label="Your current picks, enlarged"></div>
    </div>
    <div class="panel"></div>
  </div>
</main>
<div class="badge" aria-hidden="true"><img alt=""></div>
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script src="../site/toy.js"></script>
<script>{JS}</script>
</body>
</html>
""")
print("built cursor-lab")
