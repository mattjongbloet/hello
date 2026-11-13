"""Roles lab: fifteen variations of the "Recent roles" list on the home page, with company logos.
Copy is the home page's own (from Matt's CV). Logos: Hospitable mark, Carv (Matt's SVG), Savvy and Homebot tiles.
Output: redesigns/roles-lab/index.html   Re-run: python3 tools/build-roles-lab.py"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = os.path.join(ROOT, "redesigns", "roles-lab")
CV = "https://cdn.prod.website-files.com/63b35214bc1dc0317e22bd99/668ae1b79c5572bfad32e508_Matt_Jongbloet_CV_2024.pdf"
R = [  # logo, role, company, dates, short dates, line
 ("hospitable-mark.svg", "Senior Staff Product Designer", "Hospitable", "Now", "Now", "Helping hosts run their short-term rentals on autopilot."),
 ("carv-logo.svg", "Lead Product Designer", "Carv", "Feb 2024 — Mar 2025", "2024–25", "Helping recruiters cut admin and boost hires."),
 ("trellis/savvy-logo.png", "Staff Product Designer", "Trellis / Savvy.Insure", "Jan 2023 — Jan 2024", "2023–24", "$3.5MM in predicted gross annual revenue from 3 months of growth experiments."),
 ("homebot-logo.png", "Senior Product Designer", "Homebot", "Dec 2020 — Dec 2022", "2020–22", "Seven projects, research to dev-ready design, for ≈10 million users."),
]
items = "\n".join(f'''      <li class="r"><img class="lg" src="../assets/{lg}" alt="{co} logo"><span class="role">{role}</span><span class="co">{co}</span><span class="when">{when}</span><span class="yr">{yr}</span><span class="did">{did}</span></li>''' for lg, role, co, when, yr, did in R)
V = [("Rows with logos", "The current list, with a logo tile in front of each role."),
 ("Stacked cards", "Each role in its own soft card; the dates sit in a pill like the hero’s."),
 ("Two-by-two cards", "Four small cards, logo on top, years in a pill. No description."),
 ("Two columns, company first", "No cards: logo, company, role and years in a two-column grid. No description."),
 ("Timeline", "A vertical line runs through the logos."),
 ("Years on the left", "Years in their own narrow column, like a CV."),
 ("Current role featured", "Hospitable gets a tan-tinted card; earlier roles sit beneath as three small cards."),
 ("Company first", "The company name leads and the role title sits under it."),
 ("One card", "All four roles inside a single soft card; “Now” gets a green dot."),
 ("Horizontal timeline", "Newest on the left, a line and dots across the top. Company, then role."),
 ("One line each", "The tightest version: logo, role and dates on one line (the logo stands in for the company name)."),
 ("Big years", "Larger year ranges on the left give it rhythm."),
 ("Overlapping logo cards", "Echoes the project cards: a tinted band with the logo straddling its edge."),
 ("Pills", "Company and dates as soft pills under each role, matching the hero."),
 ("Dark panel", "The list on a dark panel for contrast with the rest of the section.")]
import re
home = open(os.path.join(ROOT, "redesigns", "site", "index.html")).read()
ABOUT_P = re.search(r'<p class="eyebrow">About</p>\s*<h2[^>]*>(.*?)</h2>\s*<p>(.*?)</p>', home, re.S)
ABOUT = f"""<div class="about">
        <p class="eyebrow">About</p>
        <h3>{ABOUT_P.group(1)}</h3>
        <p>{ABOUT_P.group(2)}</p>
        <a class="btn" href="../site/about.html">Read my story</a>
      </div>"""
secs = "\n".join(f"""  <section class="var v{i}">
    <h2><b>{i}</b> {n}</h2>
    <p class="note">{note}</p>
    <div class="stage">
      {ABOUT}
      <div class="col">
        <p class="eyebrow">Recent roles</p>
        <ul class="roles">
{items}
        </ul>
        <a class="cv" href="{CV}">Download full resume (PDF) →</a>
      </div>
    </div>
  </section>""" for i, (n, note) in enumerate(V, 1))
PILL = "display: inline-flex; align-items: center; min-height: 30px; padding: 0 11px; border-radius: 999px; background: color-mix(in srgb, var(--ink) 6%, transparent); color: var(--ink); font-size: 13px; font-weight: 500; white-space: nowrap;"
CARD = "background: var(--mist); border-radius: 18px;"
CSS = f"""
:root {{ --paper: #fff; --mist: #f6f6f4; --line: #e4e4df; --ink: #15171a; --ink-2: #5f636b; --signal: #b28550; --signal-soft: #f6efe4; --body: "Roobert", "Hanken Grotesk", system-ui, sans-serif; }}
* {{ box-sizing: border-box; }} body {{ margin: 0; font: 400 16px/1.5 var(--body); color: var(--ink); background: var(--mist); }}
img {{ display: block; }} a {{ color: inherit; }} :focus-visible {{ outline: 2px solid var(--signal); outline-offset: 3px; border-radius: 8px; }}
.page {{ max-width: 1120px; margin: 0 auto; padding: 28px 20px 80px; }}
.back {{ display: inline-block; padding: 12px 0; color: var(--ink-2); text-decoration: none; }} .back:hover {{ color: var(--ink); }}
h1 {{ font: 650 clamp(28px, 3.4vw, 40px)/1.1 var(--body); letter-spacing: -.025em; margin: 6px 0 8px; }}
.intro {{ color: var(--ink-2); max-width: 66ch; margin: 0; }}
.var {{ margin-top: 56px; }}
.var h2 {{ font: 600 18px/1.2 var(--body); margin: 0 0 6px; display: flex; align-items: center; gap: 10px; }}
.var h2 b {{ display: grid; place-items: center; width: 28px; height: 28px; border-radius: 50%; background: var(--ink); color: #fff; font-size: 13px; font-weight: 600; }}
.note {{ margin: 0 0 18px; color: var(--ink-2); font-size: 15px; }}
/* The home page's About section: text on the left, Recent roles in the right half. */
.stage {{ background: var(--paper); border-radius: 24px; padding: 52px 48px; display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 64px; align-items: start; }}
.eyebrow {{ margin: 0 0 16px; font-size: 13px; font-weight: 500; letter-spacing: .08em; text-transform: uppercase; color: var(--ink-2); }}
.about h3 {{ font: 650 clamp(26px, 2.9vw, 36px)/1.12 var(--body); letter-spacing: -.03em; margin: 0 0 20px; }}
.about p:not(.eyebrow) {{ color: var(--ink-2); font-size: 17px; line-height: 1.65; margin: 0 0 26px; }} .about strong {{ color: var(--ink); font-weight: 600; }}
.btn {{ display: inline-flex; align-items: center; min-height: 48px; padding: 0 22px; border-radius: 999px; box-shadow: inset 0 0 0 1.5px var(--line); text-decoration: none; font-weight: 600; font-size: 15px; }} .btn:hover {{ box-shadow: inset 0 0 0 1.5px var(--ink); }}
.cv {{ display: inline-block; margin-top: 8px; padding: 12px 0; color: var(--ink-2); font-size: 15px; text-underline-offset: 4px; }} .cv:hover {{ color: var(--ink); }}
@media (max-width: 860px) {{ .stage {{ grid-template-columns: 1fr; gap: 40px; padding: 32px 22px; }} }}
/* ---- base list (= variation 1): sized for the half column ---- */
.roles {{ list-style: none; margin: 0; padding: 0; }}
.r {{ display: grid; grid-template-columns: 44px minmax(0, 1fr) auto; grid-template-areas: "lg role when" "lg co when" "lg did did"; column-gap: 14px; row-gap: 1px; padding: 18px 0; border-bottom: 1px solid var(--line); align-items: start; align-content: start; }}
.lg {{ grid-area: lg; width: 44px; height: 44px; border-radius: 11px; }}
.role {{ grid-area: role; font-weight: 600; font-size: 16px; line-height: 1.35; }}
.co {{ grid-area: co; color: var(--ink-2); font-size: 15px; }}
.when {{ grid-area: when; color: var(--ink-2); font-size: 13px; line-height: 1.7; white-space: nowrap; justify-self: end; }}
.did {{ grid-area: did; color: var(--ink-2); font-size: 15px; line-height: 1.45; margin-top: 6px; }}
.yr {{ display: none; }}
.v1 .roles, .v6 .roles, .v8 .roles, .v11 .roles, .v12 .roles, .v14 .roles {{ border-top: 1px solid var(--line); }}
/* 2 */ .v2 .r {{ {CARD} border: 0; padding: 18px; margin-bottom: 10px; grid-template-columns: 44px minmax(0, 1fr) auto; grid-template-areas: "lg role role" "lg co when" "lg did did"; }} .v2 .when {{ {PILL} align-self: center; }}
/* 3 */ .v3 .roles {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }} .v3 .r {{ {CARD} border: 0; padding: 18px; grid-template-columns: auto 1fr; grid-template-areas: "lg yr" "role role" "co co"; }} .v3 .lg {{ margin-bottom: 14px; }} .v3 .yr {{ {PILL} grid-area: yr; justify-self: end; }} .v3 .when, .v3 .did {{ display: none; }}
/* 4 */ .v4 .roles {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 26px 20px; }} .v4 .r {{ border: 0; padding: 0; grid-template-columns: 40px minmax(0, 1fr); grid-template-areas: "lg co" "lg role" "lg yr"; column-gap: 12px; }} .v4 .lg {{ width: 40px; height: 40px; border-radius: 10px; }} .v4 .co {{ color: var(--ink); font-weight: 600; font-size: 16px; }} .v4 .role {{ font-weight: 400; font-size: 14px; color: var(--ink-2); }} .v4 .yr {{ display: block; grid-area: yr; font-size: 13px; color: var(--ink-2); margin-top: 2px; }} .v4 .when, .v4 .did {{ display: none; }}
/* 5 */ .v5 .r {{ position: relative; border: 0; padding: 0 0 28px; }} .v5 .r::before {{ content: ""; position: absolute; left: 21px; top: 0; bottom: 0; width: 2px; background: var(--line); }} .v5 .r:last-child::before {{ display: none; }} .v5 .r:last-child {{ padding-bottom: 6px; }} .v5 .lg {{ position: relative; box-shadow: 0 0 0 5px var(--paper); }}
/* 6 */ .v6 .r {{ grid-template-columns: 62px 40px minmax(0, 1fr); grid-template-areas: "yr lg role" "yr lg co" "yr lg did"; }} .v6 .yr {{ display: block; grid-area: yr; font-size: 14px; color: var(--ink-2); padding-top: 2px; white-space: nowrap; }} .v6 .lg {{ width: 40px; height: 40px; border-radius: 10px; }} .v6 .when {{ display: none; }}
/* 7 */ .v7 .roles {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; }} .v7 .r {{ {CARD} border: 0; padding: 16px; grid-template-columns: 1fr; grid-template-areas: "lg" "co" "role" "yr"; }} .v7 .r .lg {{ width: 36px; height: 36px; border-radius: 9px; margin-bottom: 12px; }} .v7 .r .co {{ color: var(--ink); font-weight: 600; font-size: 15px; line-height: 1.3; }} .v7 .r .role {{ font-weight: 400; font-size: 13px; color: var(--ink-2); margin-top: 2px; }} .v7 .r .yr {{ display: block; grid-area: yr; font-size: 13px; color: var(--ink-2); margin-top: 8px; }} .v7 .r .when, .v7 .r .did {{ display: none; }}
.v7 .r:first-child {{ grid-column: 1 / -1; background: var(--signal-soft); padding: 22px; grid-template-columns: 52px minmax(0, 1fr) auto; grid-template-areas: "lg role yr" "lg co yr" "did did did"; column-gap: 16px; }} .v7 .r:first-child .lg {{ width: 52px; height: 52px; border-radius: 13px; margin: 0; }} .v7 .r:first-child .role {{ font-size: 18px; font-weight: 600; color: var(--ink); margin: 0; }} .v7 .r:first-child .co {{ font-weight: 400; color: var(--ink-2); }} .v7 .r:first-child .did {{ display: block; color: var(--ink); margin-top: 14px; }} .v7 .r:first-child .yr {{ {PILL} background: #fff; margin: 0; }}
/* 8 */ .v8 .r {{ grid-template-areas: "lg co when" "lg role when" "lg did did"; }} .v8 .co {{ color: var(--ink); font-weight: 600; font-size: 18px; letter-spacing: -.01em; line-height: 1.3; }} .v8 .role {{ font-weight: 400; font-size: 15px; color: var(--ink-2); }}
/* 9 */ .v9 .roles {{ {CARD} border-radius: 22px; padding: 4px 20px; }} .v9 .r {{ grid-template-areas: "lg role role" "lg co when" "lg did did"; }} .v9 .r:last-child {{ border-bottom: 0; }} .v9 .r:first-child .when {{ {PILL} background: #fff; gap: 7px; }} .v9 .r:first-child .when::before {{ content: ""; width: 8px; height: 8px; border-radius: 50%; background: #1f9d55; box-shadow: 0 0 0 3px rgb(31 157 85 / .18); }}
/* 10 */ .v10 .roles {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; border-top: 2px solid var(--line); }} .v10 .r {{ position: relative; border: 0; padding: 22px 0 0; grid-template-columns: 1fr; grid-template-areas: "yr" "lg" "co" "role"; }} .v10 .r::before {{ content: ""; position: absolute; left: 0; top: -7px; width: 12px; height: 12px; border-radius: 50%; background: var(--ink); box-shadow: 0 0 0 4px var(--paper); }} .v10 .r:first-child::before {{ background: var(--signal); }}
.v10 .yr {{ display: block; grid-area: yr; font-size: 13px; font-weight: 500; color: var(--ink-2); }} .v10 .when, .v10 .did {{ display: none; }} .v10 .lg {{ width: 40px; height: 40px; border-radius: 10px; margin: 10px 0 12px; }} .v10 .co {{ color: var(--ink); font-weight: 600; font-size: 14px; line-height: 1.3; }} .v10 .role {{ font-weight: 400; font-size: 13px; color: var(--ink-2); margin-top: 3px; }}
/* 11 */ .v11 .r {{ grid-template-columns: 32px minmax(0, 1fr) auto; grid-template-areas: "lg role when"; align-items: center; padding: 13px 0; column-gap: 12px; }} .v11 .lg {{ width: 32px; height: 32px; border-radius: 8px; }} .v11 .did {{ display: none; }} .v11 .co {{ display: none; }}   /* the logo's alt text carries the company name */
/* 12 */ .v12 .r {{ grid-template-columns: 118px 40px minmax(0, 1fr); grid-template-areas: "yr lg role" "yr lg co" "yr lg did"; padding: 22px 0; column-gap: 12px; }} .v12 .lg {{ width: 40px; height: 40px; border-radius: 10px; }} .v12 .yr {{ display: block; grid-area: yr; font: 600 27px/1.2 var(--body); letter-spacing: -.035em; white-space: nowrap; }} .v12 .r:first-child .yr {{ color: var(--signal); }} .v12 .when {{ display: none; }}
/* 13 */ .v13 .roles {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }} .v13 .r {{ {CARD} border: 1px solid #ebebe8; background: var(--paper); display: block; padding: 0 18px 18px; overflow: hidden; }} .v13 .r::before {{ content: ""; display: block; height: 52px; margin: 0 -18px; background: #ececea; }} .v13 .r > span {{ display: block; }} .v13 .lg {{ position: relative; width: 48px; height: 48px; border-radius: 12px; margin: -24px 0 12px; box-shadow: 0 0 0 4px var(--paper); }} .v13 .r > .yr {{ {PILL} display: inline-flex; margin-top: 12px; }} .v13 .r > .when, .v13 .r > .did {{ display: none; }}
/* 14 */ .v14 .r {{ display: flex; flex-wrap: wrap; align-items: center; gap: 8px 6px; padding: 18px 0; }} .v14 .role {{ order: -1; flex: 0 0 100%; font-size: 17px; }} .v14 .lg {{ width: 20px; height: 20px; border-radius: 5px; margin: 0 0 0 7px; position: relative; z-index: 1; }} .v14 .co {{ {PILL} min-height: 34px; padding-left: 34px; margin-left: -33px; }} .v14 .when {{ {PILL} min-height: 34px; }} .v14 .did {{ flex: 0 0 100%; margin: 2px 0 0; }}
/* 15 */ .v15 .roles {{ background: var(--ink); border-radius: 22px; padding: 4px 20px; color: #fff; }} .v15 .r {{ border-bottom-color: rgb(255 255 255 / .12); grid-template-areas: "lg role role" "lg co when" "lg did did"; }} .v15 .r:last-child {{ border-bottom: 0; }} .v15 .co, .v15 .did {{ color: #b9bdc5; }} .v15 .when {{ {PILL} background: rgb(255 255 255 / .1); color: #fff; }}
@media (max-width: 420px) {{
  .v1 .r, .v5 .r, .v8 .r {{ grid-template-columns: 44px minmax(0, 1fr); grid-template-areas: "lg role" "lg co" "lg when" "did did"; }} .v8 .r {{ grid-template-areas: "lg co" "lg role" "lg when" "did did"; }} .v1 .when, .v5 .when, .v8 .when {{ justify-self: start; }}
  .v2 .r, .v9 .r, .v15 .r {{ grid-template-columns: 44px minmax(0, 1fr); grid-template-areas: "lg role" "lg co" "lg when" "did did"; }} .v2 .when, .v9 .when, .v15 .when {{ justify-self: start; margin-top: 6px; }}
  .v7 .roles {{ grid-template-columns: 1fr; }} .v10 .roles {{ grid-template-columns: repeat(2, minmax(0, 1fr)); row-gap: 28px; }}
  .v12 .r {{ grid-template-columns: 40px minmax(0, 1fr); grid-template-areas: "yr yr" "lg role" "lg co" "did did"; }} .v12 .yr {{ margin-bottom: 8px; }}
}}
"""
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, "index.html"), "w").write(f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="../assets/mj-logo.svg" type="image/svg+xml">
<title>Recent roles: 15 variations</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;650;700&display=swap">
<link rel="stylesheet" href="../fonts/fonts.css">
<style>{CSS}</style>
</head>
<body>
<main class="page">
  <a class="back" href="../site/index.html">← Home page</a>
  <h1>Recent roles: 15 variations</h1>
  <p class="intro">The “Recent roles” list with company logos, shown where it lives on the home page: in the right half of the About section.</p>
{secs}
</main>
</body>
</html>
""")
print("built roles-lab")
