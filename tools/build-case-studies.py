"""Matt's chosen case-study format, applied to every case study:
  opening  — title, intro, facts row, cover image, five metric tiles      (from layout 4, "Visual story")
  body     — contents menu on the left; Context → Opportunity → Approach → Outcome   (from layout 1, "Impact first")
Pages: case-studies/pmi.html, trellis.html (full); carv.html, hospitable.html (templates with placeholders).
Copy for PMI comes from tools/build-pmi-formats.py, shared pieces from tools/build-cases.py.
Re-run: python3 tools/build-case-studies.py
"""
import importlib.util, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, file))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


sys.path.insert(0, HERE)
import site_parts as sp
bc = load("build_cases", "build-cases.py")
pf = load("build_pmi_formats", "build-pmi-formats.py")
ph, HOME, IMG = bc.ph, bc.HOME, "../assets/"
T = IMG + "trellis/"
A = os.path.join(ROOT, "redesigns", "a-clarity")
OUT = os.path.join(ROOT, "redesigns", "case-studies")
SITE = "../site/"

def head(title, desc):
    h = bc.head(title, desc)
    assert len(sp.HEADER_RE.findall(h)) == 1
    h = sp.HEADER_RE.sub(lambda m: sp.header(HOME, "work"), h)
    h = h.replace("</head>", sp.THEME_HEAD + "\n</head>")
    return h.replace('<link rel="stylesheet" href="case.css">', '<link rel="stylesheet" href="case.css">\n<link rel="stylesheet" href="format.css">')


def opening(crumb, title, dek, meta, cover, tiles):
    t = "".join(f'<div><b class="num">{n}</b><span>{label}</span></div>' for n, label in tiles)
    return f"""  <section class="wrap cs-hero">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{HOME}index.html#work">Work</a><span>/</span><span>{crumb}</span></nav>
    <h1>{title}</h1>
    <p class="dek">{dek}</p>
    {bc.meta(meta)}
  </section>

  <div class="wrap">
    {cover}
    <div class="results five">{t}</div>
  </div>
"""


def body(sections):
    """sections: list of (id, label, heading, html)."""
    toc = "".join(f'<a href="#{i}"{" class=\"on\"" if k == 0 else ""}>{label}</a>' for k, (i, label, _, _) in enumerate(sections))
    secs = "".join(f"""
      <section id="{i}">
        <p class="eyebrow">{label}</p>
        <h2>{h}</h2>
        {html}
      </section>""" for i, label, h, html in sections)
    return f"""
  <div class="wrap cs-body">
    <nav class="toc" aria-label="Contents">
      <span class="eyebrow">Contents</span>
      {toc}
    </nav>
    <article class="prose">{secs}
    </article>
  </div>
"""


def nextp(href, title, visual):
    return f"""
  <div class="wrap next">
    <a href="{href}">
      <div><p class="eyebrow">Next project</p><h3>{title}</h3></div>
      {visual}
    </a>
  </div>
"""


def page(title, desc, main, todo=""):
    html = head(title, desc) + "\n<main>\n" + main + "</main>\n" + todo + bc.FOOT
    return html.replace(HOME, SITE)  # these pages belong to Matt's chosen home page, A6.1


def ul(*items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


# ---------------- PMI ----------------
PMI = page("PMI Savings — Matt Jongbloet", "Helping ≈1 million US homeowners discover they can drop private mortgage insurance early.",
    opening("Homebot", pf.TITLE, pf.DEK, pf.META,
            f'<div class="cs-cover has-dark"><img src="{IMG}pmi-mockup.png" data-dark="{IMG}pmi-mockup-dark.png" alt="{pf.COVER_ALT}"></div>',
            [("≈$200M", "a month in estimated savings for homeowners"), ("≈1M", "US homeowners on Homebot eligible to remove PMI early"), ("$195", "estimated monthly saving per homeowner"),
             ("4.8/5", "rating for value and confidence in usability testing"), ("500+", "requests to learn about PMI removal in the first sprint")])
    + body([
        ("context", "Context", "Why it mattered in 2022", ul(pf.LI_PRICES, pf.LI_COVID, pf.LI_PMI) + f'<p class="callout">{pf.CALLOUT}</p>'),
        ("opportunity", "Opportunity", "An opportunity hiding in our data", f"<p>{pf.P_OPPORTUNITY}</p><p>{pf.P_SIZE}</p>"),
        ("approach", "Approach", "Prototype widely, test hard, ship in slices", ul(pf.LI_EXPLORE, pf.LI_TEST, pf.LI_PLAN) + pf.FIG_PAIR),
        ("outcome", "Outcome", "500 requests in the first sprint", ul(pf.LI_REQUESTS, pf.LI_PRESENT) + pf.VIDEO),
    ])
    + nextp("trellis.html", "Trellis: growth experiments", f'<img src="{T}cover-v2.jpg" alt="">'))

# ---------------- Trellis ----------------
XLOG = f"""<div class="xlog-wrap">
          <table class="xlog">
            <caption>Experiment log</caption>
            <thead><tr><th scope="col">#</th><th scope="col">Change</th><th scope="col">Hypothesis</th><th scope="col">Result</th></tr></thead>
            <tbody>
              <tr><td class="num">01</td><td>Re-order the application</td><td>Asking for the car before contact details will raise completion.</td><td><b class="num">60.4% → 69.0%</b></td></tr>
              <tr><td class="num">02</td><td>{ph("Experiment")}</td><td>{ph("We think … will …")}</td><td>{ph("Result")}</td></tr>
              <tr><td class="num">03</td><td>{ph("Experiment")}</td><td>{ph("We think … will …")}</td><td>{ph("Result")}</td></tr>
            </tbody>
          </table>
          <p class="xlog-note">{ph("Add 4–6 of the ~15. Losing tests are worth including: they show the judgment.")}</p>
        </div>"""


def fig(src, alt, cap, wide=False):
    return f'<figure class="fig{" wide" if wide else ""}"><a class="frame light" href="{T}{src}"><img src="{T}{src}" alt="{alt}" loading="lazy"></a><figcaption>{cap}</figcaption></figure>'


TRELLIS = page("Trellis: Growth experiments — Matt Jongbloet", "In 3 months, a small growth team and I ran experiments on around 15 parts of Savvy’s car insurance quote flow: $3.5MM in predicted gross annual revenue.",
    opening("Trellis", "Finding $3.5MM in a car insurance quote flow",
            "In three months, a small growth team and I ran experiments on around 15 parts of Savvy’s car insurance quote flow, and proved we could get more people from “I want a quote” to “here are my offers”.",
            [("Company", "Trellis / Savvy.Insure"), ("My role", "Staff Product Designer, leading design for the growth team"), ("Team", "1 front-end engineer, 1 back-end engineer, 1 growth engineering consultant"), ("Timeframe", "3 months, 2023"), ("Surface", "Car insurance quote flow")],
            f'<a class="cover" href="{T}flow-v2.jpg"><img src="{T}cover-v2.jpg" alt="The re-ordered quote flow: vehicle details, your vehicles, tell us about yourself, your drivers, home address"></a>',
            [("$3.5MM", "predicted gross annual revenue"), ("~15", "parts of the quote flow tested"), ("3 months", "from first test to result"),
             ("69.0%", "completion in the winning re-order test, up from 60.4%"), ("+14%", "relative lift in completed applications")])
    + body([
        ("context", "Context", "Where the business wins or loses",
         "<p>Savvy.Insure, by Trellis, set out to make insurance easier for everyone. Someone who wants car insurance comes to Savvy, tells us about themselves, their cars and their drivers, and gets quotes back. That flow is where the business makes or loses money.</p>"),
        ("opportunity", "Opportunity", "Four in ten people gave up before their quote",
         f'<p>From 17 to 31 May 2023, <strong>44,846</strong> people started the unlinked application and <strong>26,333</strong> finished it: a completion rate of <strong>58.7%</strong>. Every drop-off was a quote, and revenue, lost. {ph("Add one line on what “unlinked” means.")}</p>'
         + fig("baseline-chart.jpg", "Bar chart: 44,846 started the unlinked application, 26,333 completed it, 58.7% total conversion, 17 to 31 May 2023", "Baseline, 17–31 May 2023: 58.7% of people who started the application completed it.")),
        ("approach", "Approach", "Learn cheaply, decide with evidence",
         ul("<strong>The cheapest way to learn.</strong> Not every experiment needs to be an A/B test. We framed each change as a hypothesis, picked the lightest method that could confirm or disconfirm it, and used A/B tests where we needed statistical confidence.",
            "<strong>One small team, a steady cadence.</strong> With a front-end engineer, a back-end engineer and a growth engineering consultant, I designed and shipped experiments on around 15 parts of the flow in three months.",
            "<strong>Making it a habit.</strong> I co-wrote and presented <em>How do we make good decisions about product investment?</em>, sharing how we chose methods, from interviews to A/B tests, and why learning matters more than being right.")
         + XLOG
         + '<h3 class="sub">Featured experiment: ask for the car before the phone number</h3>'
         + '<p class="callout">Hypothesis: changing the order of the unlinked application flow will increase conversion.</p>'
         + "<p>The control flow opened by asking for name, phone, email and date of birth, before Savvy had given anything back. V2 starts with the car and the drivers, builds up to the policy, and only asks for contact details at the very end, as <em>“Where should we send your offers?”</em></p>"
         + fig("flow-control.jpg", "Control flow, nine phone screens: basic information with phone and email first, then address, own or rent, vehicle information, vehicles, driver information, drivers, current premium, review", "Control: contact details on the very first screen.", True)
         + fig("flow-v2.jpg", "V2 flow, nine phone screens: vehicle information, vehicles, tell us about yourself, drivers, home address, own or rent, current premium, review, and where should we send your offers", "V2: vehicles and drivers first, contact details last. Stars mark the steps that moved.", True)
         + fig("result-chart.jpg", "Bar chart, 1 to 9 June 2023: control 60.4% (8,108 of 13,419 completed), V2 69.0% (8,498 of 12,319 completed)", "1–9 June 2023: control completed 60.4% (8,108 of 13,419); V2 completed 69.0% (8,498 of 12,319).")),
        ("outcome", "Outcome", "$3.5MM in predicted annual revenue",
         ul("Over three months, the experiments added up to <strong>$3.5MM in predicted gross annual revenue</strong>.",
            f'The re-order test lifted completion by <strong>8.6 points</strong>, a 14% relative improvement. {ph("Did V2 ship to everyone? Say so here.")}',
            "We left the team with the infrastructure to run similar tests with ease, and a shared way of deciding what to build.")
         + '<h3 class="sub">What we learned</h3>'
         + ul("<strong>People need Trellis to feel valuable before they give their info.</strong> Order matters.",
              "<strong>Learning is more important than being right.</strong> Good testing infrastructure means more people share ideas, and it takes the HiPPO out of decisions.")),
    ])
    + nextp("carv.html", "Carv", '<span class="next-ph">Carv</span>'),
    bc.todo(["What “unlinked application” means, in one line.", "The other experiments: change, hypothesis and result for 4–6 of the ~15.",
             "Whether V2 shipped, and anything you know about the effect after launch.", "How the $3.5MM was predicted. One line makes it far more credible."]))


# ---------------- Templates ----------------
def template(crumb, company, role, tagline, next_href, next_title, next_visual, todo_items):
    return page(f"{company} — Matt Jongbloet", "Case study template.",
        opening(crumb, ph("Project title that sells the outcome"), f"{tagline} {ph('One sentence on the project and its result.')}",
                [("Company", company), ("My role", role), ("Team", ph("e.g. PM, 4 engineers, data")), ("Timeframe", ph("e.g. Mar–Sep 2024, 6 months")), ("Surface", ph("e.g. Web app"))],
                f'<div class="cover cover-ph">{ph("Cover image: the shipped product, a key screen or the prototype")}</div>',
                [(ph("00"), ph("headline result")), (ph("00"), ph("result")), (ph("00"), ph("result")), (ph("00"), ph("scope, e.g. users")), (ph("00"), ph("pace, e.g. weeks to ship"))])
        + body([
            ("context", "Context", ph("Why it mattered"), f"<p>{ph('Two or three sentences: the company, the customer and the moment.')}</p>"),
            ("opportunity", "Opportunity", ph("The problem worth solving"), f"<p>{ph('What was broken, for whom, and how big it was. A number helps.')}</p>"),
            ("approach", "Approach", ph("How you got there"),
             ul(f"<strong>{ph('Step')}</strong> {ph('What you did and why.')}", f"<strong>{ph('Step')}</strong> {ph('What you did and why.')}", f"<strong>{ph('Step')}</strong> {ph('What you did and why.')}")
             + f'<div class="cover cover-ph small">{ph("Process visuals: explorations, research, before and after")}</div>'),
            ("outcome", "Outcome", ph("What changed"), ul(ph("The result, with a number."), ph("What happened next, or what you learned."))),
        ])
        + nextp(next_href, next_title, next_visual),
        bc.todo(todo_items))


CARV = template("Carv", "Carv", "Lead Product Designer", "Helping recruiters cut admin and boost hires.", "hospitable.html", "Hospitable", '<span class="next-ph">Hospitable</span>',
                ["Which Carv project to feature, and a title that sells the outcome.", "Team and timeframe.", "Five numbers for the tiles (results, scope, pace).",
                 "Context, opportunity, approach, outcome: a few lines each. Worth including: how you set the future vision with the C-level, and what the research changed.", "Visuals: cover, process, shipped screens."])
HOSP = template("Hospitable", "Hospitable", "Senior Staff Product Designer", "Helping hosts run their short-term rentals on autopilot.", "pmi.html", "PMI Savings", f'<img src="{IMG}pmi-thumb.png" alt="">',
                ["Which Hospitable project to show, and how much you can share.", "Team and timeframe.", "Five numbers for the tiles (or fewer; the row adapts).",
                 "Context, opportunity, approach, outcome: a few lines each.", "Visuals you’re allowed to show (crop or blur where needed)."])

CSS = """/* Matt's case-study format (tools/build-case-studies.py). Adds to style.css + case.css. */
.cs-hero { padding-bottom: 32px; }
.cs-hero h1 { max-width: 19ch; }
.cs-cover, .cover { margin-top: 0; }

/* Five metric tiles under the cover */
.results.five { grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 12px; margin-top: 12px; }
.results.five div { padding: 20px; }
.results.five b { font-size: clamp(26px, 2.6vw, 36px); padding-top: 2px; }
.results.five span { font-size: 14px; }

/* Body */
.cs-body { padding-top: 96px; }
.toc a { border-radius: 0 8px 8px 0; }
.prose h3.sub { font-size: 22px; font-weight: 700; letter-spacing: -0.02em; line-height: 1.25; margin-top: 28px; }
.cover-ph.small { min-height: 220px; border-radius: 14px; }

@media (max-width: 1000px) {
  .results.five { grid-template-columns: repeat(6, minmax(0, 1fr)); }
  .results.five div { grid-column: span 2; }
  .results.five div:nth-child(-n+2) { grid-column: span 3; }
}
@media (max-width: 560px) {
  .results.five { grid-template-columns: 1fr 1fr; }
  .results.five div, .results.five div:nth-child(-n+2) { grid-column: auto; }
  .results.five div:first-child { grid-column: 1 / -1; }
  .results.five b { font-size: 26px; }
}
"""

TOC_JS = """
// Contents menu: highlight the section currently being read (works from the top of the page and on anchor jumps).
(() => {
  const links = [...document.querySelectorAll('.toc a')];
  const secs = links.map((a) => document.getElementById(a.getAttribute('href').slice(1))).filter(Boolean);
  if (!secs.length) return;
  const set = () => {
    let cur = secs[0];
    for (const s of secs) if (s.getBoundingClientRect().top <= 180) cur = s;
    links.forEach((l) => l.classList.toggle('on', l.getAttribute('href') === '#' + cur.id));
  };
  addEventListener('scroll', set, { passive: true }); addEventListener('resize', set); set();
})();
"""


def build():
    os.makedirs(OUT, exist_ok=True)
    shutil.copy(os.path.join(A, "style.css"), os.path.join(OUT, "style.css"))
    js = open(os.path.join(A, "script.js")).read()
    cut = js.index("  const links = [...document.querySelectorAll('.toc a')];")
    open(os.path.join(OUT, "script.js"), "w").write(js[:cut].rstrip() + "\n})();\n" + TOC_JS + sp.THEME_JS)
    open(os.path.join(OUT, "case.css"), "w").write(bc.CSS)
    open(os.path.join(OUT, "format.css"), "w").write(CSS + open(os.path.join(HERE, "type-smaller.css")).read() + sp.HEADER_CSS + sp.DARK_CSS)
    for name, html in [("pmi.html", PMI), ("trellis.html", TRELLIS), ("carv.html", CARV), ("hospitable.html", HOSP)]:
        open(os.path.join(OUT, name), "w").write(html)
    print("built case-studies")


if __name__ == "__main__":
    build()
