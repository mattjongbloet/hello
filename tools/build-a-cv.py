"""Build three iterations of Direction A with copy from Matt's CV (2024) and his current title,
Senior Staff Product Designer at Hospitable. Each tries a different answer to the large photo on the right:
  a6-text-first   — no big photo: a small avatar chip, the headline takes the width
  a7-work-first   — the PMI case study takes the photo's place
  a8-at-a-glance  — small portrait; a CV-style "at a glance" card on the right
All in Roobert (A's type). Re-run after changing A:  python3 tools/build-a-cv.py
"""
import os, re, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "redesigns", "a-clarity")
CV = "https://cdn.prod.website-files.com/63b35214bc1dc0317e22bd99/668ae1b79c5572bfad32e508_Matt_Jongbloet_CV_2024.pdf"


def rep(s, a, b, where):
    assert a in s, f"{where}: missing {a[:80]!r}"
    return s.replace(a, b)


CONTACT_OLD = "<p>Product design, research, or a problem that needs simplifying. I’m in Amsterdam (CET).</p>"
CONTACT_NEW = "<p>I’m looking for opportunities where I can help teams build the right thing, and build it right. I’m in Amsterdam (CET).</p>"

XP_HOME = """<ul class="xp">
          <li><span class="role">Senior Staff Product Designer</span><span class="when num">Now</span><a class="co" href="https://hospitable.com/">Hospitable</a><span class="did">Helping hosts run their short-term rentals on autopilot.</span></li>
          <li><span class="role">Lead Product Designer</span><span class="when num">Feb 2024 — Mar 2025</span><a class="co" href="https://www.carv.com/">Carv</a><span class="did">Helping recruiters cut admin and boost hires.</span></li>
          <li><span class="role">Staff Product Designer</span><span class="when num">Jan 2023 — Jan 2024</span><a class="co" href="https://savvy.insure/">Trellis / Savvy.Insure</a><span class="did">$3.5MM in predicted gross annual revenue from 3 months of growth experiments.</span></li>
          <li><span class="role">Senior Product Designer</span><span class="when num">Dec 2020 — Dec 2022</span><span class="co">Homebot</span><span class="did">Seven projects, research to dev-ready design, for ≈10 million users.</span></li>
        </ul>"""

XP_ABOUT = """<ul class="xp">
          <li><span class="role">Senior Staff Product Designer</span><span class="when num">Now</span><a class="co" href="https://hospitable.com/">Hospitable</a><span class="did">Helping hosts run their short-term rentals on autopilot.</span></li>
          <li><span class="role">Lead Product Designer</span><span class="when num">Feb 2024 — Mar 2025</span><a class="co" href="https://www.carv.com/">Carv</a><span class="did">Helping recruiters cut admin and boost hires. Led design with cross-functional partners and the C-level on the future vision, and ran research into customers’ current experience.</span></li>
          <li><span class="role">Staff Product Designer</span><span class="when num">Jan 2023 — Jan 2024</span><a class="co" href="https://savvy.insure/">Trellis / Savvy.Insure</a><span class="did">Making insurance easier for everyone. $3.5MM in predicted gross annual revenue from 3 months of experiments leading the growth team, and a key product pivot with a novel experience worth an extra $500k a year.</span></li>
          <li><span class="role">Senior Product Designer</span><span class="when num">Dec 2020 — Dec 2022</span><span class="co">Homebot</span><span class="did">Helping homeowners make smarter financial decisions. The full design lifecycle on 7 projects for ≈10 million users, and research with more than 500 participants.</span></li>
          <li><span class="role">Lead Designer</span><span class="when num">Jan 2015 — Dec 2020</span><span class="co">Evolver / The Alchemist’s Kitchen</span><span class="did">User research, digital strategy, campaigns, branding, art direction, e-commerce and UX/UI.</span></li>
          <li><span class="role">Co-Founder</span><span class="when num">May 2016 — Dec 2019</span><span class="co">Humantra</span><span class="did">With two fellow creatives, designed the graphics, website and video that crowdfunded an ethical clothing start-up.</span></li>
          <li><span class="role">UX Designer</span><span class="when num">Nov 2014 — Jun 2015</span><span class="co">Creative Heads Agency</span><span class="did">User research, workshops, branding and websites.</span></li>
          <li><span class="role">Lead Designer</span><span class="when num">Jun 2012 — 2014</span><span class="co">Luker Lighting Technologies</span><span class="did">Creative lead for the UK’s largest hydroponics retailer: UI, research, e-commerce and branding.</span></li>
        </ul>"""

SHARED = {
    "index.html": [
        ("<title>Matt Jongbloet — Product Designer</title>", "<title>Matt Jongbloet — Senior Staff Product Designer</title>"),
        ('content="Product designer and UX researcher with 10+ years of experience, currently leading design at Hospitable."',
         'content="Senior Staff Product Designer at Hospitable, with over ten years in digital product design and an MSc in Digital Design."'),
        ("""    <div class="facts">
      <div><b class="num">10+ years</b><span>in product design</span></div>
      <div><b>MSc, Cum Laude</b><span>Digital Design</span></div>
      <div><b>UXC</b><span>Nielsen Norman Group</span></div>
      <div><b>5 years</b><span>sharpening my research practice</span></div>
    </div>""",
         """    <div class="facts">
      <div><b class="num">$3.5MM</b><span>predicted annual revenue from 3 months of experiments (Trellis)</span></div>
      <div><b class="num">+$500k</b><span>a year from a product pivot I led (Trellis)</span></div>
      <div><b class="num">≈10M</b><span>users of the products I designed (Homebot)</span></div>
      <div><b class="num">500+</b><span>research participants (Homebot)</span></div>
    </div>"""),
        ("""<h2 style="font-size:clamp(30px,3.4vw,44px)">Five years of brand design taught me what I didn’t want to make.</h2>
        <p>Nice-looking things without a purpose. So I moved from Canterbury to Amsterdam for an <strong>MSc in Digital Design</strong>, learned lab, field and showroom research, and spent <strong>5+ years in the US</strong> designing at early- and mid-stage SaaS companies. Now I’m back in Amsterdam.</p>""",
         """<h2 style="font-size:clamp(30px,3.4vw,44px)">It began with street art: colour, composition and form.</h2>
        <p>It’s all about communicating a message that’s <strong>clear, concise and beautiful</strong>. Today that means understanding the problem through empathy, user research and strategy before designing the solution. I have an <strong>MSc in Digital Design</strong> and over ten years in digital product design.</p>"""),
        ("Recent roles</p>", "Recent roles</p>"),
        (CONTACT_OLD, CONTACT_NEW),
    ],
    "case-pmi.html": [
        ("<div><dt>Team</dt><dd>Consumer Team</dd></div>", "<div><dt>Role</dt><dd>Senior Product Designer</dd></div>"),
        (CONTACT_OLD, CONTACT_NEW),
    ],
    "about.html": [
        ('<h1 style="margin-top:16px">Design with a purpose, backed by research.</h1>',
         '<h1 style="margin-top:16px">Build the right thing, and build it right.</h1>'),
        ("<p>I’m Matt, a product designer and UX researcher with more than ten years in product design. I live in Amsterdam and lead design at Hospitable.</p>",
         "<p>I’m Matt, a rigorously curious Senior Staff Product Designer at Hospitable who enjoys simplifying the complex through design. I live in Amsterdam.</p>"),
        ("""<p style="font-size:24px;line-height:1.4;color:var(--ink);font-weight:500">I always knew I wanted to use design to make people’s lives a little better. The first five years of my career, in visual and brand design, left me feeling like I was making nice-looking things without a purpose.</p>""",
         """<p style="font-size:24px;line-height:1.4;color:var(--ink);font-weight:500">It began with street art: colour, composition and form. It’s all about communicating a message that’s clear, concise and beautiful. How do you get there?</p>
      <p>I always knew I wanted to use design to make people’s lives a little better. The first years of my career, in visual and brand design, left me feeling like I was making nice-looking things without a purpose.</p>"""),
        ("""at <a href="https://hospitable.com/">Hospitable</a>.</p>""",
         """at <a href="https://hospitable.com/">Hospitable</a>.</p>
      <p>My work centres on understanding the problem deeply, through empathy, user research and strategy, before designing the solution. I feel an obligation to myself, my colleagues and my clients to put my experience, energy and empathy into something valuable, well executed, and that resonates with the people it’s for.</p>"""),
        ("Leading design for software that runs short-term rentals on autopilot.", "Senior Staff Product Designer on software that runs short-term rentals on autopilot."),
        ("""          <div><b>MSc Digital Design, Cum Laude</b><span>Amsterdam</span></div>
          <div><b>UX Certification (UXC)</b><span>Nielsen Norman Group</span></div>
          <div><b>10+ years</b><span>in product design, 5 of them sharpening my research practice</span></div>""",
         """          <div><b>MSc Digital Design · 8.6, Cum Laude</b><span>Amsterdam University of Applied Sciences, 2017–2018</span></div>
          <div><b>UX Certificate (UXC)</b><span>Nielsen Norman Group, 2022: Statistics for UX, Ethnographic UX Research, Discoveries, Facilitating UX Workshops, Managing UX Strategy</span></div>
          <div><b>BA Graphic Design &amp; Visual Arts</b><span>University of Greenwich, UK, 2009–2012</span></div>"""),
        ("""</main>""", """  <section class="wrap section">
    <div class="split">
      <div>
        <div class="section-head" style="margin-bottom:24px"><h2>Tools</h2></div>
        <p class="taglist"><span>Figma</span><span>Miro</span><span>Dovetail</span><span>Lookback</span><span>UserTesting</span><span>User Interviews</span><span>Amplitude</span><span>Looker</span><span>FullStory</span><span>Adobe CC</span><span>Shopify</span><span>WordPress</span><span>Klaviyo</span></p>
      </div>
      <div>
        <div class="section-head" style="margin-bottom:24px"><h2>Outside work</h2></div>
        <p class="taglist"><span>Meditation</span><span>Hiking</span><span>Cycling</span><span>Reading</span><span>Chocolate</span><span>Coffee</span><span>Tech</span><span>Psychology</span><span>Philosophy</span><span>Storytelling</span></p>
      </div>
    </div>
  </section>
</main>"""),
        (CONTACT_OLD, CONTACT_NEW),
    ],
}

PORTFOLIO = "https://www.mjongbloet.com/portfolio"
PROJECTS = {
    "trellis": ("../cases/trellis.html", "trellis/savvy-logo.png", "Trellis / Savvy.Insure", "Growth experiments", "Finding $3.5MM in predicted annual revenue in a car insurance quote flow", "trellis/cover-v2.jpg", "Read the case study →"),
    "pmi": ("case-pmi.html", "homebot-logo.png", "Homebot", "Private Mortgage Insurance (PMI)", "Helping ≈1M US homeowners save an estimated $200M a month", "pmi-mockup.png", "Read the case study →"),
    "search": (PORTFOLIO + "/home-search", "homebot-logo.png", "Homebot", "Home Search", "Helping ≈10 million people find their next home", "home-search.jpg", "See project ↗"),
    "admin": (PORTFOLIO + "/internal-admin", "homebot-logo.png", "Homebot", "Internal Admin", "Cutting the time for 20+ key admin tasks by ≈80%", "internal-admin.jpg", "See project ↗"),
    "research": (PORTFOLIO, "homebot-logo.png", "Homebot", "Scaling Research", "Empowering 30+ product people to learn in rigorous ways", "scaling-research.png", "See project ↗"),
    "health": (PORTFOLIO, "humanapi-logo.png", "Human API", "Digital Health", "Helping convince investors with a compelling story and prototype", "digital-health.jpg", "See project ↗"),
    "value": (PORTFOLIO, "homebot-logo.png", "Homebot", "Home Value Estimates", "Increasing trust and confidence in home value estimates", "home-value.png", "See project ↗"),
    "wwf": (PORTFOLIO, "wwf-logo.png", "WWF", "Location-Based Game", "Using technology to enhance nature experiences for families", "wwf-game.jpg", "See project ↗"),
}


def card(key, wide=False):
    href, logo, co, title, line, shot, more = PROJECTS[key]
    more_html = f'\n          <span class="pc-more">{more}</span>' if wide else ""
    return f"""      <a class="pcard{' pcard-wide' if wide else ''} reveal" href="{href}">
        <div class="pc-copy">
          <img class="pc-logo" src="../assets/{logo}" alt="">
          <span class="pc-co">{co}</span>
          <h3>{title}</h3>
          <p>{line}</p>{more_html}
        </div>
        <div class="pc-shot"><img src="../assets/{shot}" alt="" loading="lazy"></div>
      </a>"""


def work(order):
    cards = "\n".join(card(k, wide=(i == 0)) for i, k in enumerate(order))
    return f"""  <section class="work-band" id="work">
    <div class="wrap">
      <div class="section-head">
        <h2>Selected work</h2>
        <a href="{PORTFOLIO}">All projects →</a>
      </div>
      <div class="pcards">
{cards}
      </div>
    </div>
  </section>"""


ORDER = ["trellis", "pmi", "search", "admin", "research", "health", "value"]
WORK = {"a6-text-first": ORDER, "a8-at-a-glance": ORDER,
        # A7 already features PMI in the hero, so its list leaves PMI out.
        "a7-work-first": ["trellis", "search", "admin", "research", "health", "value", "wwf"]}

ACTIONS = """      <div class="actions">
        <a class="btn" href="#work">See my work</a>
        <a class="btn ghost" href="about.html">More about me</a>
      </div>"""

HEROES = {
    "a6-text-first": f"""  <section class="wrap hero hero-text">
    <div class="hero-copy">
      <p class="who-chip"><img src="../assets/headshot.jpg" alt=""><span><b>Matt Jongbloet</b> · Senior Staff Product Designer at <a href="https://hospitable.com/">Hospitable</a></span></p>
      <h1>I help teams build the right thing, <em>and build it right.</em></h1>
      <p class="lede">Hi, I’m Matt, a rigorously curious product designer who enjoys simplifying the complex through design. Over ten years in digital product design, an MSc in Digital Design, and a research practice I keep sharpening.</p>
{ACTIONS}
    </div>
  </section>""",
    "a7-work-first": f"""  <section class="wrap hero hero-work">
    <div class="hero-copy">
      <p class="eyebrow">Senior Staff Product Designer at Hospitable · Amsterdam</p>
      <h1>I make complex products <em>feel simple.</em></h1>
      <p class="lede">Hi, I’m Matt, a rigorously curious designer who helps teams build the right thing, and build it right: from user research and strategy to dev-ready design.</p>
{ACTIONS}
    </div>
    <a class="hero-case" href="case-pmi.html">
      <img src="../assets/pmi-mockup.png" alt="Two phone screens from the PMI feature: a removal progress bar and ways to remove PMI faster">
      <span class="tag"><span class="eyebrow">Featured case study · Homebot</span><b>Helping ≈1M homeowners drop mortgage insurance early</b><span class="num">≈$200M a month in estimated savings →</span></span>
    </a>
  </section>""",
    "a8-at-a-glance": f"""  <section class="wrap hero hero-glance">
    <div class="hero-copy">
      <img class="portrait-sm" src="../assets/headshot.jpg" alt="Matt Jongbloet">
      <h1>Hi, I’m Matt. I simplify the complex <em>through design.</em></h1>
      <p class="lede">A rigorously curious Senior Staff Product Designer at <strong>Hospitable</strong>. I’m at my best helping teams build the right thing, and build it right.</p>
{ACTIONS}
    </div>
    <aside class="glance" aria-label="At a glance">
      <p class="eyebrow">At a glance</p>
      <dl>
        <div><dt>Now</dt><dd>Senior Staff Product Designer, Hospitable</dd></div>
        <div><dt>Before</dt><dd>Carv · Trellis · Homebot</dd></div>
        <div><dt>Experience</dt><dd>10+ years in digital product design</dd></div>
        <div><dt>Education</dt><dd>MSc Digital Design, Cum Laude · NN/g UX Certificate</dd></div>
        <div><dt>Based</dt><dd>Amsterdam, NL (CET)</dd></div>
      </dl>
      <a class="glance-cv" href="{CV}">Full resume (PDF) ↗</a>
    </aside>
  </section>""",
}

SHARED_CSS = """/* Iterations on A with CV copy (tools/build-a-cv.py). Shared additions first, then this iteration's hero. */
.xp .did { grid-column: 1 / -1; color: var(--ink-2); font-size: 15px; line-height: 1.45; margin-top: 2px; }
.xp span.co { color: var(--ink-2); font-size: 15px; }
.facts span { line-height: 1.4; }
.taglist { display: flex; flex-wrap: wrap; gap: 8px; margin: 0; }
.taglist span { padding: 8px 14px; border-radius: 999px; background: var(--mist); font-size: 15px; }

/* Project cards, as on Matt's current site: white card, logo tile, one line, screenshot bleeding off the bottom-right. */
.work-band { background: #f7f7f6; margin-top: 96px; padding-block: 88px 96px; }
.pcards { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px; }
.pcard { display: flex; flex-direction: column; background: var(--paper); border: 1px solid #ebebe8; border-radius: 24px; overflow: hidden; text-decoration: none; color: var(--ink); padding: 44px 0 0 44px; transition: transform .25s ease, box-shadow .25s; }
.pcard:hover { transform: translateY(-3px); box-shadow: 0 20px 44px -26px rgb(20 20 20 / .3); }
.pc-copy { display: flex; flex-direction: column; gap: 4px; padding-right: 44px; }
.pc-logo { width: 64px; height: 64px; border-radius: 16px; margin-bottom: 20px; }
.pc-co { font-size: 16px; color: var(--ink-2); }
.pcard h3 { font-size: clamp(22px, 2vw, 28px); font-weight: 500; letter-spacing: -0.02em; line-height: 1.2; margin-top: 6px; }
.pcard p { font-size: 17px; color: var(--ink-2); line-height: 1.55; max-width: 36ch; margin-top: 4px; }
.pc-more { margin-top: 20px; font-size: 17px; font-weight: 500; }
.pc-shot { margin-top: 36px; background: #e8e8e8; border-top-left-radius: 20px; overflow: hidden; aspect-ratio: 16 / 10; }
.pc-shot img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 0; transition: transform .4s ease; }
.pcard:hover .pc-shot img { transform: scale(1.02); }
.pcard-wide { grid-column: 1 / -1; display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.2fr); padding: 0; }
.pcard-wide .pc-copy { padding: 56px 44px; align-self: center; }
.pcard-wide .pc-shot { margin-top: 64px; aspect-ratio: auto; height: 400px; align-self: end; }
.pcard-wide .pc-shot img { object-position: 0 0; }
@media (max-width: 760px) {
  .work-band { margin-top: 64px; padding-block: 64px; }
  .pcards { grid-template-columns: 1fr; gap: 16px; }
  .pcard, .pcard-wide { display: flex; padding: 28px 0 0 28px; }
  .pc-copy, .pcard-wide .pc-copy { padding: 0 28px 0 0; }
  .pcard-wide .pc-shot { margin-top: 28px; height: auto; aspect-ratio: 16 / 10; align-self: stretch; }
  .pc-shot { margin-top: 28px; }
  .pc-logo { width: 52px; height: 52px; border-radius: 14px; margin-bottom: 14px; }
}
"""

CHIP = '<p class="who-chip"><img src="../assets/headshot.jpg" alt=""><span><b>Matt Jongbloet</b> · Senior Staff Product Designer at <a href="https://hospitable.com/">Hospitable</a></span></p>'
SHINE = "a rigorously curious product designer with 15 years’ experience helping people and businesses shine"

# Iterations on A6 (Matt's favourite): icon-only header, and each leads with a different line he likes.
HEROES.update({
    "a6-1-feel-simple": f"""  <section class="wrap hero hero-text">
    <div class="hero-copy">
      {CHIP}
      <h1>I make complex products <em>feel simple.</em></h1>
      <p class="lede">I’m {SHINE}. I’m happiest when people succeed with what I design.</p>
{ACTIONS}
    </div>
  </section>""",
    "a6-2-through-design": f"""  <section class="wrap hero hero-text hero-split">
    <div class="hero-copy">
      {CHIP}
      <div class="hs-grid">
        <h1>I simplify the complex <em>through design.</em></h1>
        <div class="hs-side">
          <p class="lede">I’m {SHINE}. I’m happiest when people succeed with what I design.</p>
{ACTIONS}
        </div>
      </div>
    </div>
  </section>""",
    "a6-3-people-succeed": f"""  <section class="wrap hero hero-text hero-center">
    <div class="hero-copy">
      {CHIP}
      <h1>I’m happiest when people succeed <em>with what I design.</em></h1>
      <p class="lede">I’m {SHINE}. I make complex products feel simple.</p>
{ACTIONS}
    </div>
  </section>""",
})
ICON_ONLY = {"a6-1-feel-simple", "a6-2-through-design", "a6-3-people-succeed"}
BRAND_OLD = '<a class="brand" href="index.html"><img class="mark" src="../assets/mj-logo.svg" alt="">Matt Jongbloet</a>'
BRAND_ICON = '<a class="brand" href="index.html" aria-label="Matt Jongbloet, home"><img class="mark" src="../assets/mj-logo.svg" alt=""></a>'
for _k in ICON_ONLY:
    WORK[_k] = ORDER

ITER_CSS = {
    "a6-text-first": """
/* A6 — Text first: no big photo; the headline gets the full width. */
.hero.hero-text { grid-template-columns: 1fr; padding-block: 96px 80px; }
.hero-text h1 { font-size: clamp(44px, 7vw, 96px); max-width: 15ch; }
.hero-text .lede { max-width: 52ch; }
.who-chip { display: inline-flex; align-items: center; gap: 10px; align-self: flex-start; padding: 6px 16px 6px 6px; border-radius: 999px; background: var(--mist); font-size: 15px; color: var(--ink-2); }
.who-chip img { width: 36px; height: 36px; border-radius: 50%; object-fit: cover; }
.who-chip b { color: var(--ink); font-weight: 600; }
.who-chip a { color: var(--ink); }
.ab-hero { grid-template-columns: 1fr; }
.ab-hero .portrait { display: none; }
.ab-hero h1 { max-width: 14ch; }
@media (max-width: 560px) { .who-chip { border-radius: 18px; align-items: flex-start; } .who-chip span { padding-top: 7px; } }
""",
    "a7-work-first": """
/* A7 — Work first: the PMI case study replaces the photo. */
.hero.hero-work { grid-template-columns: minmax(0, 1fr) minmax(0, 1.05fr); align-items: center; }
.hero-work h1 { font-size: clamp(40px, 5.2vw, 68px); max-width: 13ch; }
.hero-case { position: relative; display: block; border-radius: var(--radius); overflow: hidden; background: #e8e8e8; text-decoration: none; transition: transform .25s ease, box-shadow .25s; }
.hero-case:hover { transform: translateY(-3px); box-shadow: 0 18px 40px -24px rgb(20 20 20 / .35); }
.hero-case img { width: 100%; aspect-ratio: 16 / 11; object-fit: cover; }
.hero-case .tag { position: absolute; left: 14px; right: 14px; bottom: 14px; background: var(--paper); border-radius: 12px; padding: 14px 16px; display: flex; flex-direction: column; gap: 4px; box-shadow: 0 10px 30px -12px rgb(0 0 0 / .35); }
.hero-case .tag .eyebrow { color: var(--signal-ink); margin-bottom: 4px; }
.hero-case .tag b { font-size: 17px; line-height: 1.3; }
.hero-case .tag .num { font-size: 14px; color: var(--ink-2); }
.ab-hero .portrait { max-width: 320px; }
@media (max-width: 900px) { .hero-case img { aspect-ratio: 4 / 3; } }
@media (max-width: 560px) { .hero-case .tag { position: static; border-radius: 0; box-shadow: none; } }
""",
    "a8-at-a-glance": """
/* A8 — At a glance: a small portrait, and a CV-style summary card instead of the big photo. */
.hero.hero-glance { grid-template-columns: minmax(0, 1.45fr) minmax(0, 1fr); align-items: end; }
.portrait-sm { width: 88px; height: 88px; border-radius: 22px; object-fit: cover; object-position: 50% 30%; }
.hero-glance h1 { font-size: clamp(40px, 5.6vw, 72px); max-width: 14ch; }
.glance { border: 1px solid var(--line); border-radius: var(--radius); padding: 28px; display: flex; flex-direction: column; gap: 14px; background: var(--paper); }
.glance dl { margin: 0; display: flex; flex-direction: column; }
.glance dl div { display: grid; grid-template-columns: 96px minmax(0, 1fr); gap: 12px; padding-block: 12px; border-top: 1px solid var(--line); }
.glance dt { font: 500 11px/1.9 var(--mono); text-transform: uppercase; letter-spacing: .08em; color: var(--ink-2); }
.glance dd { margin: 0; font-size: 15px; line-height: 1.45; }
.glance-cv { font-weight: 600; font-size: 15px; text-decoration: none; align-self: flex-start; padding-block: 6px; }
.glance-cv:hover { color: var(--signal-ink); }
.ab-hero .portrait { max-width: 260px; border-radius: 28px; }
@media (max-width: 560px) { .glance { padding: 20px; } .glance dl div { grid-template-columns: 1fr; gap: 2px; } }
""",
}


ICON_CSS = """
/* Icon-only header: the name now lives in the hero chip, so the mark stands alone and a little larger. */
.brand img.mark { height: 42px; }
"""
ITER_CSS["a6-1-feel-simple"] = ITER_CSS["a6-text-first"] + ICON_CSS + """
/* A6.1 — A6's layout, leading with “I make complex products feel simple.” */
.hero-text h1 { max-width: 14ch; }
"""
ITER_CSS["a6-2-through-design"] = ITER_CSS["a6-text-first"] + ICON_CSS + """
/* A6.2 — Lighter headline (Medium), with the intro and buttons set beside it. */
.hero-split .hs-grid { display: grid; grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr); gap: 56px; align-items: end; }
.hero-split h1 { font-weight: 500; letter-spacing: -0.035em; font-size: clamp(44px, 6.6vw, 90px); max-width: 12ch; }
.hero-split .hs-side { display: flex; flex-direction: column; gap: 24px; padding-bottom: 10px; }
.hero-split .lede { font-size: 18px; }
@media (max-width: 900px) { .hero-split .hs-grid { grid-template-columns: 1fr; gap: 28px; } }
"""
ITER_CSS["a6-3-people-succeed"] = ITER_CSS["a6-text-first"] + ICON_CSS + """
/* A6.3 — Centred hero, leading with “I’m happiest when people succeed with what I design.” */
.hero-center .hero-copy { align-items: center; text-align: center; }
.hero-center .who-chip { align-self: center; text-align: left; }
.hero-center h1 { font-size: clamp(40px, 6vw, 82px); max-width: 17ch; }
.hero-center .lede { max-width: 54ch; }
.hero-center .actions { justify-content: center; }
"""


def build():
    hero_re = re.compile(r'  <section class="wrap hero">.*?\n  </section>', re.S)
    work_re = re.compile(r'  <section class="wrap section" id="work">.*?\n  </section>', re.S)
    xp_re = re.compile(r'<ul class="xp">.*?</ul>', re.S)
    for name, hero in HEROES.items():
        out = os.path.join(ROOT, "redesigns", name)
        os.makedirs(out, exist_ok=True)
        shutil.copy(os.path.join(A, "style.css"), os.path.join(out, "style.css"))
        shutil.copy(os.path.join(A, "script.js"), os.path.join(out, "script.js"))
        for page in ["index.html", "case-pmi.html", "about.html"]:
            s = open(os.path.join(A, page)).read()
            for a, b in SHARED[page]:
                s = rep(s, a, b, f"{name}/{page}")
            if page == "index.html":
                assert len(hero_re.findall(s)) == 1, name
                s = hero_re.sub(lambda m: hero, s)
                assert len(work_re.findall(s)) == 1, name
                s = work_re.sub(lambda m: work(WORK[name]), s)
                s = xp_re.sub(lambda m: XP_HOME, s)
            if page == "about.html":
                s = xp_re.sub(lambda m: XP_ABOUT, s)
            if name in ICON_ONLY:
                s = rep(s, BRAND_OLD, BRAND_ICON, f"{name}/{page}")
            s = rep(s, '<link rel="stylesheet" href="style.css">', '<link rel="stylesheet" href="style.css">\n<link rel="stylesheet" href="variant.css">', f"{name}/{page}")
            open(os.path.join(out, page), "w").write(s)
        open(os.path.join(out, "variant.css"), "w").write(SHARED_CSS + ITER_CSS[name])
        print("built", name)


if __name__ == "__main__":
    build()
