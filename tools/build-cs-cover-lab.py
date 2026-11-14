"""Case-study opening lab: three ways to put the cover image first, before the headline, on the PMI case study.
Everything else on the page (facts, metric tiles, contents menu, body, next project) stays as it is.
Reads the built redesigns/case-studies/pmi.html, so run after build-case-studies.py.
Output: redesigns/cs-cover-lab/ (index.html + option-1..3.html)   Re-run: python3 tools/build-cs-cover-lab.py"""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = os.path.join(ROOT, "redesigns", "cs-cover-lab")
src = open(os.path.join(ROOT, "redesigns", "case-studies", "pmi.html")).read()
OPEN = re.compile(r'  <section class="wrap cs-hero">.*?</section>\s*<div class="wrap">\s*(<div class="cs-cover.*?</div>)\s*(<div class="results.*?</div></div>)\s*</div>\n', re.S)
m = OPEN.search(src); assert m, "PMI opening not found"
hero = m.group(0)
crumbs = re.search(r'<nav class="crumbs".*?</nav>', hero, re.S).group(0)
h1 = re.search(r'<h1>.*?</h1>', hero, re.S).group(0)
dek = re.search(r'<p class="dek">.*?</p>', hero, re.S).group(0)
meta = re.search(r'<dl class="meta.*?</dl>', hero, re.S).group(0)
cover, results = m.group(1), m.group(2)
OPTS = [
 ("Image first, same layout", "The smallest change: the cover moves above the headline, full width of the column. Title, intro and facts follow, left-aligned as now.",
  f"""  <div class="wrap cl-top">
    {crumbs}
    {cover}
  </div>
  <section class="wrap cs-hero cl-1">
    {h1}
    {dek}
    {meta}
  </section>
  <div class="wrap">
    {results}
  </div>
""", """
.cl-top { padding-top: 28px; } .cl-top .crumbs { margin-bottom: 20px; }
.cl-top .cs-cover { border-radius: 24px; overflow: hidden; }
.cl-1 { padding-top: 56px; padding-bottom: 28px; }
"""),
 ("Framed stage", "Like your reference: the cover sits inside a dark stage with room around it, then a centred title, intro and facts. The metric tiles stay as they are.",
  f"""  <div class="wrap cl-top">
    {crumbs}
    <div class="cl-stage">{cover}</div>
  </div>
  <section class="wrap cs-hero cl-2">
    {h1}
    {dek}
    {meta}
  </section>
  <div class="wrap">
    {results}
  </div>
""", """
.cl-top { padding-top: 28px; } .cl-top .crumbs { margin-bottom: 20px; }
.cl-stage { background: #0f1012; border-radius: 28px; padding: clamp(28px, 6vw, 72px) clamp(20px, 7vw, 96px) 0; overflow: hidden; }
.cl-stage .cs-cover { border-radius: 18px 18px 0 0; overflow: hidden; box-shadow: 0 30px 60px -30px rgb(0 0 0 / .35); background: none; }
:root[data-theme="dark"] .cl-stage { background: #000; box-shadow: inset 0 0 0 1px var(--line); }
.cl-2 { text-align: center; padding-top: 64px; padding-bottom: 28px; }
.cl-2 h1 { margin-inline: auto; max-width: 20ch; }
.cl-2 .dek { margin-inline: auto; max-width: 56ch; }
.cl-2 .meta { justify-content: center; text-align: left; margin-inline: auto; max-width: 980px; }
"""),
 ("Full-bleed cover, split title", "The cover runs edge to edge across the screen, then the title sits on the left with the intro and facts beside it, like a magazine opener.",
  f"""  <div class="wrap cl-top">{crumbs}</div>
  <div class="cl-bleed">{cover}</div>
  <section class="wrap cs-hero cl-3">
    <div class="cl-3-title">{h1}</div>
    <div class="cl-3-side">
      {dek}
      {meta}
    </div>
  </section>
  <div class="wrap">
    {results}
  </div>
""", """
.cl-top { padding-top: 28px; padding-bottom: 20px; }
.cl-bleed .cs-cover { border-radius: 0; max-height: 78svh; overflow: hidden; }
.cl-bleed .cs-cover img { width: 100%; height: 100%; max-height: 78svh; object-fit: cover; object-position: 50% 30%; }
.cl-3 { display: grid; grid-template-columns: minmax(0, 1.1fr) minmax(0, 1fr); gap: 24px 56px; align-items: start; padding-top: 56px; padding-bottom: 28px; }
.cl-3 h1 { margin: 0; }
.cl-3 .dek { margin-top: 6px; }
.cl-3 .meta { grid-template-columns: repeat(2, minmax(0, 1fr)); }
@media (max-width: 860px) { .cl-3 { grid-template-columns: 1fr; padding-top: 36px; } }
"""),
]
os.makedirs(OUT, exist_ok=True)
for i, (name, note, html, css) in enumerate(OPTS, 1):
    page = src.replace(hero, html, 1).replace("<head>", '<head>\n<base href="../case-studies/">', 1).replace("</head>", f"<style>{css}</style>\n</head>", 1)
    open(os.path.join(OUT, f"option-{i}.html"), "w").write(page)
frames = "\n".join(f'''  <section class="opt">
    <h2><b>{i}</b> {name} <a href="option-{i}.html">Open full page →</a></h2>
    <p class="note">{note}</p>
    <iframe src="option-{i}.html" title="PMI case study, option {i}: {name}" loading="lazy"></iframe>
  </section>''' for i, (name, note, _, _) in enumerate(OPTS, 1))
open(os.path.join(OUT, "index.html"), "w").write(f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="../assets/mj-logo.svg" type="image/svg+xml">
<title>Case study: image first</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;650;700&display=swap">
<link rel="stylesheet" href="../fonts/fonts.css">
<style>
:root {{ --paper: #fff; --mist: #f6f6f4; --line: #e4e4df; --ink: #15171a; --ink-2: #5f636b; --signal: #b28550; --body: "Roobert", "Hanken Grotesk", system-ui, sans-serif; }}
* {{ box-sizing: border-box; }} body {{ margin: 0; font: 400 16px/1.5 var(--body); color: var(--ink); background: var(--mist); }}
a {{ color: inherit; }} :focus-visible {{ outline: 2px solid var(--signal); outline-offset: 3px; border-radius: 8px; }}
.page {{ max-width: 1520px; margin: 0 auto; padding: 28px 20px 80px; }}
.back {{ display: inline-block; padding: 12px 0; color: var(--ink-2); text-decoration: none; }} .back:hover {{ color: var(--ink); }}
h1 {{ font: 650 clamp(28px, 3.4vw, 40px)/1.1 var(--body); letter-spacing: -.025em; margin: 6px 0 8px; }}
.intro {{ color: var(--ink-2); max-width: 70ch; margin: 0; }}
.opt {{ margin-top: 40px; }}
.opt h2 {{ font: 600 18px/1.2 var(--body); margin: 0 0 4px; display: flex; flex-wrap: wrap; align-items: center; gap: 6px 12px; }}
.opt h2 b {{ display: grid; place-items: center; width: 28px; height: 28px; border-radius: 50%; background: var(--ink); color: #fff; font-size: 13px; }}
.opt h2 a {{ font-weight: 500; font-size: 15px; color: var(--ink-2); padding: 12px 0; }}
.note {{ margin: 0 0 14px; color: var(--ink-2); font-size: 15px; max-width: 80ch; }}
.opt iframe {{ display: block; width: 100%; height: min(1000px, 90vh); border: 1px solid var(--line); border-radius: 18px; background: #fff; }}
</style>
</head>
<body>
<main class="page">
  <a class="back" href="../case-studies/pmi.html">← Current PMI case study</a>
  <h1>Case study: image first</h1>
  <p class="intro">Three ways to let the imagery speak first, using the PMI case study. Only the opening changes; the facts, metric tiles, contents menu and body are the format you already have. Each frame is live: scroll it, or open it full page.</p>
{frames}
</main>
</body>
</html>
""")
print("built cs-cover-lab")
