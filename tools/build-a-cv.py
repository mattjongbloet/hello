"""Build three iterations of Direction A with copy from Matt's CV (2024) and his current title,
Senior Staff Product Designer at Hospitable. Each tries a different answer to the large photo on the right:
  a6-text-first   — no big photo: a small avatar chip, the headline takes the width
  a7-work-first   — the PMI case study takes the photo's place
  a8-at-a-glance  — small portrait; a CV-style "at a glance" card on the right
All in Roobert (A's type). Re-run after changing A:  python3 tools/build-a-cv.py
"""
import os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import site_parts as sp

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

# The current site's home page: rows with company logos, condensed (no description). Matt's pick from the roles lab.
XP_SITE = """<ul class="xp xp-rows">
          <li><img class="xp-logo" src="../assets/hospitable-mark.svg" alt=""><span class="role">Senior Staff Product Designer</span><span class="when num">Now</span><a class="co" href="https://hospitable.com/">Hospitable</a></li>
          <li><img class="xp-logo" src="../assets/carv-logo.svg" alt=""><span class="role">Lead Product Designer</span><span class="when num">Feb 2024 — Mar 2025</span><a class="co" href="https://www.carv.com/">Carv</a></li>
          <li><img class="xp-logo" src="../assets/trellis/savvy-logo.png" alt=""><span class="role">Staff Product Designer</span><span class="when num">Jan 2023 — Jan 2024</span><a class="co" href="https://savvy.insure/">Trellis / Savvy.Insure</a></li>
          <li><img class="xp-logo" src="../assets/homebot-logo.png" alt=""><span class="role">Senior Product Designer</span><span class="when num">Dec 2020 — Dec 2022</span><span class="co">Homebot</span></li>
        </ul>"""
RESUME_OLD = '<p style="margin-top:18px"><a href="https://cdn.prod.website-files.com/63b35214bc1dc0317e22bd99/668ae1b79c5572bfad32e508_Matt_Jongbloet_CV_2024.pdf" style="color:var(--ink-2);font-size:15px">Download full resume (PDF) →</a></p>'
RESUME_BTN = '<p style="margin-top:18px"><a href="https://cdn.prod.website-files.com/63b35214bc1dc0317e22bd99/668ae1b79c5572bfad32e508_Matt_Jongbloet_CV_2024.pdf" style="color:var(--ink-2);font-size:15px;font-weight:600">Download full resume (PDF) →</a></p>'   # a text link again (Matt dropped the button), now bold

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
    "trellis": ("../case-studies/trellis.html", "trellis/savvy-logo.png", "Trellis / Savvy.Insure", "Growth experiments", "Finding $3.5MM in predicted annual revenue in a car insurance quote flow", "trellis/cover-v2.jpg", "Read the case study →"),
    "pmi": ("../case-studies/pmi.html", "homebot-logo.png", "Homebot", "Private Mortgage Insurance (PMI)", "Helping ≈1M US homeowners save an estimated $200M a month", "pmi-mockup.png", "Read the case study →"),
    "search": ("../case-studies/home-search.html", "homebot-logo.png", "Homebot", "Home Search", "Helping ≈10 million people find their next home", "home-search.jpg", "Read the case study →"),
    "admin": ("../case-studies/internal-admin.html", "homebot-logo.png", "Homebot", "Internal Admin", "Cutting the time for 20+ key admin tasks by ≈80%", "internal-admin.jpg", "Read the case study →"),
    "research": ("../case-studies/scaling-research.html", "homebot-logo.png", "Homebot", "Scaling Research", "Empowering 30+ product people to learn in rigorous ways", "scaling-research.png", "Read the case study →"),
    "health": ("../case-studies/digital-health.html", "humanapi-logo.png", "Human API", "Digital Health", "Helping convince investors with a compelling story and prototype", "digital-health.jpg", "Read the case study →"),
    "value": ("../case-studies/home-value-estimates.html", "homebot-logo.png", "Homebot", "Home Value Estimates", "Increasing trust and confidence in home value estimates", "home-value.png", "Read the case study →"),
    "wwf": ("../case-studies/location-based-game.html", "wwf-logo.png", "WWF", "Location-Based Game", "Using technology to enhance nature experiences for families", "wwf-game.jpg", "Read the case study →"),
}


DARK_SHOTS = {"pmi-mockup.png": "pmi-mockup-dark.png", "home-search.jpg": "home-search-dark.jpg", "home-value.png": "home-value-dark.png"}  # swapped in dark mode


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
        <div class="pc-shot{' has-dark' if shot in DARK_SHOTS else ''}"><img src="../assets/{shot}"{f' data-dark="../assets/{DARK_SHOTS[shot]}"' if shot in DARK_SHOTS else ''} alt="" loading="lazy"></div>
      </a>"""


def work(order, wide=None, all_link=True):
    wide = wide or {order[0]}
    cards = "\n".join(card(k, wide=(k in wide)) for k in order)
    more = f'\n        <a href="{PORTFOLIO}">All projects →</a>' if all_link else ""
    return f"""  <section class="work-band" id="work">
    <div class="wrap">
      <div class="section-head">
        <h2>Selected work</h2>{more}
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


# ---- The current site (Matt's picks so far): A6.1's copy, a header and hero modelled on Sati Tashibayeva's, dark mode.
PIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7Zm0 9.6A2.6 2.6 0 1 1 12 6.4a2.6 2.6 0 0 1 0 5.2Z"/></svg>'
HOSP_LOGO = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 136 25" class="hosp" aria-hidden="true"><path fill="#ed3c6a" transform="translate(0.7 0.5)" d="M 13.036 20.308 C 14.066 20.308 14.901 21.134 14.901 22.154 C 14.901 23.174 14.066 24 13.036 24 L 5.59 24 C 4.565 24.005 3.731 23.179 3.725 22.154 C 3.725 21.134 4.56 20.308 5.59 20.308 Z M 9.313 0 C 14.457 0 18.627 4.133 18.627 9.23 C 18.627 14.329 14.457 18.462 9.313 18.462 C 4.169 18.462 0 14.329 0 9.23 C 0 4.131 4.17 0 9.313 0 Z M 9.313 3.692 C 6.227 3.692 3.725 6.172 3.725 9.231 C 3.725 12.29 6.227 14.769 9.313 14.769 C 12.399 14.769 14.901 12.289 14.901 9.231 C 14.901 6.172 12.399 3.692 9.313 3.692 Z"/><path fill="currentColor" transform="translate(30 4)" d="M 6.156 4.568 C 6.776 4.568 7.353 4.683 7.889 4.913 C 8.428 5.118 8.91 5.448 9.296 5.876 C 9.681 6.288 9.983 6.79 10.201 7.383 C 10.435 7.975 10.552 8.642 10.552 9.383 L 10.552 16.049 L 7.663 16.049 L 7.663 9.753 C 7.663 9.013 7.437 8.42 6.985 7.975 C 6.549 7.515 5.98 7.284 5.276 7.284 C 4.573 7.284 3.995 7.514 3.543 7.975 C 3.107 8.42 2.889 9.012 2.889 9.753 L 2.889 16.049 L 0 16.049 L 0 0.494 L 2.89 0.494 L 2.89 5.802 C 3.107 5.572 3.367 5.366 3.668 5.185 C 3.989 5.014 4.326 4.874 4.673 4.765 C 5.092 4.634 5.586 4.568 6.156 4.568 Z M 15.462 10.37 C 15.462 11.309 15.738 12.058 16.291 12.617 C 16.843 13.177 17.531 13.457 18.351 13.457 C 19.171 13.457 19.858 13.177 20.411 12.617 C 20.964 12.057 21.241 11.309 21.241 10.37 C 21.241 9.432 20.964 8.683 20.411 8.123 C 19.858 7.563 19.171 7.283 18.351 7.283 C 17.531 7.283 16.843 7.563 16.291 8.123 C 15.738 8.683 15.461 9.433 15.461 10.37 Z M 24.13 10.37 C 24.135 11.153 23.972 11.927 23.652 12.642 C 23.351 13.333 22.932 13.942 22.396 14.469 C 21.876 14.996 21.266 15.416 20.562 15.729 C 19.863 16.028 19.111 16.179 18.351 16.173 C 17.583 16.177 16.823 16.025 16.115 15.728 C 15.434 15.419 14.814 14.993 14.281 14.469 C 13.759 13.938 13.333 13.32 13.024 12.642 C 12.72 11.923 12.567 11.15 12.572 10.37 C 12.572 9.564 12.723 8.815 13.025 8.123 C 13.33 7.436 13.755 6.809 14.281 6.272 C 14.81 5.75 15.432 5.331 16.115 5.037 C 16.819 4.724 17.581 4.564 18.351 4.567 C 19.113 4.562 19.867 4.722 20.561 5.037 C 21.249 5.322 21.873 5.742 22.396 6.272 C 22.933 6.8 23.36 7.429 23.652 8.123 C 23.971 8.815 24.13 9.563 24.13 10.37 Z M 28.39 12.47 C 28.456 12.848 28.64 13.169 28.942 13.432 C 29.243 13.695 29.645 13.827 30.148 13.827 C 30.65 13.827 31.044 13.704 31.328 13.457 C 31.63 13.193 31.781 12.905 31.781 12.593 C 31.781 12.329 31.631 12.123 31.329 11.975 C 30.984 11.805 30.622 11.672 30.249 11.58 C 29.774 11.438 29.297 11.306 28.816 11.185 C 28.324 11.058 27.851 10.867 27.409 10.617 C 26.982 10.361 26.607 10.026 26.304 9.63 C 26.019 9.218 25.877 8.683 25.877 8.025 C 25.877 7.564 25.969 7.128 26.153 6.716 C 26.354 6.288 26.645 5.909 27.007 5.605 C 27.376 5.292 27.811 5.045 28.314 4.865 C 28.816 4.667 29.386 4.568 30.022 4.568 C 31.412 4.568 32.476 4.898 33.213 5.556 C 33.95 6.183 34.425 7.064 34.545 8.025 L 31.78 8.025 C 31.713 7.778 31.529 7.531 31.227 7.284 C 30.943 7.037 30.582 6.914 30.147 6.914 C 29.711 6.914 29.368 7.021 29.117 7.234 C 28.889 7.433 28.76 7.722 28.765 8.024 C 28.765 8.288 28.907 8.494 29.192 8.642 C 29.494 8.79 29.862 8.93 30.298 9.062 C 30.733 9.177 31.202 9.309 31.705 9.457 C 32.224 9.588 32.701 9.786 33.137 10.049 C 33.572 10.313 33.933 10.659 34.217 11.086 C 34.519 11.498 34.669 12.041 34.669 12.716 C 34.669 13.176 34.569 13.621 34.368 14.049 C 34.162 14.467 33.871 14.837 33.514 15.136 C 33.11 15.469 32.651 15.728 32.157 15.901 C 31.637 16.082 31.051 16.173 30.398 16.173 C 28.891 16.173 27.743 15.835 26.956 15.161 C 26.186 14.486 25.742 13.588 25.624 12.469 L 28.388 12.469 Z M 42.708 4.568 C 43.428 4.568 44.115 4.716 44.768 5.012 C 45.417 5.289 46 5.701 46.477 6.222 C 46.988 6.746 47.389 7.367 47.657 8.049 C 47.959 8.757 48.11 9.531 48.11 10.37 C 48.11 11.21 47.96 11.984 47.658 12.691 C 47.386 13.378 46.986 14.007 46.477 14.543 C 45.991 15.053 45.411 15.464 44.768 15.753 C 44.115 16.033 43.428 16.173 42.708 16.173 C 42.275 16.18 41.843 16.122 41.427 16 C 41.109 15.898 40.798 15.775 40.497 15.63 C 40.207 15.474 39.937 15.283 39.693 15.062 L 39.693 20 L 36.803 20 L 36.803 4.691 L 38.939 4.691 L 39.442 5.802 C 39.693 5.572 39.986 5.366 40.322 5.185 C 40.653 5.018 40.998 4.877 41.352 4.765 C 41.791 4.628 42.248 4.562 42.708 4.568 Z M 39.442 10.37 C 39.442 11.309 39.718 12.058 40.271 12.617 C 40.824 13.177 41.511 13.457 42.331 13.457 C 43.151 13.457 43.839 13.177 44.391 12.617 C 44.944 12.057 45.221 11.309 45.221 10.37 C 45.221 9.432 44.944 8.683 44.391 8.123 C 43.839 7.563 43.151 7.283 42.331 7.283 C 41.511 7.283 40.824 7.563 40.271 8.123 C 39.718 8.683 39.441 9.433 39.441 10.37 Z M 53.139 16.05 L 50.249 16.05 L 50.249 4.69 L 53.139 4.69 Z M 51.757 3.21 C 51.322 3.21 50.937 3.054 50.601 2.74 C 50.283 2.412 50.124 2.033 50.124 1.605 C 50.124 1.177 50.284 0.807 50.601 0.494 C 50.936 0.164 51.321 0 51.757 0 C 52.193 0 52.57 0.165 52.887 0.494 C 53.223 0.807 53.39 1.177 53.39 1.604 C 53.39 2.033 53.223 2.412 52.888 2.741 C 52.591 3.045 52.183 3.214 51.758 3.21 Z M 57.15 1.975 L 59.662 1.975 L 59.662 4.691 L 62.174 4.691 L 62.174 7.284 L 59.662 7.284 L 59.662 11.975 C 59.662 12.469 59.804 12.864 60.089 13.16 C 60.39 13.44 60.792 13.58 61.295 13.58 L 61.621 13.58 C 61.705 13.564 61.781 13.547 61.848 13.53 C 61.917 13.513 61.984 13.489 62.048 13.457 L 62.048 15.926 C 61.931 15.976 61.798 16.016 61.647 16.049 C 61.328 16.136 60.998 16.178 60.667 16.173 C 60.097 16.173 59.569 16.083 59.084 15.901 C 58.621 15.707 58.202 15.422 57.853 15.061 C 57.51 14.686 57.237 14.251 57.049 13.778 C 56.865 13.284 56.772 12.724 56.772 12.098 L 56.772 7.285 L 55.014 7.285 L 55.014 4.938 L 55.767 4.938 C 56.689 4.938 57.149 4.485 57.149 3.58 L 57.149 1.975 Z M 69.082 4.568 C 69.736 4.568 70.339 4.683 70.892 4.914 C 71.444 5.128 71.922 5.432 72.323 5.827 C 72.725 6.222 73.035 6.691 73.253 7.235 C 73.488 7.778 73.605 8.37 73.605 9.012 L 73.605 16.049 L 71.469 16.049 L 70.967 14.939 C 70.699 15.169 70.406 15.374 70.087 15.556 C 69.76 15.739 69.415 15.888 69.057 16 C 68.615 16.12 68.159 16.179 67.701 16.173 C 66.444 16.173 65.481 15.877 64.811 15.283 C 64.141 14.675 63.806 13.901 63.806 12.963 C 63.806 12.403 63.915 11.893 64.133 11.433 C 64.367 10.955 64.753 10.551 65.289 10.223 C 65.825 9.876 66.529 9.613 67.399 9.433 C 68.287 9.235 69.392 9.136 70.716 9.136 C 70.716 8.51 70.54 8.025 70.188 7.679 C 69.853 7.333 69.401 7.16 68.831 7.16 C 68.446 7.16 68.136 7.226 67.901 7.358 C 67.706 7.472 67.528 7.613 67.374 7.778 C 67.225 7.956 67.121 8.168 67.072 8.395 L 64.183 8.395 C 64.247 7.879 64.4 7.378 64.635 6.914 C 64.889 6.45 65.23 6.039 65.64 5.704 C 66.082 5.346 66.584 5.07 67.123 4.889 C 67.709 4.675 68.363 4.568 69.083 4.568 Z M 68.203 13.951 C 68.957 13.951 69.56 13.736 70.012 13.309 C 70.481 12.864 70.716 12.296 70.716 11.605 L 70.716 11.111 C 69.861 11.111 69.174 11.152 68.656 11.234 C 68.136 11.3 67.726 11.407 67.424 11.556 C 67.139 11.687 66.947 11.852 66.846 12.049 C 66.746 12.247 66.696 12.469 66.696 12.716 C 66.696 13.029 66.838 13.316 67.123 13.58 C 67.407 13.827 67.767 13.95 68.203 13.95 Z M 82.137 16.173 C 81.679 16.179 81.222 16.121 80.78 16 C 80.422 15.887 80.077 15.738 79.75 15.555 C 79.433 15.386 79.137 15.179 78.871 14.938 L 78.369 16.049 L 76.233 16.049 L 76.233 0.494 L 79.123 0.494 L 79.123 5.679 C 79.357 5.481 79.625 5.3 79.926 5.136 C 80.194 5.004 80.504 4.88 80.856 4.766 C 81.269 4.627 81.702 4.56 82.137 4.568 C 82.857 4.568 83.544 4.716 84.197 5.012 C 84.846 5.289 85.429 5.701 85.906 6.222 C 86.417 6.746 86.818 7.367 87.086 8.049 C 87.388 8.757 87.539 9.531 87.539 10.37 C 87.539 11.21 87.389 11.983 87.087 12.691 C 86.815 13.378 86.415 14.007 85.906 14.543 C 85.42 15.053 84.84 15.464 84.197 15.753 C 83.544 16.033 82.857 16.173 82.137 16.173 Z M 78.871 10.37 C 78.871 11.309 79.147 12.057 79.701 12.617 C 80.253 13.177 80.94 13.457 81.761 13.457 C 82.581 13.457 83.268 13.177 83.821 12.617 C 84.373 12.057 84.65 11.308 84.65 10.37 C 84.65 9.432 84.373 8.683 83.82 8.123 C 83.268 7.563 82.581 7.283 81.76 7.283 C 80.94 7.283 80.253 7.563 79.7 8.123 C 79.147 8.683 78.871 9.432 78.871 10.37 Z M 92.568 16.05 L 89.678 16.05 L 89.678 0.493 L 92.568 0.493 L 92.568 16.048 Z M 105.623 12.593 C 105.454 13.054 105.217 13.487 104.92 13.877 C 104.604 14.319 104.223 14.71 103.789 15.037 C 103.354 15.367 102.851 15.637 102.282 15.852 C 101.704 16.07 101.091 16.179 100.473 16.172 C 99.705 16.176 98.945 16.025 98.237 15.728 C 97.556 15.42 96.935 14.993 96.402 14.469 C 95.88 13.938 95.455 13.32 95.146 12.642 C 94.842 11.923 94.689 11.15 94.694 10.37 C 94.694 9.564 94.844 8.815 95.146 8.123 C 95.45 7.436 95.876 6.809 96.402 6.272 C 96.931 5.75 97.554 5.331 98.237 5.037 C 98.941 4.724 99.703 4.564 100.473 4.567 C 101.226 4.567 101.938 4.707 102.608 4.987 C 103.278 5.267 103.864 5.663 104.367 6.173 C 104.883 6.704 105.284 7.334 105.548 8.025 C 105.849 8.732 106 9.515 106 10.37 C 106 10.502 105.992 10.634 105.975 10.765 L 105.925 11.111 C 105.909 11.234 105.892 11.358 105.874 11.481 L 97.834 11.481 C 97.968 12.041 98.254 12.511 98.689 12.889 C 99.124 13.268 99.719 13.457 100.473 13.457 C 100.858 13.457 101.176 13.416 101.427 13.333 C 101.695 13.251 101.921 13.153 102.106 13.037 C 102.295 12.916 102.465 12.766 102.608 12.593 Z M 100.473 7.283 C 99.719 7.283 99.099 7.498 98.613 7.926 C 98.144 8.354 97.843 8.881 97.709 9.506 L 103.236 9.506 C 103.108 8.892 102.782 8.336 102.307 7.926 C 101.838 7.498 101.226 7.284 100.473 7.284 Z"/></svg>'   # pin + wordmark; the wordmark takes the text colour so it works in dark mode
NL_FLAG = '<svg class="flag" viewBox="0 0 24 16" role="img" aria-label="Dutch flag"><clipPath id="nlf"><rect width="24" height="16" rx="2.5"/></clipPath><g clip-path="url(#nlf)"><rect width="24" height="5.34" fill="#ae1c28"/><rect y="5.33" width="24" height="5.34" fill="#fff"/><rect y="10.66" width="24" height="5.34" fill="#21468b"/></g><rect x=".5" y=".5" width="23" height="15" rx="2" fill="none" stroke="rgb(0 0 0 / .14)"/></svg>'
HEROES["site"] = f"""  <div class="hero-screen">
  <section class="wrap hero hero-text">
    <div class="hero-copy">
      <h1>I make complex products<br><em>feel simple.</em></h1>
      <p class="lede">I’m a rigorously curious product designer with 15 years’ experience shaping systems, stories and strategy. I’m happiest when people succeed with what I design.</p>
      <p class="hero-meta"><span class="hm">{NL_FLAG}Amsterdam, NL</span><span class="hm">Designing @<a class="hosp-link" href="https://hospitable.com/" aria-label="Hospitable">{HOSP_LOGO}</a></span></p>
    </div>
  </section>
  </div>"""
WORK["site"] = ["trellis", "pmi", "search", "admin", "research", "health", "value", "wwf"]   # every case study, all local
SITE_CSS = """
/* Hero modelled on Sati Tashibayeva's: a smaller headline and intro, the interactive piece on the right.
   Under the intro: location and current role (no buttons). The hero stops short of the first screen
   so the top of the project cards peeks in from the bottom and invites a scroll. */
.hero-screen { display: flex; flex-direction: column; min-height: calc(100svh - 69px - clamp(170px, 30svh, 290px)); }  /* 69px = header + its border */
.hero-screen > .wrap { width: 100%; }
.hero-screen .hero { flex: 1; }
.hero.hero-text h1 { font-size: clamp(34px, 4.3vw, 62px); max-width: none; letter-spacing: -0.03em; }
.hero .lede { font-size: clamp(16px, 1.25vw, 18px); max-width: 40ch; }
.hero-screen .hero h1 em { color: var(--accent-text, var(--signal)); }   /* “feel simple.” takes the accent */
.hero-screen .hero.hero-text.has-toy { padding-block: clamp(36px, 7svh, 76px) clamp(48px, 9svh, 96px); }   /* more air under the header and above Selected work */
.has-toy .hero-toy { max-width: 520px; gap: 8px; }
.hero-screen .toy-stage { width: clamp(240px, calc(70svh - 180px), 100%); margin-inline: auto; }
.hero-screen .face-pop { min-height: 62px; }
/* Location and current role sit just under the intro, where the buttons were, as soft pills so they read as their own element.
   (Fifteen treatments to compare: redesigns/meta-lab/, tools/build-meta-lab.py.) */
.hero .lede { margin-bottom: 0; }
.hero-meta { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; margin: 0; font-size: 15px; color: var(--ink); font-weight: 500; }   /* the column's 28px gap spaces it, as it did the buttons */
.hero-meta .hm { display: inline-flex; align-items: center; gap: 9px; min-height: 40px; padding: 0 16px; border-radius: 999px; background: color-mix(in srgb, var(--ink) 6%, transparent); }
.hero-meta .flag { width: 24px; height: 16px; flex: none; }
.hero-meta .hosp-link { display: inline-flex; align-items: center; padding-block: 10px; color: var(--ink); margin-left: -2px; }
.hero-meta .hosp { width: auto; height: 17px; color: inherit; }
/* Two columns, one height: the face column is exactly as tall as the text column, so the top of the face lines up
   with the top of the headline and the hint sits level with the pills. The face is sized by that height. */
@media (min-width: 901px) {
  .hero-screen .hero.hero-text.has-toy { align-items: stretch; align-content: center; }
  .hero-screen .hero-toy { height: 0; min-height: 100%; gap: 0; justify-self: end; }
  .hero-screen .toy-stage { flex: 1 1 0; min-height: 0; width: auto; max-width: 100%; aspect-ratio: 1; align-self: center; margin: 0; }
  .hero-screen .toy-hint { flex: none; min-height: 40px; display: grid; place-items: center; }   /* 40px = the pills' height */
}
.work-band { margin-top: 0; padding-top: 52px; }
/* Recent roles (Matt's pick from the roles lab): rows with a company logo, condensed. */
.xp.xp-rows { border-top: 0; }   /* no separator lines: white space only */
.xp-rows li { grid-template-columns: 40px minmax(0, 1fr) auto; grid-template-areas: "lg role when" "lg co when"; column-gap: 14px; row-gap: 1px; padding: 0 0 22px; border-bottom: 0; align-items: start; }
.xp-rows .xp-logo { grid-area: lg; width: 40px; height: 40px; border-radius: 10px; }
.xp-rows .role { grid-area: role; font-size: 16px; line-height: 1.35; }
.xp-rows .co { grid-area: co; justify-self: start; }
.xp-rows .when { grid-area: when; grid-row: auto; font-size: 13px; line-height: 1.7; }
@media (max-width: 480px) { .xp-rows li { grid-template-columns: 40px minmax(0, 1fr); grid-template-areas: "lg role" "lg co" "lg when"; } .xp-rows .when { text-align: left; } }
/* On phones the company links get extra padding as tap targets; pull it back so linked and unlinked rows space the same. */
.xp-rows a.co { margin-block: -8px; position: relative; }
@media (min-width: 561px) { .xp-rows a.co { margin-block: 0; } }
/* Project cards (Matt's pick from the card lab): screenshot on top edge to edge, the logo straddling its bottom edge, bold title. */
.pcard { padding: 0; flex-direction: column-reverse; justify-content: flex-end; }
.pc-shot { margin: 0; border-radius: 0; }
.pc-copy { padding: 0 32px 32px; }
.pc-logo { width: 64px; height: 64px; margin: -32px 0 14px; position: relative; z-index: 1; box-shadow: 0 0 0 4px var(--paper); }   /* z-index keeps it above the image when the image scales on hover */
.pcard h3 { font-weight: 600; }
:root[data-theme="dark"] .pc-logo { box-shadow: 0 0 0 4px var(--mist); opacity: 1; }
@media (max-width: 900px) { .pcard { padding: 0; } .pc-shot { margin: 0; } .pc-copy { padding: 0 24px 26px; } .pc-logo { width: 56px; height: 56px; margin: -28px 0 12px; } }
@media (max-width: 900px) { .hero-screen { min-height: 0; } }
"""

ICON_CSS = """
/* Icon-only header: the name now lives in the hero chip, so the mark stands alone and a little larger. */
.brand img.mark { height: 42px; }
"""
TYPE_SMALLER = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "type-smaller.css")).read()
ITER_CSS["a6-1-feel-simple"] = ITER_CSS["a6-text-first"] + ICON_CSS + """
/* A6.1 — Matt's chosen home page: A6's layout, leading with “I make complex products feel simple.” */
.hero-text h1 { max-width: 14ch; }
""" + TYPE_SMALLER
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


ITER_CSS["site"] = ITER_CSS["a6-text-first"] + TYPE_SMALLER + SITE_CSS + sp.HEADER_CSS + sp.DARK_CSS
FACTS_RE = re.compile(r'  <div class="wrap">\n    <div class="facts">.*?\n    </div>\n  </div>\n', re.S)


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
                # site: no wide cards (Matt wants every project two per row)
                s = work_re.sub(lambda m: work(WORK[name], wide={"-"}, all_link=False) if name == "site" else work(WORK[name]), s)
                s = xp_re.sub(lambda m: XP_SITE if name == "site" else XP_HOME, s)
                if name == "site":
                    s = rep(s, RESUME_OLD, RESUME_BTN, f"{name}/{page}")
            if page == "about.html":
                s = xp_re.sub(lambda m: XP_ABOUT, s)
            if name == "site":
                cur = "about" if page == "about.html" else "work"
                assert len(sp.HEADER_RE.findall(s)) == 1
                s = sp.HEADER_RE.sub(lambda m: sp.header("", cur, work_href="#work" if page == "index.html" else None), s)
                s = rep(s, "</head>", sp.THEME_HEAD + "\n</head>", f"{name}/{page}")
                if page == "index.html":
                    assert len(FACTS_RE.findall(s)) == 1
                    s = FACTS_RE.sub("", s)
            if name in ICON_ONLY:
                s = rep(s, BRAND_OLD, BRAND_ICON, f"{name}/{page}")
            s = rep(s, '<link rel="stylesheet" href="style.css">', '<link rel="stylesheet" href="style.css">\n<link rel="stylesheet" href="variant.css">', f"{name}/{page}")
            open(os.path.join(out, page), "w").write(s)
        open(os.path.join(out, "variant.css"), "w").write(SHARED_CSS + ITER_CSS[name])
        if name == "site":
            open(os.path.join(out, "script.js"), "a").write(sp.THEME_JS)
            os.remove(os.path.join(out, "case-pmi.html"))   # case studies live in redesigns/case-studies
        print("built", name)


if __name__ == "__main__":
    build()
