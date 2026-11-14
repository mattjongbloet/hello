"""Case-study header lab: 15 treatments of the top of a case study (Trellis as the example). Every one has
"Back to work" on the left and "Next: <next case study>" on the right (Matt's request, after a reference portfolio),
then the title, intro and the five facts (company, role, team, timeframe, surface), arranged differently.
Output: redesigns/cs-head-lab/index.html   Re-run: python3 tools/build-cs-head-lab.py"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = os.path.join(ROOT, "redesigns", "cs-head-lab")
TITLE = "Finding $3.5MM in three months of growth experiments"
DEK = "Savvy hadn’t had a designer for two years. In three months, a small growth team and I ran around 15 experiments across the homepage and the car insurance quote flows, adding up to $3.5MM in predicted gross annual revenue."
NEXT = ("Private Mortgage Insurance", "../case-studies/pmi.html")
TEAM = "".join(f'<a class="mate" href="https://www.linkedin.com/in/{h}/" title="{n}" aria-label="{n} on LinkedIn"><img src="../assets/team/{h}.jpg" alt=""></a>' for n, h in [("Drew Bolles", "drew-bolles"), ("Chuong Nguyen", "chuongtnguyen"), ("Alexey Komissarouk", "alexeymk")])
FACTS = [("Company", "Trellis / Savvy.Insure"), ("My role", "Staff Product Designer, Growth"), ("Team", f'<span class="team">{TEAM}</span>'), ("Timeframe", "3 months, 2023"), ("Surface", "Homepage and car insurance quote flows")]
ARROW_L = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3 5 8l5 5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW_R = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="m6 3 5 5-5 5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
LOGO = '<img class="co-logo" src="../assets/trellis/savvy-logo.png" alt="">'

def topnav(style=""):
    return (f'<nav class="cnav {style}" aria-label="Case study"><a class="back" href="../site/index.html#work">{ARROW_L}<span>Back to work</span></a>'
            f'<a class="next" href="{NEXT[1]}"><span><small>Next</small> {NEXT[0]}</span>{ARROW_R}</a></nav>')
facts = lambda cls="": f'<dl class="facts {cls}">' + "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in FACTS) + "</dl>"
h1, dek = f"<h1>{TITLE}</h1>", f'<p class="dek">{DEK}</p>'

V = [
 ("Current, with the new top bar", "Today’s layout: title and intro left-aligned, facts in a full-width row. Shown so you can compare.", "",
  f'{topnav()}{h1}{dek}{facts()}'),
 ("Split: title left, intro right", "The title takes the left column, the intro sits in the right column aligned to the title’s last line. The facts row runs full width underneath, so the right side is never empty.", "split",
  f'{topnav()}<div class="row"><div class="c-t">{h1}</div><div class="c-d">{dek}</div></div>{facts()}'),
 ("Split: facts under the intro", "Title on the left; the intro and the facts stack in the right column, with the facts in two columns.", "split2",
  f'{topnav()}<div class="row"><div class="c-t">{h1}</div><div class="c-d">{dek}{facts("two")}</div></div>'),
 ("Centred, facts with dividers", "Title and intro centred; the five facts become equal centred columns with thin dividers, so the row reads as part of the centred block.", "centre",
  f'{topnav()}<div class="mid">{h1}{dek}</div>{facts("div")}'),
 ("Centred, facts in a card", "Centred title and intro; the facts sit in a soft rounded card with dividers.", "centre",
  f'{topnav()}<div class="mid">{h1}{dek}</div>{facts("div card")}'),
 ("Facts as a sidebar", "Title and intro on the left; the facts run down a narrow right column, top-aligned with the title, filling the gap.", "side",
  f'{topnav()}<div class="row"><div class="c-t">{h1}{dek}</div>{facts("stack")}</div>'),
 ("Facts in a tinted panel", "Like the sidebar, but the facts sit in a tinted panel on the right.", "side",
  f'{topnav()}<div class="row"><div class="c-t">{h1}{dek}</div>{facts("stack panel")}</div>'),
 ("Full-width headline", "A larger headline that runs the full width, so there’s no gap; the intro sits under it, left-aligned at reading width, then the facts row.", "wide",
  f'{topnav()}{h1}{dek}{facts()}'),
 ("Intro aligned to the facts", "Title on the left; the intro starts at the second fact column, so the text and the row underneath share one grid.", "grid",
  f'{topnav()}{h1}<div class="g5">{dek}</div>{facts()}'),
 ("Tinted band", "Title, intro and facts inside a full-width tinted band; the facts sit along the band’s bottom edge.", "band",
  f'{topnav()}<div class="bandbox">{h1}{dek}{facts()}</div>'),
 ("Logo on the right", "The Savvy logo tile fills the right of the title area, so the left-aligned text feels anchored.", "logo",
  f'{topnav()}<div class="row"><div class="c-t">{h1}{dek}</div><div class="c-l">{LOGO}</div></div>{facts()}'),
 ("Compact facts line", "Title and intro left; the facts collapse into one compact line of label–value pairs with thin dividers.", "",
  f'{topnav()}{h1}{dek}{facts("inline")}'),
 ("Centred, compact facts", "Everything centred, with the facts as a short centred line of pills.", "centre",
  f'{topnav()}<div class="mid">{h1}{dek}</div>{facts("pills")}'),
 ("Top bar as pills", "The current layout, with Back and Next as soft pill buttons; the facts move up beside the intro on wide screens.", "split",
  f'{topnav("pillnav")}{h1}<div class="row"><div class="c-d0">{dek}</div>{facts("two")}</div>'),
 ("Title with an eyebrow, facts row framed", "A small company eyebrow above the title; the facts row gets a top and bottom rule, like a spec sheet.", "",
  f'{topnav()}<p class="eye">{LOGO}Trellis / Savvy.Insure · Growth</p>{h1}{dek}{facts("ruled")}'),
]
secs = "\n".join(f'''  <section class="var">
    <h2><b>{i}</b> {n}</h2>
    <p class="note">{note}</p>
    <div class="frame"><header class="hd {cls}">{html}</header></div>
  </section>''' for i, (n, note, cls, html) in enumerate(V, 1))
CSS = """
:root { --paper: #fff; --mist: #f6f6f4; --line: #e4e4df; --ink: #15171a; --ink-2: #5f636b; --signal: #b28550; --body: "Roobert", "Hanken Grotesk", system-ui, sans-serif; }
* { box-sizing: border-box; } body { margin: 0; font: 400 16px/1.5 var(--body); color: var(--ink); background: var(--mist); }
img { display: block; } a { color: inherit; } :focus-visible { outline: 2px solid var(--signal); outline-offset: 3px; border-radius: 8px; }
.page { max-width: 1320px; margin: 0 auto; padding: 28px 20px 80px; }
.back-lab { display: inline-block; padding: 12px 0; color: var(--ink-2); text-decoration: none; }
.page > h1 { font: 650 clamp(28px, 3.4vw, 40px)/1.1 var(--body); letter-spacing: -.025em; margin: 6px 0 8px; }
.intro { color: var(--ink-2); max-width: 70ch; margin: 0; }
.var { margin-top: 56px; } .var h2 { font: 600 18px/1.2 var(--body); margin: 0 0 6px; display: flex; align-items: center; gap: 10px; }
.var h2 b { display: grid; place-items: center; width: 28px; height: 28px; border-radius: 50%; background: var(--ink); color: #fff; font-size: 13px; }
.var .note { margin: 0 0 16px; color: var(--ink-2); font-size: 15px; max-width: 80ch; }
.frame { background: var(--paper); border: 1px solid #ebebe8; border-radius: 20px; padding: 0 clamp(20px, 4vw, 56px) clamp(36px, 4vw, 56px); overflow: hidden; }
/* the header itself (site type sizes) */
.hd h1 { font: 650 clamp(32px, 4.3vw, 54px)/1.06 var(--body); letter-spacing: -.035em; margin: 0; max-width: 19ch; }
.hd .dek { font-size: clamp(16px, 1.4vw, 19px); line-height: 1.55; color: var(--ink-2); max-width: 54ch; margin: 22px 0 0; }
.cnav { display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 22px 0 40px; font-size: 15px; }
.cnav a { display: inline-flex; align-items: center; gap: 8px; min-height: 44px; color: var(--ink-2); text-decoration: none; }
.cnav a:hover { color: var(--ink); } .cnav svg { width: 16px; height: 16px; flex: none; }
.cnav .next span { text-align: right; } .cnav .next small { color: var(--ink-2); font-size: 15px; margin-right: 4px; } .cnav .next { color: var(--ink); font-weight: 500; }
.cnav.pillnav a { padding: 0 16px; border-radius: 999px; background: color-mix(in srgb, var(--ink) 6%, transparent); color: var(--ink); }
.facts { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 18px 24px; margin: 40px 0 0; padding-top: 22px; border-top: 1px solid var(--line); }
.facts div { min-width: 0; } .facts dt { font-size: 12px; font-weight: 500; letter-spacing: .08em; text-transform: uppercase; color: var(--ink-2); margin-bottom: 6px; } .facts dd { margin: 0; font-size: 15px; line-height: 1.4; }
.team { display: flex; gap: 6px; } .mate img { width: 38px; height: 38px; border-radius: 50%; object-fit: cover; }
.co-logo { width: 72px; height: 72px; border-radius: 18px; }
/* 2 split / 3 / 14 */
.row { display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr); gap: 24px clamp(32px, 5vw, 72px); align-items: end; }
.split .dek { margin: 0; } .split h1 { max-width: none; }
.split2 .row { align-items: start; } .split2 .dek { margin: 6px 0 0; } .split2 h1 { max-width: none; }
.facts.two { grid-template-columns: repeat(2, minmax(0, 1fr)); margin-top: 28px; }
.split .c-d0 .dek { margin: 0; } .split .row:has(.c-d0) { align-items: start; margin-top: 22px; } .split .row .facts.two { margin-top: 0; padding-top: 0; border-top: 0; }
/* 4, 5, 13 centred */
.centre .mid { text-align: center; } .centre h1, .centre .dek { margin-left: auto; margin-right: auto; } .centre h1 { max-width: 22ch; } .centre .dek { max-width: 60ch; }
.facts.div { gap: 0; text-align: center; } .facts.div div { padding: 0 14px; } .facts.div div + div { border-left: 1px solid var(--line); } .facts.div .team { justify-content: center; }
.facts.card { border: 0; background: var(--mist); border-radius: 18px; padding: 22px 8px; margin-top: 44px; }
.facts.pills { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; border: 0; padding: 0; margin-top: 30px; }
.facts.pills div { display: inline-flex; align-items: center; gap: 8px; min-height: 40px; padding: 0 14px; border-radius: 999px; background: color-mix(in srgb, var(--ink) 5%, transparent); }
.facts.pills dt { margin: 0; font-size: 11px; } .facts.pills .mate img { width: 30px; height: 30px; } .facts.pills .mate { padding: 7px 2px; }
/* 6, 7 sidebar */
.side .row { align-items: start; grid-template-columns: minmax(0, 1fr) minmax(220px, 300px); } .side h1 { max-width: 18ch; }
.facts.stack { grid-template-columns: 1fr; gap: 16px; margin: 6px 0 0; padding: 0 0 0 24px; border-top: 0; border-left: 1px solid var(--line); }
.facts.stack.panel { border: 0; background: var(--mist); border-radius: 18px; padding: 22px 24px; margin: 0; }
/* 8 wide */
.wide h1 { max-width: none; font-size: clamp(34px, 5.6vw, 76px); } .wide .dek { margin-top: 26px; max-width: 62ch; }
/* 9 grid */
.grid h1 { max-width: 22ch; } .g5 { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 0 24px; } .g5 .dek { grid-column: 2 / -1; max-width: none; }
/* 10 band */
.band .bandbox { margin: 0 calc(-1 * clamp(20px, 4vw, 56px)); padding: clamp(28px, 4vw, 48px) clamp(20px, 4vw, 56px) 30px; background: #eef1f6; }
.band .facts { border-top-color: #d6dbe4; }
/* 11 logo */
.logo .row { align-items: center; grid-template-columns: minmax(0, 1fr) auto; } .logo .c-l .co-logo { width: clamp(96px, 12vw, 160px); height: auto; border-radius: 32px; }
/* 12 inline */
.facts.inline { display: flex; flex-wrap: wrap; gap: 10px 0; } .facts.inline div { display: inline-flex; align-items: center; gap: 8px; padding-right: 18px; margin-right: 18px; border-right: 1px solid var(--line); }
.facts.inline div:last-child { border-right: 0; } .facts.inline dt { margin: 0; font-size: 11px; } .facts.inline .mate img { width: 30px; height: 30px; } .facts.inline .mate { padding: 7px 2px; }
/* 15 eyebrow + ruled */
.eye { display: flex; align-items: center; gap: 10px; margin: 0 0 18px; font-size: 14px; font-weight: 500; color: var(--ink-2); } .eye .co-logo { width: 28px; height: 28px; border-radius: 8px; }
.facts.ruled { border-bottom: 1px solid var(--line); padding-bottom: 22px; }
@media (max-width: 860px) {
  .row, .side .row, .row2, .g5 { grid-template-columns: 1fr; } .g5 .dek { grid-column: 1; } .row2 > div:first-child { display: none; }
  .facts, .facts.div { grid-template-columns: repeat(2, minmax(0, 1fr)); } .facts.div div + div { border-left: 0; } .facts.div { gap: 18px 0; }
  .facts.stack { padding-left: 0; border-left: 0; margin-top: 28px; } .logo .c-l { display: none; }
  .cnav .back span { display: none; } .cnav .back { padding-right: 8px; }
}
"""
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, "index.html"), "w").write(f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="../assets/mj-logo.svg" type="image/svg+xml">
<title>Case-study header: 15 options</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;650;700&display=swap">
<link rel="stylesheet" href="../fonts/fonts.css">
<style>{CSS}</style>
</head>
<body>
<main class="page">
  <a class="back-lab" href="../case-studies/trellis.html">← Trellis case study</a>
  <h1>Case-study header: 15 options</h1>
  <p class="intro"><a href="full-1.html">1</a> · <a href="full-4.html">4</a> · <a href="full-7.html">7</a> · <a href="full-8.html">8</a> · <a href="full-13.html">13</a>: shortlisted, shown in the full case study.</p>
  <p class="intro">The top of a case study, shown on Trellis. Each one starts with “Back to work” on the left and the next case study on the right, then the same title, intro and five facts, arranged to avoid the empty space on the right.</p>
{secs}
</main>
</body>
</html>
""")
# ---- The shortlist in the full Trellis case study: the built page with its opening swapped for the option.
import re
PICKS = [1, 4, 7, 8, 13]
page = open(os.path.join(ROOT, "redesigns", "case-studies", "trellis.html")).read()
OPEN = re.compile(r'  <section class="wrap cs-hero">.*?</section>\n', re.S); assert OPEN.search(page), "Trellis opening not found"
HEAD_CSS = CSS[CSS.index("/* the header itself"):]
# a few class names here are already used by the case-study styles, so the copies use their own
REN = {"facts": "hfacts", "team": "hteam", "mate": "hmate", "split": "hsplit", "wide": "hwide", "next": "hnext"}
def own(t):   # only class attributes in the markup and class selectors in the CSS, never the words in the copy
    t = re.sub(r'class="([^"]*)"', lambda m: 'class="' + " ".join(REN.get(c, c) for c in m.group(1).split()) + '"', t)
    return re.sub(r"\.(" + "|".join(REN) + r")(?![\w-])", lambda m: "." + REN[m.group(1)], t)
for n in PICKS:
    name, note, cls, html = V[n - 1]
    hd = own(f'  <header class="wrap hd {cls}">{html}</header>\n')
    out = OPEN.sub(lambda m: hd, page, 1).replace("<head>", '<head>\n<base href="../case-studies/">', 1).replace("</head>", f"<style>{own(HEAD_CSS)}\n.hd {{ padding-bottom: 40px; }}</style>\n</head>", 1)
    open(os.path.join(OUT, f"full-{n}.html"), "w").write(out)
print("built cs-head-lab")
