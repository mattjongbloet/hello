"""Face lab: one page to try ideas for the 3D face's nose and mouth (the vinyl and wheel eyes stay).
Reuses the eyes from tools/toys/object-face.js. Output: redesigns/face-lab/.  Re-run: python3 tools/build-face-lab.py"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); T = os.path.join(ROOT, "tools", "toys"); OUT = os.path.join(ROOT, "redesigns", "face-lab")
rd = lambda n: open(os.path.join(T, n)).read()
src = rd("object-face.js"); a = src.index("  // ---- Left eye: vinyl record ----"); b = src.index("  // ---- Nose: a tree ----")
import base64, io
from PIL import Image
im = Image.open(os.path.join(ROOT, "redesigns", "assets", "art-why.jpg")).convert("RGB"); im = im.resize((760, round(760 * im.height / im.width)), Image.LANCZOS)
buf = io.BytesIO(); im.save(buf, "JPEG", quality=82)   # embedded so the 3D texture also loads from file://
ART = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
js = rd("three-common.js") + "\n" + rd("face-lab.js").replace("/*EYES*/", src[a:b]).replace("%%ART%%", ART)
NOSES = [("tree", "Tree (current)"), ("cursor", "Cursor (smaller)"), ("pinecone", "Pinecone"), ("tent", "Tent"), ("trowel", "Trowel"), ("art", "Framed art")]
MOUTHS = [("beans", "Coffee beans (current)"), ("bezier", "Bezier curve"), ("trail", "Hiking trail"), ("swatches", "Colour swatches"), ("stroopwafel", "Stroopwafel")]
btn = lambda kind, items, cur: "".join(f'<button type="button" data-kind="{kind}" data-name="{n}" aria-pressed="{"true" if n == cur else "false"}">{label}</button>' for n, label in items)
HTML = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="icon" href="../assets/mj-logo.svg" type="image/svg+xml">
<title>Face lab — nose and mouth ideas</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="../fonts/fonts.css">
<link rel="stylesheet" href="lab.css">
</head>
<body>
<main class="lab">
  <header class="lab-head">
    <a class="lab-back" href="../site/index.html">← Back to the home page</a>
    <h1>Face lab</h1>
    <p>The vinyl and the wheel stay as the eyes. Pick a nose and a mouth, then hover and click them on the face.</p>
  </header>
  <div class="lab-grid">
    <div class="lab-face">
      <div class="lab-stage-wrap"><div class="toy-stage" role="img" aria-label="A face made of 3D objects, with a switchable nose and mouth"></div><div class="lab-overlay" aria-hidden="true"></div></div>
      <p class="lab-tip" aria-live="polite">Click the framed art to open it. Click the stroopwafel to take bites.</p>
    </div>
    <div class="lab-opts">
      <h2>Nose</h2><div role="group" aria-label="Nose">{btn("nose", NOSES, "art")}</div>
      <h2>Mouth</h2><div role="group" aria-label="Mouth">{btn("mouth", MOUTHS, "stroopwafel")}</div>
      <p class="lab-note">Each one has its click behaviour working. The accent colour here <span class="lab-accent">looks like this</span>, and changes when you pick a swatch.</p>
    </div>
  </div>
</main>
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script src="lab.js"></script>
</body>
</html>
"""
CSS = """/* Face lab (tools/build-face-lab.py): a single page to compare nose and mouth ideas for the 3D face. */
:root { --paper: #ffffff; --mist: #f4f4f1; --line: #e4e4df; --ink: #15171a; --ink-2: #5f636b; --signal: #b28550;
  --body: "Roobert", "Hanken Grotesk", ui-sans-serif, system-ui, sans-serif; }
*, *::before, *::after { box-sizing: border-box; }
body { margin: 0; background: var(--paper); color: var(--ink); font: 16px/1.55 var(--body); -webkit-font-smoothing: antialiased; }
.lab { max-width: 1160px; margin: 0 auto; padding: 32px max(20px, env(safe-area-inset-left, 0px)) 72px; }
.lab-head { display: flex; flex-direction: column; gap: 8px; margin-bottom: 20px; }
.lab-back { color: var(--ink-2); text-decoration: none; font-size: 15px; align-self: flex-start; padding-block: 8px; }
.lab-back:hover { color: var(--ink); }
.lab-head h1 { margin: 0; font-size: clamp(30px, 4vw, 44px); letter-spacing: -0.03em; line-height: 1.05; }
.lab-head p { margin: 0; color: var(--ink-2); max-width: 60ch; }
.lab-grid { display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr); gap: 48px; align-items: start; }
.lab-face { display: flex; flex-direction: column; gap: 12px; }
.lab-stage-wrap { position: relative; width: min(100%, calc(100svh - 300px)); min-width: 260px; margin-inline: auto; }
.toy-stage { position: relative; width: 100%; aspect-ratio: 1; touch-action: none; }
.toy-stage canvas { position: absolute; inset: 0; width: 100%; height: 100%; display: block; }
.lab-tip { margin: 0; min-height: 3.1em; text-align: center; color: var(--ink-2); font-size: 15px; }
.lab-opts { display: flex; flex-direction: column; gap: 12px; padding-top: 12px; }
.lab-opts h2 { margin: 12px 0 0; font-size: 15px; font-weight: 600; color: var(--ink-2); }
.lab-opts div { display: flex; flex-wrap: wrap; gap: 8px; }
.lab-opts button { font: 500 15px/1 var(--body); padding: 12px 16px; border-radius: 999px; border: 0; background: var(--mist); color: var(--ink); cursor: pointer; transition: background .15s, color .15s; }
.lab-opts button:hover { background: var(--line); }
.lab-opts button[aria-pressed="true"] { background: var(--ink); color: var(--paper); }
.lab-opts button:focus-visible, .lab-back:focus-visible { outline: 2px solid var(--signal); outline-offset: 3px; border-radius: 999px; }
.lab-note { margin: 16px 0 0; color: var(--ink-2); font-size: 15px; }
.lab-accent { border-bottom: 3px solid var(--signal); color: var(--ink); font-weight: 600; }
/* Edit mode (cursor nose) */
.lab-overlay { position: absolute; inset: 0; pointer-events: none; opacity: 0; transition: opacity .2s; }
.lab-overlay.on { opacity: 1; }
.lab-box { position: absolute; border: 1.5px solid #2f6bff; }
.lab-box i { position: absolute; width: 8px; height: 8px; background: #fff; border: 1.5px solid #2f6bff; }
.lab-box i:nth-child(1) { left: -5px; top: -5px; } .lab-box i:nth-child(2) { right: -5px; top: -5px; } .lab-box i:nth-child(3) { left: -5px; bottom: -5px; } .lab-box i:nth-child(4) { right: -5px; bottom: -5px; }
.lab-box span { position: absolute; left: 50%; bottom: -24px; transform: translateX(-50%); background: #2f6bff; color: #fff; font-size: 11px; line-height: 1; padding: 4px 6px; border-radius: 4px; white-space: nowrap; }
.lab-box b { position: absolute; left: -1.5px; top: -20px; color: #2f6bff; font-size: 11px; font-weight: 600; line-height: 1; }
.lab-gap { position: absolute; height: 0; border-top: 1.5px solid #f0326e; }
.lab-gap::before, .lab-gap::after { content: ""; position: absolute; top: -6px; height: 11px; border-left: 1.5px solid #f0326e; }
.lab-gap::before { left: 0; } .lab-gap::after { right: 0; }
.lab-gap span { position: absolute; left: 50%; top: -22px; transform: translateX(-50%); background: #f0326e; color: #fff; font-size: 11px; line-height: 1; padding: 4px 6px; border-radius: 4px; }
/* Lightbox for the framed art */
.art-lightbox { position: fixed; inset: 0; z-index: 100; display: grid; place-items: center; padding: 56px 20px 20px; background: rgb(10 10 12 / .88); cursor: zoom-out; }
.art-lightbox img { max-width: min(100%, 760px); max-height: calc(100vh - 84px); border-radius: 6px; box-shadow: 0 30px 80px rgb(0 0 0 / .6); }
.art-lightbox button { position: absolute; top: 12px; right: 16px; font: 500 15px/1 var(--body); padding: 12px 16px; border-radius: 999px; border: 0; background: #fff; color: #15171a; cursor: pointer; }
@media (max-width: 860px) { .lab-grid { grid-template-columns: 1fr; gap: 12px; } .lab-stage-wrap { width: min(100%, 420px); } }
"""
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, "index.html"), "w").write(HTML); open(os.path.join(OUT, "lab.css"), "w").write(CSS); open(os.path.join(OUT, "lab.js"), "w").write(js)
print("built face-lab")
