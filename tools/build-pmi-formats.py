"""Five layouts of the same case study (PMI, Homebot) so Matt can pick a format.
Same copy and images in each; only the structure changes.
  pmi-formats/f1-impact-first.html   — header row, In short, contents rail, context → opportunity → approach → outcome
  pmi-formats/f2-key-decisions.html  — the story as three decisions with their evidence
  pmi-formats/f3-snapshot.html       — one screen, plus an optional full story
  pmi-formats/f4-visual-story.html   — images lead, captions alongside
  pmi-formats/f5-double-diamond.html — Discover → Define → Design → Deliver
Shares header, footer and base CSS with tools/build-cases.py. Re-run: python3 tools/build-pmi-formats.py
"""
import importlib.util, os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
spec = importlib.util.spec_from_file_location("build_cases", os.path.join(HERE, "build-cases.py"))
bc = importlib.util.module_from_spec(spec); spec.loader.exec_module(bc)

A = os.path.join(ROOT, "redesigns", "a-clarity")
OUT = os.path.join(ROOT, "redesigns", "pmi-formats")
HOME = bc.HOME
IMG = "../assets/"

FORMATS = [("f1-impact-first.html", "1", "Impact first"), ("f2-key-decisions.html", "2", "Key decisions"), ("f3-snapshot.html", "3", "Snapshot"),
           ("f4-visual-story.html", "4", "Visual story"), ("f5-double-diamond.html", "5", "Double Diamond")]

# ---------- Shared copy (identical in every format) ----------
TITLE = "Helping homeowners drop mortgage insurance early"
DEK = "About a million Homebot homeowners could stop paying PMI sooner than they thought. I designed the feature that told them, and gave their loan officers a reason to start the conversation."
META = [("Company", "Homebot"), ("My role", "Senior Product Designer"), ("My part", "Prototyping, research, delivery plan"), ("Team", "Consumer Team"), ("Date", "July 2022")]
P_OPPORTUNITY = "Interviews and our data warehouse pointed to the same opportunity: help homeowners realise the savings they could make on private mortgage insurance (PMI), and help our customers, their loan officers and realtors, build trust as their advisors."
P_SIZE = "We estimated that around <strong>one million</strong> US homeowners using Homebot were eligible to remove PMI early, saving each of them around <strong>$195 a month</strong>. Together that came to roughly <strong>$200 million a month</strong>."
LI_PRICES = "Home prices rose faster than ever in 2021. The typical home gained <strong>$50,000</strong> in value."
LI_COVID = "Nearly two-thirds of US households struck by COVID-19 faced financial trouble."
LI_PMI = "PMI lets buyers without a 20% down payment become homeowners. It can be removed once the loan-to-value ratio falls below 80% of the original appraised value, or sooner if the home has appreciated."
CALLOUT = "Rising prices meant many homeowners may already have crossed that line without realising it."
LI_EXPLORE = "<strong>Explored broadly.</strong> I sketched and rapidly prototyped variations on copy, infographics and visualisations, and on ways to connect homeowners with their loan officers and realtors."
LI_TEST = "<strong>Tested with 20 people.</strong> I ran usability sessions with 20 participants and landed on a design rated <strong>4.8 out of 5</strong> on its value and on confidence in removing PMI."
LI_PLAN = "<strong>Planned delivery with engineering.</strong> With the engineering leads I broke the design into four sprints, each the smallest chunk of deliverable value."
LI_REQUESTS = "Within the first sprint, homeowners sent <strong>over 500 requests</strong> to learn more about cancelling PMI, worth around <strong>$97,500 a month</strong> in savings."
LI_PRESENT = "I presented the project to the whole company using the Double Diamond framework. It connected colleagues to our mission, showed how the product org works, and built excitement for the feature."

COVER_ALT = "Two phone screens: 'When can you remove your $152.13 monthly mortgage insurance? Maybe now' with a 20% removal progress bar, and a screen listing ways to remove PMI faster"
FIG_ITER = f'<figure class="fig"><div class="frame"><img src="{IMG}pmi-iterations.png" alt="Figma board of PMI screen iterations" loading="lazy"></div><figcaption>Iterations on copy, visualisations and contact options.</figcaption></figure>'
FIG_HANDOFF = f'<figure class="fig"><div class="frame"><img src="{IMG}pmi-handoff.png" alt="Figma handoff board with light and dark mode screens" loading="lazy"></div><figcaption>Handoff, including light mode.</figcaption></figure>'
FIG_PAIR = f'<div class="fig-pair">{FIG_ITER}{FIG_HANDOFF}</div>'
FIG_HANDOFF_SOLO = FIG_HANDOFF.replace('class="fig"', 'class="fig narrow"')
VIDEO = f"""<a class="video" href="https://www.youtube.com/watch?v=7k9B34Jx0yg">
          <img src="{IMG}pmi-video.jpg" alt="Video still of the PMI feature: 'When can you remove your monthly mortgage insurance? Soon.' with a 16% progress bar" loading="lazy">
          <span class="play"><i></i>Watch the walkthrough</span>
        </a>"""
RESULTS = """<div class="results">
      <div><b class="num">≈1M</b><span>US homeowners on Homebot eligible to remove PMI early</span></div>
      <div><b class="num">$195</b><span>estimated monthly saving per homeowner</span></div>
      <div><b class="num">4.8/5</b><span>rating for value and confidence in usability testing</span></div>
      <div><b class="num">500+</b><span>requests to learn about PMI removal in the first sprint</span></div>
    </div>"""
TLDR = bc.tldr([("Problem", "Around a million homeowners on Homebot were paying for mortgage insurance they could already remove, and didn’t know it."),
                ("What I did", "Prototyped widely, tested with 20 people, and planned delivery in four sprints with the engineering leads."),
                ("Result", "Over 500 requests to learn about removing PMI in the first sprint, from an opportunity worth an estimated $200M a month.")],
               [("≈$200M", "a month in estimated savings for ≈1M homeowners"), ("4.8/5", "for value and confidence in usability testing"), ("500+", "requests in the first sprint")])
NEXT = f"""  <div class="wrap next">
    <a href="https://www.mjongbloet.com/portfolio/home-search">
      <div><p class="eyebrow">Next project</p><h3>Home Search</h3></div>
      <img src="{IMG}home-search.jpg" alt="">
    </a>
  </div>
"""


def bar(current):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == current else ""}><b>{n}</b><span>{label}</span></a>' for h, n, label in FORMATS)
    return f"""<div class="formatbar"><div class="wrap"><span class="eyebrow">PMI case study · 5 layouts</span><nav aria-label="Case study layouts">{links}</nav></div></div>
"""


def page(fname, label, body):
    h = bc.head(f"PMI · {label} — Matt Jongbloet", "Helping ≈1 million US homeowners discover they can drop private mortgage insurance early.")
    h = h.replace('<link rel="stylesheet" href="case.css">', '<link rel="stylesheet" href="case.css">\n<link rel="stylesheet" href="formats.css">')
    return h + bar(fname) + "\n<main>\n" + body + NEXT + "</main>\n" + bc.FOOT


def hero(extra=""):
    return f"""  <section class="wrap cs-hero">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{HOME}index.html#work">Work</a><span>/</span><span>Homebot</span></nav>
    <h1>{TITLE}</h1>
    <p class="dek">{DEK}</p>
    {bc.meta(META)}{extra}
  </section>
"""


COVER = f'<div class="cs-cover"><img src="{IMG}pmi-mockup.png" alt="{COVER_ALT}"></div>'

# ---------- 1 · Impact first ----------
F1 = hero() + f"""
  <div class="wrap">
    {TLDR}
    {COVER}
  </div>

  <div class="wrap cs-body">
    <nav class="toc" aria-label="Contents">
      <span class="eyebrow">Contents</span>
      <a href="#context" class="on">Context</a>
      <a href="#opportunity">Opportunity</a>
      <a href="#approach">Approach</a>
      <a href="#outcome">Outcome</a>
    </nav>
    <article class="prose">
      <section id="context">
        <p class="eyebrow">Context</p>
        <h2>Why it mattered in 2022</h2>
        <ul><li>{LI_PRICES}</li><li>{LI_COVID}</li><li>{LI_PMI}</li></ul>
        <p class="callout">{CALLOUT}</p>
      </section>
      <section id="opportunity">
        <p class="eyebrow">Opportunity</p>
        <h2>An opportunity hiding in our data</h2>
        <p>{P_OPPORTUNITY}</p>
        <p>{P_SIZE}</p>
      </section>
      <section id="approach">
        <p class="eyebrow">Approach</p>
        <h2>Prototype widely, test hard, ship in slices</h2>
        <ul><li>{LI_EXPLORE}</li><li>{LI_TEST}</li><li>{LI_PLAN}</li></ul>
        {FIG_PAIR}
      </section>
      <section id="outcome">
        <p class="eyebrow">Outcome</p>
        <h2>500 requests in the first sprint</h2>
        <ul><li>{LI_REQUESTS}</li><li>{LI_PRESENT}</li></ul>
        {VIDEO}
      </section>
    </article>
  </div>
"""


def decision(n, q, did, evidence, fig=""):
    return f"""          <li><span class="d-n num">{n}</span><div><h3>{q}</h3><dl>
            <div><dt>What I did</dt><dd>{did}</dd></div>
            <div><dt>Evidence</dt><dd>{evidence}</dd></div></dl>{fig}</div></li>"""


# ---------- 2 · Key decisions ----------
F2 = hero() + f"""
  <div class="wrap">
    {TLDR}
    {COVER}
  </div>

  <div class="wrap cs-body">
    <nav class="toc" aria-label="Contents">
      <span class="eyebrow">Contents</span>
      <a href="#bet" class="on">The bet</a>
      <a href="#decisions">Key decisions</a>
      <a href="#alignment">Bringing people along</a>
      <a href="#outcome">Outcome</a>
    </nav>
    <article class="prose">
      <section id="bet">
        <p class="eyebrow">The bet</p>
        <h2>Homeowners were paying for insurance they could already drop</h2>
        <p>{LI_PMI}</p>
        <p class="callout">{CALLOUT}</p>
      </section>
      <section id="decisions">
        <p class="eyebrow">Key decisions</p>
        <h2>Three calls that shaped it</h2>
        <ol class="decisions">
{decision("01", "Which opportunity is worth building?", "Followed where interviews and our data warehouse agreed: helping homeowners realise the savings on PMI, and helping loan officers and realtors build trust as their advisors.", "Around one million eligible homeowners on Homebot, saving about $195 a month each: roughly $200 million a month.")}
{decision("02", "How do we tell someone they might be overpaying?", "Sketched and rapidly prototyped variations on copy, infographics and visualisations, and on ways to connect homeowners with their loan officers and realtors.", "Usability sessions with 20 participants; the final design was rated 4.8 out of 5 on its value and on confidence in removing PMI.", FIG_ITER)}
{decision("03", "How do we get it to homeowners quickly?", "With the engineering leads, broke the design into four sprints, each the smallest chunk of deliverable value.", "Over 500 requests to learn about cancelling PMI within the first sprint, worth around $97,500 a month in savings.", FIG_HANDOFF_SOLO)}
        </ol>
      </section>
      <section id="alignment">
        <p class="eyebrow">Bringing people along</p>
        <h2>One story for the whole company</h2>
        <ul><li>{LI_PRESENT}</li></ul>
      </section>
      <section id="outcome">
        <p class="eyebrow">Outcome</p>
        <h2>500 requests in the first sprint</h2>
        <ul><li>{LI_REQUESTS}</li></ul>
        {VIDEO}
      </section>
    </article>
  </div>
"""

# ---------- 3 · Snapshot ----------
F3 = f"""  <section class="wrap snapshot">
    <div class="snap-visual has-img"><img src="{IMG}pmi-mockup.png" alt="{COVER_ALT}"></div>
    <div class="snap-copy">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="{HOME}index.html#work">Work</a><span>/</span><span>Homebot</span></nav>
      <h1>{TITLE}</h1>
      <p class="dek">{DEK}</p>
      <dl class="snap-meta">{"".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in META)}</dl>
      <div class="snap-stats">
        <div><b class="num">≈$200M</b><span>a month in estimated savings</span></div>
        <div><b class="num">4.8/5</b><span>in usability testing</span></div>
        <div><b class="num">500+</b><span>requests in the first sprint</span></div>
      </div>
      <dl class="snap-lines">
        <div><dt>Problem</dt><dd>Around a million homeowners on Homebot could remove PMI early, saving about $195 a month each, and didn’t know it.</dd></div>
        <div><dt>Approach</dt><dd>Prototyped widely, tested with 20 people, and planned delivery in four sprints with the engineering leads.</dd></div>
        <div><dt>Result</dt><dd>Over 500 requests to learn about cancelling PMI in the first sprint, worth around $97,500 a month in savings.</dd></div>
      </dl>
    </div>
  </section>

  <section class="wrap">
    <details class="deep">
      <summary>Read the full story</summary>
      <div class="prose">
        <section><h2>Why it mattered in 2022</h2><ul><li>{LI_PRICES}</li><li>{LI_COVID}</li><li>{LI_PMI}</li></ul><p class="callout">{CALLOUT}</p></section>
        <section><h2>An opportunity hiding in our data</h2><p>{P_OPPORTUNITY}</p><p>{P_SIZE}</p></section>
        <section><h2>Prototype widely, test hard, ship in slices</h2><ul><li>{LI_EXPLORE}</li><li>{LI_TEST}</li><li>{LI_PLAN}</li></ul>{FIG_PAIR}</section>
        <section><h2>500 requests in the first sprint</h2><ul><li>{LI_REQUESTS}</li><li>{LI_PRESENT}</li></ul>{VIDEO}</section>
      </div>
    </details>
  </section>
"""


def plate(n, label, title, body, visual, flip=False):
    return f"""    <section class="plate{' flip' if flip else ''}">
      <div class="plate-visual">{visual}</div>
      <div class="plate-cap"><span class="eyebrow"><span class="num">{n}</span> · {label}</span><h2>{title}</h2>{body}</div>
    </section>"""


IMG_FRAME = lambda src, alt, light=False: f'<div class="pframe{" light" if light else ""}"><img src="{IMG}{src}" alt="{alt}" loading="lazy"></div>'

# ---------- 4 · Visual story ----------
F4 = hero() + f"""
  <div class="wrap">
    {COVER}
    {RESULTS}
  </div>

  <div class="wrap plates">
{plate("01", "Opportunity", "An opportunity hiding in our data", f"<p>{P_OPPORTUNITY}</p><p>{P_SIZE}</p>", '<div class="bigstat"><b class="num">≈$200M</b><span>a month in estimated savings: around one million homeowners, about $195 each</span></div>')}
{plate("02", "Context", "Why it mattered in 2022", f"<ul><li>{LI_PRICES}</li><li>{LI_COVID}</li><li>{LI_PMI}</li></ul>", f'<blockquote class="bigquote">{CALLOUT}</blockquote>', True)}
{plate("03", "Explore and test", "Prototype widely, test hard", f"<ul><li>{LI_EXPLORE}</li><li>{LI_TEST}</li></ul>", IMG_FRAME("pmi-iterations.png", "Figma board of PMI screen iterations"))}
{plate("04", "Deliver", "Ship in slices", f"<ul><li>{LI_PLAN}</li></ul>", IMG_FRAME("pmi-handoff.png", "Figma handoff board with light and dark mode screens"), True)}
{plate("05", "Outcome", "500 requests in the first sprint", f"<ul><li>{LI_REQUESTS}</li><li>{LI_PRESENT}</li></ul>", VIDEO)}
  </div>
"""


def phase(n, pid, name, gist, title, body):
    return f"""    <section class="phase" id="{pid}">
      <div class="phase-label"><span class="phase-n num">{n}</span><h2>{name}</h2><p>{gist}</p></div>
      <div class="phase-body"><h3>{title}</h3>{body}</div>
    </section>"""


def checkpoint(text):
    return f'    <p class="checkpoint"><i aria-hidden="true"></i>{text}</p>'


DIAMOND = """<svg class="dd" viewBox="0 0 660 150" role="img" aria-label="Double Diamond: Discover, Define, Design, Deliver">
      <polygon points="10,75 165,5 165,145" fill="#ffe3d6"/><polygon points="165,5 320,75 165,145" fill="#ffc9b0"/>
      <polygon points="340,75 495,5 495,145" fill="#ffe3d6"/><polygon points="495,5 650,75 495,145" fill="#ffc9b0"/>
      <g font-size="15" font-weight="600" fill="#15171a" text-anchor="middle"><text x="112" y="80">Discover</text><text x="218" y="80">Define</text><text x="442" y="80">Design</text><text x="548" y="80">Deliver</text></g>
    </svg>"""

# ---------- 5 · Double Diamond ----------
F5 = hero() + f"""
  <div class="wrap">
    {COVER}
    <div class="dd-wrap">
      {DIAMOND}
      <nav class="dd-nav" aria-label="Phases"><a href="#discover">01 Discover</a><a href="#define">02 Define</a><a href="#design">03 Design</a><a href="#deliver">04 Deliver</a></nav>
    </div>
  </div>

  <div class="wrap phases">
{phase("01", "discover", "Discover", "Understand the people and the moment.", "Why it mattered in 2022", f'<ul><li>{LI_PRICES}</li><li>{LI_COVID}</li></ul><p>{P_OPPORTUNITY}</p>')}
{checkpoint("We’ve identified an opportunity to pursue.")}
{phase("02", "define", "Define", "Pin down the exact problem.", "A million homeowners paying for insurance they could drop", f'<ul><li>{LI_PMI}</li></ul><p class="callout">{CALLOUT}</p><p>{P_SIZE}</p>')}
{checkpoint("We’ve defined the exact problem to solve.")}
{phase("03", "design", "Design", "Explore widely, then test.", "Prototype widely, test hard", f'<ul><li>{LI_EXPLORE}</li><li>{LI_TEST}</li></ul>{FIG_ITER}')}
{phase("04", "deliver", "Deliver", "Ship in slices and measure.", "500 requests in the first sprint", f'<ul><li>{LI_PLAN}</li><li>{LI_REQUESTS}</li><li>{LI_PRESENT}</li></ul>{FIG_HANDOFF_SOLO}{VIDEO}')}
{checkpoint("We’ve identified a good solution to the problem.")}
    {RESULTS}
  </div>
"""

CSS = """/* Five layouts of the PMI case study (tools/build-pmi-formats.py). Adds to style.css + case.css. */
.formatbar a b { min-width: 1ch; }
.cs-cover { margin-top: 0; }
.cs-hero { padding-bottom: 32px; }
.prose .decisions .fig { margin-top: 18px; }

/* 3 · Snapshot with a real image */
.snap-visual.has-img { padding: 0; background: #e8e8e8; overflow: hidden; min-height: 0; aspect-ratio: 5 / 4; }
.snap-visual.has-img img { width: 100%; height: 100%; object-fit: cover; }
.deep .prose { max-width: 760px; gap: 56px; padding-top: 12px; }
.deep[open] summary { border-bottom: 1px solid var(--line); margin-bottom: 28px; }

/* 4 · Visual story */
.plates { padding-top: 40px; }
.plate { display: grid; grid-template-columns: minmax(0, 1.55fr) minmax(0, 1fr); gap: 56px; align-items: start; padding-block: 64px; border-top: 1px solid var(--line); }
.plate:first-child { border-top: 0; }
.plate.flip .plate-visual { order: 2; }
.plate-cap { position: sticky; top: 100px; display: flex; flex-direction: column; gap: 16px; }
.plate-cap h2 { font-size: clamp(26px, 2.6vw, 34px); font-weight: 700; }
.plate-cap p, .plate-cap li { color: #33363c; font-size: 16px; line-height: 1.6; }
.plate-cap ul { margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 12px; }
.plate-cap li { position: relative; padding-left: 24px; }
.plate-cap li::before { content: ""; position: absolute; left: 2px; top: .75em; width: 10px; height: 2px; background: var(--signal); }
.plate-cap strong { color: var(--ink); }
.pframe { border-radius: var(--radius); overflow: hidden; background: #1c1c1c; }
.pframe.light { background: #e8e8e8; }
.pframe img { width: 100%; }
.bigstat { border-radius: var(--radius); background: var(--signal-soft); padding: 56px 48px; display: flex; flex-direction: column; gap: 14px; }
.bigstat b { font: 700 clamp(64px, 9vw, 128px)/0.95 var(--display); letter-spacing: -0.04em; color: var(--signal-ink); padding-top: 6px; }
.bigstat span { font-size: 19px; max-width: 30ch; line-height: 1.45; }
.fig.narrow { max-width: 440px; }
.bigquote { margin: 0; padding: 56px 48px; border-radius: var(--radius); background: var(--signal-soft); font: 600 clamp(26px, 3vw, 40px)/1.2 var(--display); letter-spacing: -0.02em; color: var(--ink); }

/* 5 · Double Diamond */
.dd-wrap { display: flex; flex-direction: column; align-items: center; gap: 18px; padding-block: 56px 8px; }
.dd { width: min(660px, 100%); height: auto; font-family: var(--display); }
.dd-nav { display: flex; flex-wrap: wrap; gap: 6px; justify-content: center; }
.dd-nav a { padding: 9px 16px; border-radius: 999px; background: var(--mist); text-decoration: none; font-size: 15px; font-weight: 500; }
.dd-nav a:hover { background: var(--signal-soft); color: var(--signal-ink); }
.phases { padding-top: 24px; }
.phase { display: grid; grid-template-columns: 240px minmax(0, 720px); gap: 64px; padding-block: 56px; border-top: 1px solid var(--line); scroll-margin-top: 80px; }
.phase-label { position: sticky; top: 100px; align-self: start; display: flex; flex-direction: column; gap: 8px; }
.phase-n { font: 500 13px/1 var(--mono); color: var(--signal-ink); }
.phase-label h2 { font-size: clamp(30px, 3vw, 40px); font-weight: 700; }
.phase-label p { color: var(--ink-2); font-size: 15px; }
.phase-body { display: flex; flex-direction: column; gap: 18px; }
.phase-body h3 { font-size: clamp(22px, 2.2vw, 28px); font-weight: 700; line-height: 1.2; }
.phase-body p, .phase-body li { color: #33363c; }
.phase-body ul { margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 14px; }
.phase-body li { position: relative; padding-left: 28px; }
.phase-body li::before { content: ""; position: absolute; left: 4px; top: .7em; width: 10px; height: 2px; background: var(--signal); }
.phase-body strong { color: var(--ink); }
.checkpoint { display: flex; align-items: center; gap: 12px; margin: 0 0 0 304px; padding: 14px 18px; border-radius: 12px; background: var(--signal-soft); font-weight: 600; max-width: 720px; }
.checkpoint i { flex: none; width: 12px; height: 12px; border-radius: 50%; background: var(--signal); }
.phases .results { margin-top: 56px; }

@media (max-width: 900px) {
  .plate, .phase { grid-template-columns: 1fr; gap: 24px; padding-block: 40px; }
  .plate.flip .plate-visual { order: 0; }
  .plate-cap, .phase-label { position: static; }
  .checkpoint { margin-left: 0; }
  .bigquote, .bigstat { padding: 32px 24px; }
}
@media (max-width: 560px) {
  .formatbar a span { display: none; }
  .formatbar a { padding: 8px 12px; }
  .dd-nav a { padding: 9px 12px; font-size: 14px; }
}
"""


def build():
    os.makedirs(OUT, exist_ok=True)
    shutil.copy(os.path.join(A, "style.css"), os.path.join(OUT, "style.css"))
    shutil.copy(os.path.join(A, "script.js"), os.path.join(OUT, "script.js"))
    open(os.path.join(OUT, "case.css"), "w").write(bc.CSS)
    open(os.path.join(OUT, "formats.css"), "w").write(CSS)
    for (fname, _, label), body in zip(FORMATS, [F1, F2, F3, F4, F5]):
        open(os.path.join(OUT, fname), "w").write(page(fname, label, body))
    print("built pmi-formats")


if __name__ == "__main__":
    build()
