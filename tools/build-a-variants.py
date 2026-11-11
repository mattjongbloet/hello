"""Build the five close variations of Direction A (redesigns/a1-… to a5-…) from redesigns/a-clarity.

Each variation is A's own HTML, CSS and JS plus:
  - shared content updates: Senior Staff title, research-light positioning;
  - its own variant.css (loaded after A's style.css) and, where needed, a few HTML edits.
Re-run after changing A:  python3 tools/build-a-variants.py
"""
import os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "redesigns", "a-clarity")
PAGES = ["index.html", "case-pmi.html", "about.html"]
FONT_A = "https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;650;700&family=JetBrains+Mono:wght@500&display=swap"


def rep(s, a, b, page, var):
    assert a in s, f"{var}/{page}: missing {a[:70]!r}"
    return s.replace(a, b)


# Shared by every variation: the title Matt holds now, and positioning that leads with the role, not research.
COMMON = {
    "index.html": [
        ("<title>Matt Jongbloet — Product Designer</title>", "<title>Matt Jongbloet — Senior Staff Product Designer</title>"),
        ('content="Product designer and UX researcher with 10+ years of experience, currently leading design at Hospitable."',
         'content="Senior Staff Product Designer with 10+ years of experience, currently at Hospitable."'),
        ('<p class="eyebrow">Product designer &amp; UX researcher · Amsterdam</p>', '<p class="eyebrow">Senior Staff Product Designer · Amsterdam</p>'),
        ("<b>Staff Product Designer</b><span>Hospitable", "<b>Senior Staff Product Designer</b><span>Hospitable"),
        ('<span class="role">Staff Product Designer</span><span class="when num">Mar 2024', '<span class="role">Senior Staff Product Designer</span><span class="when num">Mar 2024'),
        ("<div><b>5 years</b><span>sharpening my research practice</span></div>", "<div><b class=\"num\">30+</b><span>product people empowered to learn</span></div>"),
        ("<p>Product design, research, or a problem that needs simplifying. I’m in Amsterdam (CET).</p>",
         "<p>Senior staff product design, or a problem that needs simplifying. I’m in Amsterdam (CET).</p>"),
    ],
    "case-pmi.html": [
        ("<p>Product design, research, or a problem that needs simplifying. I’m in Amsterdam (CET).</p>",
         "<p>Senior staff product design, or a problem that needs simplifying. I’m in Amsterdam (CET).</p>"),
    ],
    "about.html": [
        ("I’m Matt, a product designer and UX researcher with more than ten years in product design.",
         "I’m Matt, a Senior Staff Product Designer with more than ten years in product design."),
        ('<span class="role">Staff Product Designer</span><span class="when num">Mar 2024', '<span class="role">Senior Staff Product Designer</span><span class="when num">Mar 2024'),
        ("<p>Product design, research, or a problem that needs simplifying. I’m in Amsterdam (CET).</p>",
         "<p>Senior staff product design, or a problem that needs simplifying. I’m in Amsterdam (CET).</p>"),
    ],
}

DARK_IMAGES = [("../assets/pmi-mockup.png", "../assets/pmi-mockup-dark.png"),
               ("../assets/home-search.jpg", "../assets/home-search-dark.jpg"),
               ("../assets/home-value.png", "../assets/home-value-dark.png"),
               ('src="../assets/mj-logo.svg"', 'src="../assets/mj-logo-light.svg"')]  # header logo only, not the favicon

VARIANTS = {
    "a1-serif": {
        "font": "https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;650;700&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@500&display=swap",
    },
    "a2-cobalt": {},
    "a3-grid": {},
    "a4-night": {"swap": DARK_IMAGES},
    "a5-senior-staff": {
        "html": {
            "index.html": [
                ("<p class=\"lede\">I’m Matt. I’m rigorously curious, I enjoy simplifying the complex, and I’m happiest when people succeed with what I design. Right now I’m leading design at <strong>Hospitable</strong>, helping hosts run their short-term rentals on autopilot.</p>",
                 "<p class=\"lede\">I’m Matt, Senior Staff Product Designer at <strong>Hospitable</strong>. I work above the screens: finding the opportunity worth building, shaping it into a plan engineering can ship, and bringing the company along.</p>"),
                ("""      <div><b class="num">10+ years</b><span>in product design</span></div>
      <div><b>MSc, Cum Laude</b><span>Digital Design</span></div>
      <div><b>UXC</b><span>Nielsen Norman Group</span></div>
      <div><b class="num">30+</b><span>product people empowered to learn</span></div>""",
                 """      <div><b class="num">≈$200M</b><span>a month in estimated savings (PMI)</span></div>
      <div><b class="num">≈10M</b><span>people helped by Home Search</span></div>
      <div><b class="num">≈80%</b><span>less time on 20+ admin tasks</span></div>
      <div><b class="num">30+</b><span>product people empowered to learn</span></div>"""),
                ("""  <section class="wrap section">
    <div class="split">""",
                 """  <section class="wrap section" id="how">
    <div class="section-head"><h2>How I work at staff level</h2></div>
    <div class="how">
      <div class="reveal"><span class="eyebrow">01 · Find</span><h3>The opportunity worth building</h3><p>At Homebot, interviews and our data showed ≈1M homeowners could drop PMI early. I designed for that opportunity.</p></div>
      <div class="reveal"><span class="eyebrow">02 · Plan</span><h3>A shape engineering can ship</h3><p>With the engineering leads I split the PMI design into four sprints, each the smallest chunk of deliverable value.</p></div>
      <div class="reveal"><span class="eyebrow">03 · Align</span><h3>The whole company, not just the team</h3><p>I presented PMI to the entire company with the Double Diamond, connecting colleagues to the mission.</p></div>
      <div class="reveal"><span class="eyebrow">04 · Raise</span><h3>How the org works</h3><p>With Scaling Research I empowered 30+ product people to learn in rigorous ways.</p></div>
    </div>
  </section>

  <section class="wrap section">
    <div class="split">"""),
            ],
            "about.html": [
                ("<h1 style=\"margin-top:16px\">Design with a purpose, backed by research.</h1>",
                 "<h1 style=\"margin-top:16px\">Design with a purpose, at the scale of a company.</h1>"),
            ],
            "case-pmi.html": [
                ("<div><dt>My part</dt><dd>Prototyping, research, delivery plan</dd></div>",
                 "<div><dt>My part</dt><dd>Opportunity, design, delivery plan</dd></div>"),
            ],
        },
    },
}


def build():
    for var, cfg in VARIANTS.items():
        out = os.path.join(ROOT, "redesigns", var)
        os.makedirs(out, exist_ok=True)
        shutil.copy(os.path.join(A, "style.css"), os.path.join(out, "style.css"))
        shutil.copy(os.path.join(A, "script.js"), os.path.join(out, "script.js"))
        for page in PAGES:
            s = open(os.path.join(A, page)).read()
            for a, b in COMMON[page]:
                s = rep(s, a, b, page, var)
            for a, b in cfg.get("html", {}).get(page, []):
                s = rep(s, a, b, page, var)
            for a, b in cfg.get("swap", []):  # optional: only where the page uses that image
                s = s.replace(a, b)
            if cfg.get("font"):
                s = rep(s, FONT_A, cfg["font"], page, var)
            s = rep(s, '<link rel="stylesheet" href="style.css">', '<link rel="stylesheet" href="style.css">\n<link rel="stylesheet" href="variant.css">', page, var)
            open(os.path.join(out, page), "w").write(s)
        assert os.path.exists(os.path.join(out, "variant.css")), f"{var}: write variant.css first"
        print("built", var)


if __name__ == "__main__":
    build()
