"""Roles lab: fifteen variations of the "Recent roles" list on the home page, with company logos.
Copy is the home page's own (from Matt's CV). The Carv tile is a placeholder (letter C) until Matt supplies the logo.
Output: redesigns/roles-lab/index.html   Re-run: python3 tools/build-roles-lab.py"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = os.path.join(ROOT, "redesigns", "roles-lab")
CV = "https://cdn.prod.website-files.com/63b35214bc1dc0317e22bd99/668ae1b79c5572bfad32e508_Matt_Jongbloet_CV_2024.pdf"
R = [  # logo, role, company, dates, short dates, line
 ("hospitable-mark.svg", "Senior Staff Product Designer", "Hospitable", "Now", "Now", "Helping hosts run their short-term rentals on autopilot."),
 ("carv-placeholder.svg", "Lead Product Designer", "Carv", "Feb 2024 — Mar 2025", "2024–25", "Helping recruiters cut admin and boost hires."),
 ("trellis/savvy-logo.png", "Staff Product Designer", "Trellis / Savvy.Insure", "Jan 2023 — Jan 2024", "2023–24", "$3.5MM in predicted gross annual revenue from 3 months of growth experiments."),
 ("homebot-logo.png", "Senior Product Designer", "Homebot", "Dec 2020 — Dec 2022", "2020–22", "Seven projects, research to dev-ready design, for ≈10 million users."),
]
items = "\n".join(f'''      <li class="r"><img class="lg" src="../assets/{lg}" alt=""><span class="role">{role}</span><span class="co">{co}</span><span class="when">{when}</span><span class="yr">{yr}</span><span class="did">{did}</span></li>''' for lg, role, co, when, yr, did in R)
V = [("Rows with logos", "The current list, with a logo tile in front of each role."),
 ("Stacked cards", "Each role in its own white card; the dates sit in a soft pill like the hero’s."),
 ("Two-by-two cards", "Four cards in a grid, logo on top."),
 ("Four across", "Compact: company first, then role and dates. No description."),
 ("Timeline", "A vertical line runs through the logos."),
 ("Dates on the left", "Dates in their own column, like a CV."),
 ("Current role featured", "Hospitable gets a large tan-tinted card; earlier roles sit beneath as smaller cards."),
 ("Company first", "The company name leads and the role title sits under it."),
 ("One card", "All four roles inside a single white card; “Now” gets a green dot."),
 ("Horizontal timeline", "Newest on the left, a line and dots across the top."),
 ("One line each", "The tightest version: logo, role, company and dates on one line."),
 ("Big years", "Large year ranges on the left give it rhythm."),
 ("Overlapping logo cards", "Echoes the project cards: a tinted band with the logo straddling its edge."),
 ("Pills", "Company and dates as soft pills under each role, matching the hero."),
 ("Dark panel", "The list on a dark panel for contrast with the rest of the page.")]
secs = "\n".join(f'''  <section class="var v{i}">
    <h2><b>{i}</b> {n}</h2>
    <p class="note">{note}</p>
    <div class="stage">
      <p class="eyebrow">Recent roles</p>
      <ul class="roles">
{items}
      </ul>
      <a class="cv" href="{CV}">Download full resume (PDF) →</a>
    </div>
  </section>''' for i, (n, note) in enumerate(V, 1))
PILL = "display: inline-flex; align-items: center; min-height: 32px; padding: 0 12px; border-radius: 999px; background: color-mix(in srgb, var(--ink) 6%, transparent); color: var(--ink); font-size: 14px; font-weight: 500;"
CARD = "background: var(--paper); border: 1px solid #ebebe8; border-radius: 20px;"
CSS = f"""
:root {{ --paper: #fff; --mist: #f6f6f4; --line: #e4e4df; --ink: #15171a; --ink-2: #5f636b; --signal: #b28550; --signal-soft: #f6efe4; --body: "Roobert", "Hanken Grotesk", system-ui, sans-serif; }}
* {{ box-sizing: border-box; }} body {{ margin: 0; font: 400 16px/1.5 var(--body); color: var(--ink); background: var(--mist); }}
img {{ display: block; }} a {{ color: inherit; }} :focus-visible {{ outline: 2px solid var(--signal); outline-offset: 3px; border-radius: 8px; }}
.page {{ max-width: 1080px; margin: 0 auto; padding: 28px 20px 80px; }}
.back {{ display: inline-block; padding: 12px 0; color: var(--ink-2); text-decoration: none; }} .back:hover {{ color: var(--ink); }}
h1 {{ font: 650 clamp(28px, 3.4vw, 40px)/1.1 var(--body); letter-spacing: -.025em; margin: 6px 0 8px; }}
.intro {{ color: var(--ink-2); max-width: 66ch; margin: 0; }}
.var {{ margin-top: 64px; }}
.var h2 {{ font: 600 18px/1.2 var(--body); margin: 0 0 6px; display: flex; align-items: center; gap: 10px; }}
.var h2 b {{ display: grid; place-items: center; width: 28px; height: 28px; border-radius: 50%; background: var(--ink); color: #fff; font-size: 13px; font-weight: 600; }}
.note {{ margin: 0 0 22px; color: var(--ink-2); font-size: 15px; }}
.eyebrow {{ margin: 0 0 14px; font-size: 13px; font-weight: 500; letter-spacing: .08em; text-transform: uppercase; color: var(--ink-2); }}
.cv {{ display: inline-block; margin-top: 8px; padding: 12px 0; color: var(--ink-2); font-size: 15px; text-underline-offset: 4px; }} .cv:hover {{ color: var(--ink); }}
/* ---- base list (= variation 1) ---- */
.roles {{ list-style: none; margin: 0; padding: 0; }}
.r {{ display: grid; grid-template-columns: 48px minmax(0, 1fr) auto; grid-template-areas: "lg role when" "lg co when" "lg did did"; column-gap: 16px; row-gap: 2px; padding: 20px 0; border-bottom: 1px solid var(--line); align-items: start; align-content: start; }}
.lg {{ grid-area: lg; width: 48px; height: 48px; border-radius: 12px; }}
.role {{ grid-area: role; font-weight: 600; font-size: 18px; line-height: 1.3; }}
.co {{ grid-area: co; color: var(--ink-2); }}
.when {{ grid-area: when; color: var(--ink-2); font-size: 15px; white-space: nowrap; justify-self: end; }}
.did {{ grid-area: did; color: var(--ink-2); margin-top: 6px; }}
.yr {{ display: none; }}
.v1 .roles {{ border-top: 1px solid var(--line); }}
/* 2 */ .v2 .r {{ {CARD} padding: 22px 24px; margin-bottom: 12px; }} .v2 .when {{ {PILL} }}
/* 3 */ .v3 .roles {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }} .v3 .r {{ {CARD} padding: 24px; grid-template-columns: auto 1fr; grid-template-areas: "lg when" "role role" "co co" "did did"; }} .v3 .lg {{ width: 56px; height: 56px; border-radius: 14px; margin-bottom: 14px; }} .v3 .when {{ {PILL} }}
/* 4 */ .v4 .roles {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; }} .v4 .r {{ {CARD} padding: 20px; grid-template-columns: 1fr; grid-template-areas: "lg" "co" "role" "when"; }} .v4 .lg {{ margin-bottom: 14px; }} .v4 .co {{ color: var(--ink); font-weight: 600; font-size: 17px; }} .v4 .role {{ font-weight: 400; font-size: 15px; color: var(--ink-2); }} .v4 .when {{ justify-self: start; margin-top: 10px; font-size: 14px; }} .v4 .did {{ display: none; }}
/* 5 */ .v5 .r {{ position: relative; border: 0; padding: 0 0 34px; column-gap: 20px; }} .v5 .r::before {{ content: ""; position: absolute; left: 23px; top: 0; bottom: 0; width: 2px; background: var(--line); }} .v5 .r:last-child::before {{ display: none; }} .v5 .r:last-child {{ padding-bottom: 8px; }} .v5 .lg {{ position: relative; box-shadow: 0 0 0 6px var(--mist); }}
/* 6 */ .v6 .roles {{ border-top: 1px solid var(--line); }} .v6 .r {{ grid-template-columns: 190px 44px minmax(0, 1fr); grid-template-areas: "when lg role" "when lg co" "when lg did"; }} .v6 .when {{ justify-self: start; padding-top: 3px; }} .v6 .lg {{ width: 44px; height: 44px; }}
/* 7 */ .v7 .roles {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }} .v7 .r {{ {CARD} padding: 22px; grid-template-columns: 1fr; grid-template-areas: "lg" "role" "co" "when"; }} .v7 .r .lg {{ margin-bottom: 14px; }} .v7 .r .when {{ justify-self: start; margin-top: 10px; font-size: 14px; }} .v7 .r .did {{ display: none; }}
.v7 .r:first-child {{ grid-column: 1 / -1; background: var(--signal-soft); border-color: transparent; padding: 30px; grid-template-columns: 72px minmax(0, 1fr) auto; grid-template-areas: "lg role when" "lg co when" "lg did did"; column-gap: 22px; }} .v7 .r:first-child .lg {{ width: 72px; height: 72px; border-radius: 18px; margin: 0; }} .v7 .r:first-child .role {{ font-size: 24px; letter-spacing: -.02em; }} .v7 .r:first-child .did {{ display: block; color: var(--ink); }} .v7 .r:first-child .when {{ {PILL} background: #fff; margin: 0; justify-self: end; }}
/* 8 */ .v8 .roles {{ border-top: 1px solid var(--line); }} .v8 .r {{ grid-template-areas: "lg co when" "lg role when" "lg did did"; }} .v8 .co {{ color: var(--ink); font-weight: 600; font-size: 20px; letter-spacing: -.01em; line-height: 1.3; }} .v8 .role {{ font-weight: 400; font-size: 16px; color: var(--ink-2); }}
/* 9 */ .v9 .roles {{ {CARD} border-radius: 24px; padding: 6px 28px; }} .v9 .r:last-child {{ border-bottom: 0; }} .v9 .r:first-child .when {{ {PILL} gap: 8px; }} .v9 .r:first-child .when::before {{ content: ""; width: 8px; height: 8px; border-radius: 50%; background: #1f9d55; box-shadow: 0 0 0 4px rgb(31 157 85 / .18); }}
/* 10 */ .v10 .roles {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 24px; border-top: 2px solid var(--line); }} .v10 .r {{ position: relative; border: 0; padding: 26px 0 0; grid-template-columns: 1fr; grid-template-areas: "yr" "lg" "role" "co" "did"; }} .v10 .r::before {{ content: ""; position: absolute; left: 0; top: -7px; width: 12px; height: 12px; border-radius: 50%; background: var(--ink); box-shadow: 0 0 0 4px var(--mist); }} .v10 .r:first-child::before {{ background: var(--signal); }}
.v10 .yr {{ display: block; grid-area: yr; font-size: 15px; font-weight: 500; color: var(--ink-2); }} .v10 .when {{ display: none; }} .v10 .lg {{ margin: 12px 0 14px; }} .v10 .role {{ font-size: 17px; }} .v10 .did {{ font-size: 15px; }}
/* 11 */ .v11 .roles {{ border-top: 1px solid var(--line); }} .v11 .r {{ grid-template-columns: 36px auto minmax(0, 1fr) auto; grid-template-areas: "lg role co when"; align-items: center; padding: 14px 0; column-gap: 14px; }} .v11 .lg {{ width: 36px; height: 36px; border-radius: 10px; }} .v11 .role {{ font-size: 17px; }} .v11 .did {{ display: none; }}
/* 12 */ .v12 .roles {{ border-top: 1px solid var(--line); }} .v12 .r {{ grid-template-columns: 230px 48px minmax(0, 1fr); grid-template-areas: "yr lg role" "yr lg co" "yr lg did"; padding: 26px 0; }} .v12 .yr {{ display: block; grid-area: yr; font: 600 40px/1.1 var(--body); letter-spacing: -.035em; }} .v12 .r:first-child .yr {{ color: var(--signal); }} .v12 .when {{ display: none; }}
/* 13 */ .v13 .roles {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }} .v13 .r {{ {CARD} display: block; padding: 0 26px 26px; overflow: hidden; }} .v13 .r::before {{ content: ""; display: block; height: 68px; margin: 0 -26px; background: #ececea; }} .v13 .r > span {{ display: block; }} .v13 .lg {{ position: relative; width: 56px; height: 56px; border-radius: 14px; margin: -28px 0 14px; box-shadow: 0 0 0 4px var(--paper); }} .v13 .r > .when {{ {PILL} display: inline-flex; margin-top: 14px; }} .v13 .r > .yr {{ display: none; }}
/* 14 */ .v14 .roles {{ border-top: 1px solid var(--line); }} .v14 .r {{ display: flex; flex-wrap: wrap; align-items: center; gap: 10px 8px; padding: 22px 0; }} .v14 .role {{ order: -1; flex: 0 0 100%; font-size: 20px; letter-spacing: -.01em; }} .v14 .lg {{ width: 22px; height: 22px; border-radius: 6px; margin: 0 0 0 8px; position: relative; z-index: 1; }} .v14 .co {{ {PILL} min-height: 36px; padding-left: 38px; margin-left: -38px; }} .v14 .when {{ {PILL} min-height: 36px; }} .v14 .did {{ flex: 0 0 100%; margin: 0; }}
/* 15 */ .v15 .roles {{ background: var(--ink); border-radius: 24px; padding: 8px 30px; color: #fff; }} .v15 .r {{ border-bottom-color: rgb(255 255 255 / .12); }} .v15 .r:last-child {{ border-bottom: 0; }} .v15 .co, .v15 .did {{ color: #b9bdc5; }} .v15 .when {{ {PILL} background: rgb(255 255 255 / .1); color: #fff; }}
@media (max-width: 760px) {{
  .r, .v6 .r, .v8 .r, .v12 .r, .v2 .r {{ grid-template-columns: 44px minmax(0, 1fr); grid-template-areas: "lg role" "lg co" "lg when" "did did"; }}
  .when {{ justify-self: start; margin-top: 4px; }} .lg {{ width: 44px; height: 44px; }}
  .v3 .roles, .v7 .roles, .v13 .roles {{ grid-template-columns: 1fr; }} .v4 .roles, .v10 .roles {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
  .v7 .r:first-child {{ grid-template-columns: 1fr; grid-template-areas: "lg" "role" "co" "did" "when"; padding: 24px; }} .v7 .r:first-child .lg {{ margin-bottom: 14px; }} .v7 .r:first-child .when {{ justify-self: start; margin-top: 12px; }}
  .v10 .r, .v4 .r, .v7 .r {{ grid-template-columns: 1fr; }} .v10 .r {{ grid-template-areas: "yr" "lg" "role" "co" "did"; }} .v4 .r {{ grid-template-areas: "lg" "co" "role" "when"; }} .v7 .r {{ grid-template-areas: "lg" "role" "co" "when"; }}
  .v3 .r {{ grid-template-columns: auto 1fr; grid-template-areas: "lg when" "role role" "co co" "did did"; }} .v3 .when {{ justify-self: end; }}
  .v11 .r {{ grid-template-columns: 36px minmax(0, 1fr); grid-template-areas: "lg role" "lg co" "lg when"; }}
  .v12 .r {{ grid-template-areas: "yr yr" "lg role" "lg co" "did did"; }} .v12 .yr {{ font-size: 30px; margin-bottom: 10px; }}
  .v9 .roles, .v15 .roles {{ padding-inline: 20px; }}
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
  <p class="intro">The “Recent roles” list from the home page, now with company logos, in the same language as the hero pills and project cards. The Carv tile is a placeholder letter until the real logo is added.</p>
{secs}
</main>
</body>
</html>
""")
print("built roles-lab")
