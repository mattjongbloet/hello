"""Meta lab: fifteen treatments of the two items under the hero intro ("Amsterdam, NL" + flag, "Designing @ Hospitable").
Reads the flag and logo from the built home page, so run after build-a-cv.py.  Output: redesigns/meta-lab/index.html
Re-run: python3 tools/build-meta-lab.py"""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = os.path.join(ROOT, "redesigns", "meta-lab")
home = open(os.path.join(ROOT, "redesigns", "site", "index.html")).read()
FLAG = re.search(r'<svg class="flag".*?</svg>', home, re.S).group(0)
LOGO = re.search(r'<svg[^>]*class="hosp".*?</svg>', home, re.S).group(0)
LEDE = re.search(r'<p class="lede">(.*?)</p>', home, re.S).group(1)
LINK = f'<a class="hosp-link" href="https://hospitable.com/" aria-label="Hospitable">{LOGO}</a>'
PIN = '<svg class="pin" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7Zm0 9.6A2.6 2.6 0 1 1 12 6.4a2.6 2.6 0 0 1 0 5.2Z"/></svg>'
std = f'<span class="hm">{FLAG}Amsterdam, NL</span><span class="hm">Designing @{LINK}</span>'
V = [  # (name, note, markup or None for the standard two items)
 ("Plain", "No container: type weight alone separates it from the intro.", None),
 ("Soft pills", "Each item in a pill of the text colour at 6%. On the home page now.", None),
 ("Outlined pills", "A hairline border, no fill.", None),
 ("Tan tint pills", "Pills in a light tint of the accent.", None),
 ("One pill, divided", "Both items share one pill with a divider.", None),
 ("Solid dark pills", "High contrast: they read almost like buttons.", None),
 ("Labels above", "Small labels over each value, like a spec sheet.", f'<span class="hm"><small>Based in</small><span>{FLAG}Amsterdam, NL</span></span><span class="hm"><small>Designing @</small>{LINK}</span>'),
 ("Rule above", "A hairline separates the row from the intro.", None),
 ("Accent bar, stacked", "Two lines beside a tan bar.", None),
 ("Icon chips", "Flag and pin in round chips, text beside them.", f'<span class="hm"><i>{FLAG}</i>Amsterdam, NL</span><span class="hm"><i>{PIN}</i>Designing @{LINK}</span>'),
 ("Status dot", "A green “now” dot leads the current role.", f'<span class="hm"><i class="dot"></i>Designing @{LINK}</span><span class="hm">{FLAG}Amsterdam, NL</span>'),
 ("One quiet sentence", "Reads as a caption: smaller and greyer than the intro.", f'<span class="hm">Based in {FLAG} Amsterdam, NL, designing @{LINK}</span>'),
 ("Hospitable pink pill", "The role pill takes a tint of Hospitable’s pink.", None),
 ("Raised pills", "White pills with a soft shadow.", None),
 ("Square tags", "Small, squarer tags.", None),
]
cards = "\n".join(f'''  <article class="card v{i}">
    <h2><b>{i}</b> {n}</h2>
    <p class="lede">{LEDE}</p>
    <p class="hero-meta">{m or std}</p>
    <p class="note">{note}</p>
  </article>''' for i, (n, note, m) in enumerate(V, 1))
CSS = """
:root { --paper: #fff; --mist: #f6f6f4; --line: #e4e4df; --ink: #15171a; --ink-2: #5f636b; --signal: #b28550; --signal-soft: #f6efe4; --signal-ink: #7a5626; --body: "Roobert", "Hanken Grotesk", system-ui, sans-serif; }
* { box-sizing: border-box; } body { margin: 0; font: 400 16px/1.5 var(--body); color: var(--ink); background: var(--mist); }
a { color: inherit; } :focus-visible { outline: 2px solid var(--signal); outline-offset: 3px; border-radius: 6px; }
.page { max-width: 1240px; margin: 0 auto; padding: 28px 20px 64px; }
.back { display: inline-block; padding: 12px 0; color: var(--ink-2); text-decoration: none; } .back:hover { color: var(--ink); }
h1 { font: 650 clamp(28px, 3.4vw, 40px)/1.1 var(--body); letter-spacing: -.025em; margin: 6px 0 8px; }
.intro { color: var(--ink-2); max-width: 62ch; margin: 0 0 28px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 520px), 1fr)); gap: 16px; }
.card { background: var(--paper); border: 1px solid var(--line); border-radius: 18px; padding: 22px 24px 20px; display: flex; flex-direction: column; }
.card h2 { font: 600 15px/1.2 var(--body); margin: 0 0 18px; display: flex; align-items: center; gap: 10px; }
.card h2 b { display: grid; place-items: center; width: 26px; height: 26px; border-radius: 50%; background: var(--ink); color: #fff; font-size: 13px; font-weight: 600; }
.lede { font-size: 17px; line-height: 1.6; color: var(--ink-2); margin: 0; max-width: 40ch; }
.note { margin: auto 0 0; padding-top: 20px; font-size: 14px; color: var(--ink-2); }
/* shared */
.hero-meta { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; margin: 24px 0 0; font-size: 15px; font-weight: 500; color: var(--ink); }
.hm { display: inline-flex; align-items: center; gap: 9px; min-height: 40px; }
.flag { width: 24px; height: 16px; flex: none; } .pin { width: 16px; height: 16px; }
.hosp-link { display: inline-flex; align-items: center; padding-block: 11px; color: var(--ink); } .hosp { width: auto; height: 17px; color: inherit; }
/* 1 plain */ .v1 .hero-meta { gap: 6px 28px; font-size: 16px; }
/* 2 soft pills */ .v2 .hm { padding: 0 16px; border-radius: 999px; background: color-mix(in srgb, var(--ink) 6%, transparent); }
/* 3 outlined */ .v3 .hm { padding: 0 16px; border-radius: 999px; box-shadow: inset 0 0 0 1.5px var(--line); }
/* 4 tan tint */ .v4 .hm { padding: 0 16px; border-radius: 999px; background: var(--signal-soft); }
/* 5 one pill */ .v5 .hero-meta { display: inline-flex; align-self: flex-start; gap: 0; padding: 0 6px; border-radius: 999px; background: color-mix(in srgb, var(--ink) 6%, transparent); } .v5 .hm { padding: 0 14px; } .v5 .hm + .hm { box-shadow: -1.5px 0 0 color-mix(in srgb, var(--ink) 14%, transparent); } @media (max-width: 440px) { .v5 .hero-meta { border-radius: 22px; } .v5 .hm + .hm { box-shadow: none; } }
/* 6 dark */ .v6 .hm { padding: 0 16px; border-radius: 999px; background: var(--ink); color: #fff; } .v6 .hosp-link { color: #fff; }
/* 7 labels */ .v7 .hero-meta { gap: 14px 40px; align-items: flex-start; } .v7 .hm { flex-direction: column; align-items: flex-start; gap: 2px; font-size: 16px; } .v7 .hm > span { display: inline-flex; align-items: center; gap: 9px; min-height: 40px; } .v7 small { font-size: 13px; font-weight: 500; color: var(--ink-2); }
/* 8 rule */ .v8 .hero-meta { gap: 6px 28px; padding-top: 14px; border-top: 1px solid var(--line); max-width: 40ch; }
/* 9 bar */ .v9 .hero-meta { flex-direction: column; align-items: flex-start; gap: 0; padding-left: 16px; border-left: 3px solid var(--signal); }
/* 10 chips */ .v10 .hero-meta { gap: 10px 26px; } .v10 .hm i { display: grid; place-items: center; width: 40px; height: 40px; border-radius: 50%; background: color-mix(in srgb, var(--ink) 6%, transparent); color: var(--signal-ink); }
/* 11 dot */ .v11 .hero-meta { gap: 6px 28px; } .v11 .dot { width: 9px; height: 9px; border-radius: 50%; background: #1f9d55; box-shadow: 0 0 0 4px rgb(31 157 85 / .18); margin-right: 3px; }
/* 12 sentence */ .v12 .hero-meta { margin-top: 16px; font-size: 14px; font-weight: 400; color: var(--ink-2); } .v12 .hm { gap: 7px; flex-wrap: wrap; } .v12 .flag { width: 20px; height: 13.3px; } .v12 .hosp { height: 15px; }
/* 13 pink */ .v13 .hm { padding: 0 16px; border-radius: 999px; background: color-mix(in srgb, var(--ink) 6%, transparent); } .v13 .hm + .hm { background: #fdecf1; }
/* 14 raised */ .v14 .hm { padding: 0 16px; border-radius: 999px; background: #fff; box-shadow: 0 0 0 1px rgb(0 0 0 / .06), 0 6px 16px -6px rgb(0 0 0 / .18); }
/* 15 tags */ .v15 .hero-meta { gap: 8px; font-size: 14px; } .v15 .hm { padding: 0 12px; border-radius: 8px; background: var(--mist); box-shadow: inset 0 0 0 1px var(--line); } .v15 .hosp { height: 15px; }
"""
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, "index.html"), "w").write(f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="../assets/mj-logo.svg" type="image/svg+xml">
<title>Location and role: 15 treatments</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;650;700&display=swap">
<link rel="stylesheet" href="../fonts/fonts.css">
<style>{CSS}</style>
</head>
<body>
<main class="page">
  <a class="back" href="../site/index.html">← Home page</a>
  <h1>Location and role: 15 treatments</h1>
  <p class="intro">The two items that sit under the hero intro, shown with the intro above each so you can judge how separate they feel. Number 2 is on the home page now. <a href="heroes.html">See the shortlist (2, 13, 14) in the full hero →</a></p>
  <div class="grid">
{cards}
  </div>
</main>
</body>
</html>
""")

# ---- The shortlist in the full hero: copies of the home page with one treatment each, plus a page that stacks them.
SHORT = [("soft", "Soft pills", ""),   # the home page's current style
 ("pink", "Hospitable pink pill", """.hero-meta .hm + .hm { background: #fdecf1; }
:root[data-theme="dark"] .hero-meta .hm + .hm { background: rgb(237 60 106 / .2); }"""),
 ("raised", "Raised pills", """.hero-meta .hm { background: #fff; box-shadow: 0 0 0 1px rgb(0 0 0 / .06), 0 6px 16px -6px rgb(0 0 0 / .18); }
:root[data-theme="dark"] .hero-meta .hm { background: #1d1f24; box-shadow: 0 0 0 1px rgb(255 255 255 / .08), 0 8px 18px -8px rgb(0 0 0 / .8); }"""),
 ("outline-grey", "Outlined pills", """.hero-meta .hm { background: none; box-shadow: inset 0 0 0 1.5px var(--line); }"""),
 ("outline", "Outlined pills: grey and pink", """.hero-meta .hm { background: none; box-shadow: inset 0 0 0 1.5px var(--line); }
.hero-meta .hm + .hm { box-shadow: inset 0 0 0 1.5px #f6bfce; }
:root[data-theme="dark"] .hero-meta .hm + .hm { box-shadow: inset 0 0 0 1.5px rgb(237 60 106 / .5); }""")]
for key, name, css in SHORT:
    page = home.replace("<head>", '<head>\n<base href="../site/">', 1).replace("</head>", f"<style>{css}</style>\n</head>", 1)
    open(os.path.join(OUT, f"hero-{key}.html"), "w").write(page)
frames = "\n".join(f'''  <section class="opt">
    <h2>{name} <a href="hero-{key}.html">Open full page →</a></h2>
    <iframe src="hero-{key}.html" title="Home page hero with {name.lower()}" loading="lazy"></iframe>
  </section>''' for key, name, css in SHORT)
open(os.path.join(OUT, "heroes.html"), "w").write(f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="../assets/mj-logo.svg" type="image/svg+xml">
<title>Hero with the shortlisted pills</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;650;700&display=swap">
<link rel="stylesheet" href="../fonts/fonts.css">
<style>{CSS}
.page {{ max-width: 1520px; }}
.opt {{ margin-top: 28px; }}
.opt h2 {{ font: 600 18px/1.2 var(--body); margin: 0 0 12px; display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 16px; }}
.opt h2 a {{ font-weight: 500; font-size: 15px; color: var(--ink-2); padding: 12px 0; }}
.opt iframe {{ display: block; width: 100%; height: min(820px, 86vh); border: 1px solid var(--line); border-radius: 18px; background: #fff; }}
</style>
</head>
<body>
<main class="page">
  <a class="back" href="index.html">← All 15 treatments</a>
  <h1>Hero with the shortlisted pills</h1>
  <p class="intro">The real home page once per shortlisted treatment. Each frame is live: you can scroll it, switch to dark mode and click the face.</p>
{frames}
</main>
</body>
</html>
""")
print("built meta-lab")
