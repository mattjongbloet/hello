"""Case-study formats, in the A6 look (A's style.css + Roobert):
  cases/trellis.html     — Format 1, Impact first   (filled in from the Trellis deck and Matt's notes)
  cases/carv.html        — Format 2, Key decisions  (template: CV facts + placeholders)
  cases/hospitable.html  — Format 3, Snapshot       (template: CV facts + placeholders)
Placeholders are marked .ph and listed again under "To fill in" at the end of each page.
Re-run: python3 tools/build-cases.py
"""
import os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "redesigns", "a-clarity")
OUT = os.path.join(ROOT, "redesigns", "cases")
HOME = "../a6-text-first/"
CV = "https://cdn.prod.website-files.com/63b35214bc1dc0317e22bd99/668ae1b79c5572bfad32e508_Matt_Jongbloet_CV_2024.pdf"
FONT = "https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;650;700&family=JetBrains+Mono:wght@500&display=swap"


def ph(text):
    return f'<span class="ph">{text}</span>'


def head(title, desc):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="icon" href="../assets/mj-logo.svg" type="image/svg+xml">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONT}">
<link rel="stylesheet" href="../fonts/fonts.css">
<link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="case.css">
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="brand" href="{HOME}index.html"><img class="mark" src="../assets/mj-logo.svg" alt="">Matt Jongbloet</a>
    <nav class="nav" aria-label="Main">
      <a href="{HOME}index.html#work" aria-current="page">Work</a>
      <a href="{HOME}about.html">About</a>
      <a href="{CV}">Resume</a>
    </nav>
    <a class="btn" href="#contact">Contact</a>
  </div>
</header>
"""


def formatbar(current):
    items = [("trellis.html", "1 · Impact first", "Trellis"), ("carv.html", "2 · Key decisions", "Carv"), ("hospitable.html", "3 · Snapshot", "Hospitable")]
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == current else ""}><b>Format {f}</b><span>{p}</span></a>' for h, f, p in items)
    return f"""<div class="formatbar"><div class="wrap"><span class="eyebrow">Case study formats</span><nav aria-label="Case study formats">{links}</nav></div></div>
"""


def meta(rows):
    return '<dl class="meta meta5">' + "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in rows) + "</dl>"


def tldr(lines, stats):
    ls = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in lines)
    ss = "".join(f'<div><b class="num">{n}</b><span>{t}</span></div>' for n, t in stats)
    return f"""<div class="tldr">
      <dl class="tldr-lines"><span class="eyebrow">In short</span>{ls}</dl>
      <div class="tldr-stats">{ss}</div>
    </div>"""


def todo(items):
    li = "".join(f"<li>{i}</li>" for i in items)
    return f"""  <section class="wrap todo" aria-label="To fill in">
    <div class="todo-card"><p class="eyebrow">To fill in (review note, not part of the page)</p><ol>{li}</ol></div>
  </section>
"""


def nextp(href, eyebrow, title, img):
    return f"""  <div class="wrap next">
    <a href="{href}">
      <div><p class="eyebrow">{eyebrow}</p><h3>{title}</h3></div>
      {img}
    </a>
  </div>
"""


FOOT = f"""<section class="contact" id="contact">
  <div class="wrap">
    <div>
      <h2>Drop me a line.</h2>
      <p>I’m looking for opportunities where I can help teams build the right thing, and build it right. I’m in Amsterdam (CET).</p>
    </div>
    <div class="links">
      <a class="btn" href="mailto:matthewjongbloet@gmail.com">matthewjongbloet@gmail.com</a>
      <a class="plain" href="{CV}">Resume (PDF) ↗</a>
    </div>
  </div>
</section>
<footer class="foot"><div class="wrap"><span>© 2026 Matt Jongbloet</span><span><a href="{HOME}index.html">Work</a> · <a href="{HOME}about.html">About</a> · <a href="#contact">Contact</a></span></div></footer>
<script src="script.js"></script>
</body>
</html>
"""

T = "../assets/trellis/"

TRELLIS = head("Trellis: Growth experiments — Matt Jongbloet", "In 3 months, a small growth team and I ran experiments on around 15 parts of Savvy’s car insurance quote flow: $3.5MM in predicted gross annual revenue.") + formatbar("trellis.html") + f"""
<main>
  <section class="wrap cs-hero">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{HOME}index.html#work">Work</a><span>/</span><span>Trellis</span></nav>
    <h1>Finding $3.5MM in a car insurance quote flow</h1>
    <p class="dek">In three months, a small growth team and I ran experiments on around 15 parts of Savvy’s car insurance quote flow, and proved we could get more people from “I want a quote” to “here are my offers”.</p>
    {meta([("Company", "Trellis / Savvy.Insure"), ("My role", "Staff Product Designer, leading design for the growth team"), ("Team", "1 front-end engineer, 1 back-end engineer, 1 growth engineering consultant"), ("Timeframe", "3 months, 2023"), ("Surface", "Car insurance quote flow")])}
  </section>

  <div class="wrap">
    {tldr([("Problem", "Only about 59% of people who started the car insurance application finished it. Every drop-off was a quote, and revenue, lost."),
            ("What I did", "Led design for a small growth team through around 15 experiments on the quote flow, from hypothesis to test to decision."),
            ("Result", "$3.5MM in predicted gross annual revenue. One test alone lifted completion from 60.4% to 69.0%.")],
           [("$3.5MM", "predicted gross annual revenue"), ("~15", "parts of the flow tested in 3 months"), ("+8.6 pts", "completion in the re-order test (60.4% → 69.0%)")])}
    <a class="cover" href="{T}flow-v2.jpg"><img src="{T}cover-v2.jpg" alt="The re-ordered quote flow: vehicle details, your vehicles, tell us about yourself, your drivers, home address"></a>
  </div>

  <div class="wrap cs-body">
    <nav class="toc" aria-label="Contents">
      <span class="eyebrow">Contents</span>
      <a href="#context" class="on">Context</a>
      <a href="#problem">Problem</a>
      <a href="#approach">Approach</a>
      <a href="#experiment">Featured experiment</a>
      <a href="#outcome">Outcome</a>
      <a href="#learnings">Learnings</a>
    </nav>

    <article class="prose">
      <section id="context">
        <p class="eyebrow">Context</p>
        <h2>Where the business wins or loses</h2>
        <p>Savvy.Insure, by Trellis, set out to make insurance easier for everyone. Someone who wants car insurance comes to Savvy, tells us about themselves, their cars and their drivers, and gets quotes back. That flow is where the business makes or loses money.</p>
      </section>

      <section id="problem">
        <p class="eyebrow">Problem</p>
        <h2>Four in ten people gave up before their quote</h2>
        <p>From 17 to 31 May 2023, <strong>44,846</strong> people started the unlinked application and <strong>26,333</strong> finished it: a completion rate of <strong>58.7%</strong>. {ph("Add one line on what “unlinked” means, e.g. people who fill the form in by hand rather than linking an existing policy.")}</p>
        <figure class="fig"><a class="frame light" href="{T}baseline-chart.jpg"><img src="{T}baseline-chart.jpg" alt="Bar chart: 44,846 started the unlinked application, 26,333 completed it, 58.7% total conversion, 17 to 31 May 2023" loading="lazy"></a><figcaption>Baseline, 17–31 May 2023: 58.7% of people who started the application completed it.</figcaption></figure>
      </section>

      <section id="approach">
        <p class="eyebrow">Approach</p>
        <h2>Learn cheaply, decide with evidence</h2>
        <ul>
          <li><strong>The cheapest way to learn.</strong> Not every experiment needs to be an A/B test. We framed each change as a hypothesis, picked the lightest method that could confirm or disconfirm it, and used A/B tests where we needed statistical confidence.</li>
          <li><strong>One small team, a steady cadence.</strong> With a front-end engineer, a back-end engineer and a growth engineering consultant, I designed and shipped experiments on around 15 parts of the flow in three months.</li>
          <li><strong>Making it a habit.</strong> I co-wrote and presented <em>How do we make good decisions about product investment?</em>, sharing how we chose methods, from interviews to A/B tests, and why learning matters more than being right.</li>
        </ul>
        <div class="xlog-wrap">
          <table class="xlog">
            <caption>Experiment log</caption>
            <thead><tr><th scope="col">#</th><th scope="col">Change</th><th scope="col">Hypothesis</th><th scope="col">Result</th></tr></thead>
            <tbody>
              <tr><td class="num">01</td><td>Re-order the application</td><td>Asking for the car before contact details will raise completion.</td><td><b class="num">60.4% → 69.0%</b></td></tr>
              <tr><td class="num">02</td><td>{ph("Experiment")}</td><td>{ph("We think … will …")}</td><td>{ph("Result")}</td></tr>
              <tr><td class="num">03</td><td>{ph("Experiment")}</td><td>{ph("We think … will …")}</td><td>{ph("Result")}</td></tr>
              <tr><td class="num">04</td><td>{ph("Experiment")}</td><td>{ph("We think … will …")}</td><td>{ph("Result")}</td></tr>
            </tbody>
          </table>
          <p class="xlog-note">{ph("Add the rest of the ~15, or the 4–6 most telling. Losing tests are worth including: they show the judgment.")}</p>
        </div>
      </section>

      <section id="experiment">
        <p class="eyebrow">Featured experiment</p>
        <h2>Ask for the car before the phone number</h2>
        <p class="callout">Hypothesis: changing the order of the unlinked application flow will increase conversion.</p>
        <p>The control flow opened by asking for name, phone, email and date of birth, before Savvy had given anything back. V2 starts with the car and the drivers, builds up to the policy, and only asks for contact details at the very end, as <em>“Where should we send your offers?”</em></p>
        <figure class="fig wide"><a class="frame light" href="{T}flow-control.jpg"><img src="{T}flow-control.jpg" alt="Control flow, nine phone screens: basic information with phone and email first, then address, own or rent, vehicle information, vehicles, driver information, drivers, current premium, review" loading="lazy"></a><figcaption>Control: contact details on the very first screen.</figcaption></figure>
        <figure class="fig wide"><a class="frame light" href="{T}flow-v2.jpg"><img src="{T}flow-v2.jpg" alt="V2 flow, nine phone screens: vehicle information, vehicles, tell us about yourself, drivers, home address, own or rent, current premium, review, and where should we send your offers" loading="lazy"></a><figcaption>V2: vehicles and drivers first, contact details last. Stars mark the steps that moved.</figcaption></figure>
        <figure class="fig"><a class="frame light" href="{T}result-chart.jpg"><img src="{T}result-chart.jpg" alt="Bar chart, 1 to 9 June 2023: control 60.4% (8,108 of 13,419 completed), V2 69.0% (8,498 of 12,319 completed)" loading="lazy"></a><figcaption>1–9 June 2023: control completed 60.4% (8,108 of 13,419); V2 completed 69.0% (8,498 of 12,319).</figcaption></figure>
      </section>

      <section id="outcome">
        <p class="eyebrow">Outcome</p>
        <h2>$3.5MM in predicted annual revenue</h2>
        <ul>
          <li>Over three months, the experiments added up to <strong>$3.5MM in predicted gross annual revenue</strong>.</li>
          <li>The re-order test lifted completion by <strong>8.6 points</strong>, a 14% relative improvement. {ph("Did V2 ship to everyone? Say so here.")}</li>
          <li>We left the team with the infrastructure to run similar tests with ease, and a shared way of deciding what to build.</li>
        </ul>
      </section>

      <section id="learnings">
        <p class="eyebrow">Learnings</p>
        <h2>Value before data</h2>
        <ul>
          <li><strong>People need Trellis to feel valuable before they give their info.</strong> Order matters.</li>
          <li><strong>Learning is more important than being right.</strong> Good testing infrastructure means more people share ideas, and it takes the HiPPO out of decisions.</li>
          <li><strong>What I’d do differently:</strong> {ph("one or two honest lines")}</li>
        </ul>
      </section>
    </article>
  </div>

{nextp("carv.html", "Next · Format 2", "Carv", '<span class="next-ph">Carv</span>')}
</main>
{todo(["What “unlinked application” means, in one line.",
       "The other experiments: change, hypothesis and result for 4–6 of the ~15.",
       "Whether V2 shipped, and anything you know about the effect after launch.",
       "How the $3.5MM was predicted (e.g. modelled from conversion lift × traffic × revenue per policy). One line makes it far more credible.",
       "A line on what you’d do differently.",
       "Any before/after screens of the other experiments, if you can find them."])}""" + FOOT

CARV = head("Carv — Matt Jongbloet", "Case study template: key decisions format.") + formatbar("carv.html") + f"""
<main>
  <section class="wrap cs-hero">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{HOME}index.html#work">Work</a><span>/</span><span>Carv</span></nav>
    <h1>{ph("Project title that sells the outcome")}</h1>
    <p class="dek">Helping recruiters cut admin and boost hires. {ph("One sentence on the project and its result.")}</p>
    {meta([("Company", "Carv"), ("My role", "Lead Product Designer"), ("Team", ph("e.g. PM, 4 engineers, data")), ("Timeframe", ph("e.g. Mar–Sep 2024, 6 months")), ("Surface", ph("e.g. Recruiter web app"))])}
  </section>

  <div class="wrap">
    {tldr([("Problem", ph("What was broken, for whom.")), ("What I did", ph("Your part, in one line.")), ("Result", ph("The outcome, with a number if you have one."))],
           [(ph("00"), ph("headline result")), (ph("00"), ph("second result")), (ph("00"), ph("scope, e.g. users"))])}
    <div class="cover cover-ph">{ph("Hero visual: the shipped product, or the vision prototype")}</div>
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
        <h2>{ph("What the company believed")}</h2>
        <p>{ph("Two or three sentences: the opportunity, what Carv believed, and what you set out to change.")}</p>
      </section>

      <section id="decisions">
        <p class="eyebrow">Key decisions</p>
        <h2>Three calls that shaped it</h2>
        <ol class="decisions">
          <li><span class="d-n num">01</span><div><h3>{ph("The question you faced")}</h3><dl>
            <div><dt>Options</dt><dd>{ph("What you considered.")}</dd></div>
            <div><dt>We chose</dt><dd>{ph("What you chose, and why.")}</dd></div>
            <div><dt>Evidence</dt><dd>{ph("Research, data or prototype that backed it.")}</dd></div></dl></div></li>
          <li><span class="d-n num">02</span><div><h3>{ph("The question you faced")}</h3><dl>
            <div><dt>Options</dt><dd>{ph("What you considered.")}</dd></div>
            <div><dt>We chose</dt><dd>{ph("What you chose, and why.")}</dd></div>
            <div><dt>Evidence</dt><dd>{ph("Research, data or prototype that backed it.")}</dd></div></dl></div></li>
          <li><span class="d-n num">03</span><div><h3>{ph("The question you faced")}</h3><dl>
            <div><dt>Options</dt><dd>{ph("What you considered.")}</dd></div>
            <div><dt>We chose</dt><dd>{ph("What you chose, and why.")}</dd></div>
            <div><dt>Evidence</dt><dd>{ph("Research, data or prototype that backed it.")}</dd></div></dl></div></li>
        </ol>
      </section>

      <section id="alignment">
        <p class="eyebrow">Bringing people along</p>
        <h2>From research to a shared vision</h2>
        <ul>
          <li><strong>Vision with the C-level.</strong> I led and executed design with cross-functional stakeholders and the C-level on the product’s future vision. {ph("How: workshops, a vision prototype, a roadmap?")}</li>
          <li><strong>Research into the real experience.</strong> I facilitated research into customers’ current experience to help them reach their goals. {ph("What did you learn that changed the plan?")}</li>
        </ul>
      </section>

      <section id="outcome">
        <p class="eyebrow">Outcome</p>
        <h2>{ph("What happened")}</h2>
        <p>{ph("Results, and what happened next: shipped, adopted, measured.")}</p>
      </section>
    </article>
  </div>

{nextp("hospitable.html", "Next · Format 3", "Hospitable", '<span class="next-ph">Hospitable</span>')}
</main>
{todo(["The project to feature, and a title that sells the outcome.",
       "Team and timeframe (e.g. PM, 4 engineers · Mar–Sep 2024).",
       "The three decisions that shaped it: options, choice, evidence.",
       "How you worked with the C-level on the vision (artefacts help: a vision prototype, a roadmap).",
       "Outcome numbers, or qualitative proof (customer quotes, adoption).",
       "Visuals: shipped screens, vision prototype, research artefacts."])}""" + FOOT

HOSP = head("Hospitable — Matt Jongbloet", "Case study template: snapshot format.") + formatbar("hospitable.html") + f"""
<main>
  <section class="wrap snapshot">
    <div class="snap-visual">{ph("Hero visual (crop or blur anything confidential)")}</div>
    <div class="snap-copy">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="{HOME}index.html#work">Work</a><span>/</span><span>Hospitable</span></nav>
      <h1>{ph("Project title")}</h1>
      <p class="dek">Helping hosts run their short-term rentals on autopilot. {ph("One sentence on this project.")}</p>
      <dl class="snap-meta">
        <div><dt>Company</dt><dd>Hospitable</dd></div>
        <div><dt>My role</dt><dd>Senior Staff Product Designer</dd></div>
        <div><dt>Team</dt><dd>{ph("e.g. PM, 5 engineers")}</dd></div>
        <div><dt>Timeframe</dt><dd>{ph("e.g. 2025, ongoing")}</dd></div>
      </dl>
      <div class="snap-stats">
        <div><b class="num">{ph("00")}</b><span>{ph("result")}</span></div>
        <div><b class="num">{ph("00")}</b><span>{ph("result")}</span></div>
        <div><b class="num">{ph("00")}</b><span>{ph("scope")}</span></div>
      </div>
      <dl class="snap-lines">
        <div><dt>Problem</dt><dd>{ph("What hosts struggled with.")}</dd></div>
        <div><dt>My role</dt><dd>{ph("What you owned vs. contributed to.")}</dd></div>
        <div><dt>Approach</dt><dd>{ph("How you got there, in one line.")}</dd></div>
        <div><dt>Result</dt><dd>{ph("What changed.")}</dd></div>
      </dl>
    </div>
  </section>

  <section class="wrap">
    <details class="deep">
      <summary>Read the full story</summary>
      <div class="prose">
        <p>{ph("Optional deep dive: context, key decisions, outcome. Or keep this for interviews and say so: “Happy to walk through this in person.”")}</p>
      </div>
    </details>
  </section>

{nextp("trellis.html", "Next · Format 1", "Trellis", f'<img src="{T}cover-v2.jpg" alt="">')}
</main>
{todo(["Which Hospitable project to show, and how much you can share.",
       "Team and timeframe.",
       "Three numbers (or two numbers and a scope, e.g. hosts or properties).",
       "The four lines: problem, your role, approach, result.",
       "A hero visual you’re allowed to show (crop or blur where needed)."])}""" + FOOT

CSS = """/* Case-study formats (tools/build-cases.py). Builds on A's style.css; Roobert via fonts.css. */
:root { --display: "Roobert", "Hanken Grotesk", ui-sans-serif, system-ui, sans-serif; --body: "Roobert", "Hanken Grotesk", ui-sans-serif, system-ui, sans-serif; }
.brand img.mark { width: auto; height: 34px; border-radius: 0; object-fit: contain; }

/* Review aid: switch between the three formats */
.formatbar { background: var(--mist); border-bottom: 1px solid var(--line); }
.formatbar .wrap { display: flex; align-items: center; gap: 20px; padding-block: 10px; flex-wrap: wrap; }
.formatbar nav { display: flex; gap: 6px; flex-wrap: wrap; }
.formatbar a { display: inline-flex; gap: 8px; align-items: baseline; padding: 8px 14px; border-radius: 999px; text-decoration: none; font-size: 14px; color: var(--ink-2); }
.formatbar a b { color: var(--ink); font-weight: 600; }
.formatbar a[aria-current="page"] { background: var(--paper); box-shadow: 0 0 0 1px var(--line); }
.formatbar a:hover { color: var(--ink); }

/* Placeholders */
.ph { display: inline; background: #fff4d6; color: #6b4e00; border-bottom: 1.5px dashed #d9a400; padding: 1px 4px; border-radius: 3px; font-weight: 500; font-style: normal; }
h1 .ph, h2 .ph, h3 .ph { font-weight: inherit; }

/* Header row (5 items) */
.cs-hero h1 { max-width: 20ch; }
.meta.meta5 { grid-template-columns: repeat(5, minmax(0, 1fr)); }
.meta.meta5 dd { font-weight: 500; line-height: 1.4; }

/* TL;DR */
.tldr { display: grid; grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr); gap: 0; border: 1px solid var(--line); border-radius: var(--radius); overflow: hidden; margin-bottom: 20px; }
.tldr-lines { margin: 0; padding: 28px 32px; display: flex; flex-direction: column; gap: 14px; }
.tldr-lines div { display: grid; grid-template-columns: 110px minmax(0, 1fr); gap: 16px; }
.tldr-lines dt { font: 500 11px/1.9 var(--mono); text-transform: uppercase; letter-spacing: .08em; color: var(--ink-2); }
.tldr-lines dd { margin: 0; font-size: 17px; line-height: 1.5; }
.tldr-stats { background: var(--signal-soft); padding: 28px 32px; display: flex; flex-direction: column; gap: 20px; justify-content: center; }
.tldr-stats div { display: flex; flex-direction: column; gap: 4px; }
.tldr-stats b { font: 700 clamp(30px, 3vw, 40px)/1 var(--display); letter-spacing: -0.03em; color: var(--signal-ink); padding-top: 2px; }
.tldr-stats span { font-size: 15px; color: var(--ink); }
.cover { display: block; border-radius: var(--radius); overflow: hidden; background: #dfe7fb; }
.cover img { width: 100%; }
.cover-ph { min-height: 360px; display: grid; place-items: center; background: repeating-linear-gradient(45deg, var(--mist), var(--mist) 12px, #efefea 12px, #efefea 24px); }

/* Figures */
.fig .frame { display: block; }
.fig .frame.light { background: #fff; border: 1px solid var(--line); }
.fig .frame img { width: 100%; }
@media (min-width: 901px) {
  .prose .fig.wide { width: min(1120px, calc(100vw - 40px)); margin-left: -264px; }
}

/* Experiment log */
.xlog-wrap { display: flex; flex-direction: column; gap: 10px; margin-top: 6px; }
.xlog { width: 100%; border-collapse: collapse; font-size: 15px; }
.xlog caption { text-align: left; font: 500 11px/1 var(--mono); text-transform: uppercase; letter-spacing: .08em; color: var(--ink-2); padding-bottom: 12px; }
.xlog th { text-align: left; font-weight: 600; color: var(--ink-2); font-size: 13px; padding: 10px 12px 10px 0; border-bottom: 1px solid var(--line); }
.xlog td { padding: 12px 12px 12px 0; border-bottom: 1px solid var(--line); vertical-align: top; line-height: 1.45; }
.xlog td:first-child { color: var(--ink-2); font-family: var(--mono); font-size: 13px; width: 36px; }
.xlog b { color: var(--signal-ink); white-space: nowrap; }
.xlog-note { font-size: 15px; }

/* Key decisions (format 2) */
.decisions { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 14px; }
.decisions li { display: grid; grid-template-columns: 56px minmax(0, 1fr); gap: 8px; border: 1px solid var(--line); border-radius: 18px; padding: 24px; }
.prose .decisions li { padding-left: 24px; }
.prose .decisions li::before { display: none; }
.d-n { font: 700 28px/1 var(--display); color: var(--signal-ink); letter-spacing: -0.03em; padding-top: 2px; }
.decisions h3 { font-size: 20px; font-weight: 600; letter-spacing: -0.015em; line-height: 1.3; margin-bottom: 12px; }
.decisions dl { margin: 0; display: flex; flex-direction: column; gap: 8px; }
.decisions dl div { display: grid; grid-template-columns: 96px minmax(0, 1fr); gap: 12px; }
.decisions dt { font: 500 11px/1.9 var(--mono); text-transform: uppercase; letter-spacing: .08em; color: var(--ink-2); }
.decisions dd { margin: 0; font-size: 16px; line-height: 1.5; }

/* Snapshot (format 3) */
.snapshot { display: grid; grid-template-columns: minmax(0, 1.1fr) minmax(0, 1fr); gap: 48px; padding-block: 56px 40px; align-items: start; }
.snap-visual { min-height: 560px; border-radius: var(--radius); display: grid; place-items: center; padding: 24px; text-align: center; background: repeating-linear-gradient(45deg, var(--mist), var(--mist) 12px, #efefea 12px, #efefea 24px); position: sticky; top: 92px; }
.snap-copy { display: flex; flex-direction: column; gap: 22px; }
.snap-copy h1 { font-size: clamp(34px, 4vw, 52px); font-weight: 700; }
.snap-copy .dek { font-size: 19px; color: var(--ink-2); }
.snap-meta, .snap-lines { margin: 0; display: flex; flex-direction: column; border-top: 1px solid var(--line); }
.snap-meta div, .snap-lines div { display: grid; grid-template-columns: 110px minmax(0, 1fr); gap: 12px; padding-block: 12px; border-bottom: 1px solid var(--line); }
.snap-meta dt, .snap-lines dt { font: 500 11px/1.9 var(--mono); text-transform: uppercase; letter-spacing: .08em; color: var(--ink-2); }
.snap-meta dd, .snap-lines dd { margin: 0; font-size: 16px; line-height: 1.5; }
.snap-stats { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
.snap-stats div { background: var(--signal-soft); border-radius: 14px; padding: 16px; display: flex; flex-direction: column; gap: 6px; }
.snap-stats b { font: 700 28px/1 var(--display); color: var(--signal-ink); }
.snap-stats span { font-size: 14px; }
.deep { border: 1px solid var(--line); border-radius: 18px; padding: 0 24px; }
.deep summary { cursor: pointer; font-weight: 600; padding-block: 20px; }
.deep .prose { padding-bottom: 24px; }

.next-ph { width: 220px; aspect-ratio: 16 / 10; border-radius: 12px; display: grid; place-items: center; background: var(--mist); color: var(--ink-2); font-weight: 600; }

/* Review note */
.todo { padding-top: 72px; }
.todo-card { border: 1.5px dashed #d9a400; background: #fffaf0; border-radius: 18px; padding: 24px 28px; }
.todo-card .eyebrow { color: #6b4e00; margin-bottom: 12px; }
.todo-card ol { margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 8px; color: var(--ink); }

@media (max-width: 900px) {
  .meta.meta5 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .tldr { grid-template-columns: 1fr; }
  .snapshot { grid-template-columns: 1fr; gap: 28px; }
  .snap-visual { position: static; min-height: 280px; }
}
@media (max-width: 560px) {
  .tldr-lines, .tldr-stats { padding: 22px; }
  .tldr-lines div, .decisions dl div, .snap-meta div, .snap-lines div { grid-template-columns: 1fr; gap: 2px; }
  .decisions li { grid-template-columns: 1fr; padding: 20px; }
  .snap-stats { grid-template-columns: 1fr; }
  .xlog th:nth-child(3), .xlog td:nth-child(3) { display: none; }
  .formatbar a { padding: 8px 10px; }
  .formatbar a span { display: none; }
  .next-ph { width: 100%; }
}
"""


def build():
    os.makedirs(OUT, exist_ok=True)
    shutil.copy(os.path.join(A, "style.css"), os.path.join(OUT, "style.css"))
    shutil.copy(os.path.join(A, "script.js"), os.path.join(OUT, "script.js"))
    open(os.path.join(OUT, "case.css"), "w").write(CSS)
    for name, html in [("trellis.html", TRELLIS), ("carv.html", CARV), ("hospitable.html", HOSP)]:
        open(os.path.join(OUT, name), "w").write(html)
    print("built cases")


if __name__ == "__main__":
    build()
