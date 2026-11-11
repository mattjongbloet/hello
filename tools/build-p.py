"""Build Direction P — Sentence (Matt's own mockup) into redesigns/p-sentence/.
Shared header, contact and footer live here; page bodies below. Re-run: python3 tools/build-p.py"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "redesigns", "p-sentence")
FONTS = "https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Hanken+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap"
CV = "https://cdn.prod.website-files.com/63b35214bc1dc0317e22bd99/668ae1b79c5572bfad32e508_Matt_Jongbloet_CV_2024.pdf"
SPARK = '<svg class="spark" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 0c.9 6.4 5.6 11.1 12 12-6.4.9-11.1 5.6-12 12-.9-6.4-5.6-11.1-12-12C6.4 11.1 11.1 6.4 12 0z"/></svg>'
FLAG = '<svg class="flag" viewBox="0 0 9 6" aria-hidden="true"><rect width="9" height="2" fill="#ae1c28"/><rect y="2" width="9" height="2" fill="#fff"/><rect y="4" width="9" height="2" fill="#21468b"/></svg>'
ST_SPARK = '<svg class="sticker st-spark" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" stroke="#fff" stroke-width="1.6" stroke-linejoin="round" d="M12 1c.9 6 5 10.1 11 11-6 .9-10.1 5-11 11-.9-6-5-10.1-11-11 6-.9 10.1-5 11-11z"/></svg>'
ST_HEART = '<svg class="sticker st-heart" viewBox="0 0 32 29" aria-hidden="true"><path fill="#ff5c93" stroke="#fff" stroke-width="2.4" stroke-linejoin="round" d="M16 27.5S2 19.4 2 9.6C2 5.4 5.2 2 9.2 2c3 0 5.4 1.8 6.8 4.3C17.4 3.8 19.8 2 22.8 2 26.8 2 30 5.4 30 9.6c0 9.8-14 17.9-14 17.9z"/></svg>'


def head(title, desc):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="icon" href="../assets/mj-logo.svg" type="image/svg+xml">
<link rel="stylesheet" href="../fonts/fonts.css">
<link rel="stylesheet" href="style.css">
</head>
<body>
"""


def header(current):
    items = [("h", "Home", "index.html"), ("w", "Work", "index.html#work"), ("a", "About", "about.html"), ("c", "Contact", "#contact")]
    links = "\n".join(
        f'      <a href="{href}" aria-keyshortcuts="{k}"{" aria-current=\"page\"" if label == current else ""}><span class="key" data-k="{k}" aria-hidden="true">{k.upper()}</span>{label}</a>'
        for k, label, href in items)
    return f"""<header class="top">
  <div class="wrap">
    <a class="chip name" href="index.html"><img class="mark" src="../assets/mj-logo.svg" alt="">Matt Jongbloet</a>
    <nav class="nav" aria-label="Main">
{links}
    </nav>
    <span class="chip status"><i aria-hidden="true"></i>Open to senior staff roles</span>
  </div>
</header>
"""


CONTACT = f"""<section class="contact" id="contact">
  <div class="wrap">
    <div class="contact-card">
      <div>
        <h2>Drop me a line.{SPARK}</h2>
        <p>Senior staff product design, or a problem that needs simplifying. I’m in Amsterdam (CET).</p>
      </div>
      <div class="links">
        <a class="btn" href="mailto:matthewjongbloet@gmail.com">matthewjongbloet@gmail.com</a>
        <a class="plain" href="{CV}">Resume (PDF) ↗</a>
        <span class="hint"><span class="key" aria-hidden="true">C</span>jumps here from anywhere</span>
      </div>
    </div>
  </div>
</section>
<footer class="foot"><div class="wrap"><span>© 2026 Matt Jongbloet</span><span class="keys" aria-hidden="true">Move around with <span class="key">H</span><span class="key">W</span><span class="key">A</span><span class="key">C</span></span><span><a href="index.html">Home</a> · <a href="about.html">About</a> · <a href="{CV}">Resume</a></span></div></footer>
<script src="script.js"></script>
</body>
</html>
"""

HOME = f"""<main>
  <section class="wrap hero">
    <div class="hero-copy">
      <div class="avatar"><img src="../assets/headshot.jpg" alt="Matt Jongbloet"><span class="dot" aria-hidden="true"></span></div>
      <h1 class="sentence">Matt Jongbloet is a <em>senior staff product designer</em> at <a class="logo-pill" href="https://hospitable.com/"><img src="../assets/hospitable-logo.svg" alt="Hospitable"></a> with 15+&nbsp;yrs experience helping people and businesses <span class="shine">shine{SPARK}</span></h1>
      <p class="based">{FLAG}<span>Based in Amsterdam, NL —</span><a href="about.html">More about me ↗</a></p>
    </div>
    <div class="stickers" aria-hidden="true">
      {ST_SPARK}
      <span class="sticker st-pill">Product</span>
      {ST_HEART}
      <span class="sticker st-badge"><span><b>MSc</b><span>Cum Laude</span></span></span>
    </div>
  </section>

  <div class="wrap" id="work">
    <hr class="rule">
    <div class="row-head"><h2>Selected work ↓</h2><a href="#contact">Reach out for more details</a></div>

    <div class="cards">
      <a class="card big c-yellow reveal" href="case-pmi.html">
        <div class="copy">
          <div class="tags"><span class="tag"><img src="../assets/homebot-logo.png" alt="">Homebot</span><span class="tag">Case study</span></div>
          <h3>Private Mortgage Insurance</h3>
          <p>Helping homeowners discover they can drop PMI early, and giving their loan officers a reason to reach out.</p>
          <div class="metric"><b class="num">≈$200M</b><span>a month in estimated savings for ≈1M eligible US homeowners</span></div>
          <span class="go">Read the case study <i aria-hidden="true">→</i></span>
        </div>
        <div class="frame"><img src="../assets/pmi-mockup.png" alt="Two phone screens from the PMI feature showing a removal progress bar and ways to remove PMI faster"></div>
      </a>
      <a class="card c-orange reveal" href="https://www.mjongbloet.com/portfolio/home-search">
        <div class="tags"><span class="tag"><img src="../assets/homebot-logo.png" alt="">Homebot</span></div>
        <h3>Home Search</h3>
        <p>Turning a newly acquired search product into an experience that holds its own.</p>
        <div class="metric"><b class="num">≈10M</b><span>people helped to find their next home</span></div>
        <div class="frame"><img src="../assets/home-search.jpg" alt="Home Search on mobile: search screen and a map of listings in Denver"></div>
      </a>
      <a class="card c-blue reveal" href="https://www.mjongbloet.com/portfolio/internal-admin">
        <div class="tags"><span class="tag"><img src="../assets/homebot-logo.png" alt="">Homebot · Internal tools</span></div>
        <h3>Internal Admin</h3>
        <p>Making Homebot’s internal admin for customers, contracts and plans faster to work in.</p>
        <div class="metric"><b class="num">≈80%</b><span>less time needed to complete 20+ key tasks</span></div>
        <div class="frame"><img src="../assets/internal-admin.jpg" alt="Homebot admin contracts table"></div>
      </a>
    </div>

    <div class="minis">
      <a class="mini c-green reveal" href="https://www.mjongbloet.com/portfolio"><div class="frame"><img src="../assets/home-value.png" alt=""></div><span class="who">Homebot</span><h3>Home Value Estimates</h3><p>Increasing trust and confidence in home value estimates.</p></a>
      <a class="mini c-pink reveal" href="https://www.mjongbloet.com/portfolio"><div class="frame"><img src="../assets/scaling-research.png" alt=""></div><span class="who">Homebot</span><h3>Scaling Research</h3><p>Empowering 30+ product people to learn in rigorous ways.</p></a>
      <a class="mini c-lilac reveal" href="https://www.mjongbloet.com/portfolio"><div class="frame"><img src="../assets/digital-health.jpg" alt=""></div><span class="who">Human API</span><h3>Digital Health</h3><p>A story and prototype that helped convince investors.</p></a>
      <a class="mini c-yellow reveal" href="https://www.mjongbloet.com/portfolio"><div class="frame"><img src="../assets/wwf-game.jpg" alt=""></div><span class="who">WWF</span><h3>Location-Based Game</h3><p>Using technology to enhance nature experiences for families.</p></a>
    </div>

    <div class="facts">
      <span class="fact"><b>15+ years</b>designing, 10+ in product</span>
      <span class="fact"><b>MSc, Cum Laude</b>Digital Design</span>
      <span class="fact"><b>UXC</b>Nielsen Norman Group</span>
      <span class="fact"><b class="num">30+</b>product people empowered to learn</span>
    </div>
  </div>

  <section class="wrap section">
    <div class="split">
      <div class="stack reveal">
        <span class="label">About</span>
        <h2>Five years of brand design taught me what I <em>didn’t</em> want to make.</h2>
        <p>Nice-looking things without a purpose. So I moved from Canterbury to Amsterdam for an <strong>MSc in Digital Design</strong>, then spent <strong>5+ years in the US</strong> designing at early- and mid-stage SaaS companies. Now I’m back in Amsterdam.</p>
        <a class="link" href="about.html">Read my story ↗</a>
      </div>
      <div class="reveal">
        <p class="sub">Recent roles</p>
        <ul class="xp">
          <li><span class="role">Senior Staff Product Designer</span><span class="when num">Mar 2024 — Now</span><a class="co" href="https://hospitable.com/">Hospitable</a></li>
          <li><span class="role">Lead Product Designer</span><span class="when num">Feb 2024 — Mar 2025</span><a class="co" href="https://www.carv.com/">Carv</a></li>
          <li><span class="role">Staff Product Designer, Growth</span><span class="when num">Jan 2022 — Feb 2023</span><a class="co" href="https://savvy.insure/">Trellis</a></li>
        </ul>
        <a class="small-link" href="{CV}">Download full resume (PDF) →</a>
      </div>
    </div>
  </section>
</main>
"""

CASE = f"""<main>
  <section class="wrap cs-hero">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html#work">← Work</a><span>/</span><span>Homebot · 2022</span></nav>
    <h1>Helping homeowners drop mortgage insurance <em>early</em></h1>
    <p class="dek">About a million Homebot homeowners could stop paying PMI sooner than they thought. I designed the feature that told them, and gave their loan officers a reason to start the conversation.</p>
    <dl class="meta">
      <div><dt>Company</dt><dd>Homebot</dd></div>
      <div><dt>Date</dt><dd>July 2022</dd></div>
      <div><dt>Team</dt><dd>Consumer Team</dd></div>
      <div><dt>My part</dt><dd>Opportunity, design, delivery plan</dd></div>
    </dl>
  </section>

  <div class="wrap">
    <div class="cover">
      <div class="frame"><img src="../assets/pmi-mockup.png" alt="Two phone screens: 'When can you remove your $152.13 monthly mortgage insurance? Maybe now' with a 20% removal progress bar, and a screen listing ways to remove PMI faster"></div>
      <span class="sticker st-badge" aria-hidden="true"><span><b>≈$200M</b><span>a month</span><span>estimated</span></span></span>
    </div>
    <div class="results">
      <div class="c-yellow"><b class="num">≈1M</b><span>US homeowners on Homebot eligible to remove PMI early</span></div>
      <div class="c-orange"><b class="num">$195</b><span>estimated monthly saving per homeowner</span></div>
      <div class="c-blue"><b class="num">4.8/5</b><span>rating for value and confidence in usability testing</span></div>
      <div class="c-green"><b class="num">500+</b><span>requests to learn about PMI removal in the first sprint</span></div>
    </div>
  </div>

  <div class="wrap cs-body">
    <nav class="toc" aria-label="Contents">
      <span class="label">Contents</span>
      <a href="#overview" class="on"><span class="key">1</span>Overview</a>
      <a href="#background"><span class="key">2</span>Background</a>
      <a href="#action"><span class="key">3</span>What I did</a>
      <a href="#outcome"><span class="key">4</span>Outcome</a>
    </nav>

    <article class="prose">
      <section id="overview">
        <span class="label">Overview</span>
        <h2>An opportunity hiding in our data</h2>
        <p>Interviews and our data warehouse pointed to the same opportunity: help homeowners realise the savings they could make on private mortgage insurance (PMI), and help our customers, their loan officers and realtors, build trust as their advisors.</p>
        <p>We estimated that around <strong>one million</strong> US homeowners using Homebot were eligible to remove PMI early, saving each of them around <strong>$195 a month</strong>. Together that came to roughly <strong>$200 million a month</strong>.</p>
      </section>

      <section id="background">
        <span class="label">Background</span>
        <h2>Why it mattered in 2022</h2>
        <ul>
          <li>Home prices rose faster than ever in 2021. The typical home gained <strong>$50,000</strong> in value.</li>
          <li>Nearly two-thirds of US households struck by COVID-19 faced financial trouble.</li>
          <li>PMI lets buyers without a 20% down payment become homeowners. It can be removed once the loan-to-value ratio falls below 80% of the original appraised value, or sooner if the home has appreciated.</li>
        </ul>
        <div class="callout">{SPARK}<p>Rising prices meant many homeowners may already have crossed that line without realising it.</p></div>
      </section>

      <section id="action">
        <span class="label">What I did</span>
        <h2>Prototype widely, test hard, ship in slices</h2>
        <ul>
          <li><strong>Explored broadly.</strong> I sketched and rapidly prototyped variations on copy, infographics and visualisations, and on ways to connect homeowners with their loan officers and realtors.</li>
          <li><strong>Tested with 20 people.</strong> I ran usability sessions with 20 participants and landed on a design rated <strong>4.8 out of 5</strong> on its value and on confidence in removing PMI.</li>
          <li><strong>Planned delivery with engineering.</strong> With the engineering leads I broke the design into four sprints, each the smallest chunk of deliverable value.</li>
        </ul>
        <div class="fig-pair">
          <figure class="fig"><div class="shot"><img src="../assets/pmi-iterations.png" alt="Figma board of PMI screen iterations"></div><figcaption>Iterations on copy, visualisations and contact options.</figcaption></figure>
          <figure class="fig"><div class="shot"><img src="../assets/pmi-handoff.png" alt="Figma handoff board with light and dark mode screens"></div><figcaption>Handoff, including light mode.</figcaption></figure>
        </div>
      </section>

      <section id="outcome">
        <span class="label">Outcome</span>
        <h2>500 requests in the first sprint</h2>
        <ul>
          <li>Within the first sprint, homeowners sent <strong>over 500 requests</strong> to learn more about cancelling PMI, worth around <strong>$97,500 a month</strong> in savings.</li>
          <li>I presented the project to the whole company using the Double Diamond framework. It connected colleagues to our mission, showed how the product org works, and built excitement for the feature.</li>
        </ul>
        <a class="video" href="https://www.youtube.com/watch?v=7k9B34Jx0yg">
          <img src="../assets/pmi-video.jpg" alt="Video still of the PMI feature: 'When can you remove your monthly mortgage insurance? Soon.' with a 16% progress bar">
          <span class="play"><i></i>Watch the walkthrough</span>
        </a>
      </section>
    </article>
  </div>

  <div class="wrap next">
    <a class="card c-orange" href="https://www.mjongbloet.com/portfolio/home-search">
      <div class="stack" style="gap:14px"><span class="label" style="color:var(--on-color)">Next project</span><h3>Home Search</h3><p>Turning a newly acquired search product into an experience that holds its own.</p><span class="go">View project <i aria-hidden="true">→</i></span></div>
      <div class="frame"><img src="../assets/home-search.jpg" alt=""></div>
    </a>
  </div>
</main>
"""

ABOUT = f"""<main>
  <section class="wrap ab-hero">
    <div class="hero-copy">
      <div class="avatar"><img src="../assets/headshot.jpg" alt=""><span class="dot" aria-hidden="true"></span></div>
      <h1 class="sentence">I always knew I wanted to use design to make people’s lives a little <em>better</em>.</h1>
      <p class="based">{FLAG}<span>Senior Staff Product Designer at Hospitable, based in Amsterdam, NL</span></p>
    </div>
    <div class="portrait">
      <img src="../assets/headshot.jpg" alt="Matt Jongbloet smiling in front of a colourful mural">
      {ST_SPARK}
      <span class="sticker st-pill" aria-hidden="true">Amsterdam</span>
    </div>
  </section>

  <div class="wrap"><div class="wide"><img src="../assets/nepal.jpeg" alt="Two hikers standing on a ridge in front of snow-capped Himalayan peaks in Nepal"></div></div>

  <section class="wrap story">
    <span class="label" style="padding-top:12px">My story</span>
    <div class="prose">
      <p class="lead">The first five years of my career, in visual and brand design, left me feeling like I was making nice-looking things without a purpose.</p>
      <p>So I left Canterbury, England for an MSc in Digital Design in Amsterdam. There I learned the fundamentals of lab, field and showroom research, and experimented with new methods on real projects for large companies. My next step was to find a place where I could deliver dev-ready designs and also conduct research.</p>
      <p>I got lucky. After marrying my now wife, I moved to the USA, where I played pivotal design roles for 5+ years at early- and mid-stage SaaS companies. I’ve since moved back to Amsterdam, where I help hosts run their short-term rentals on autopilot at <a href="https://hospitable.com/">Hospitable</a>.</p>
    </div>
  </section>

  <section class="wrap section">
    <div class="row-head" style="padding-top:0"><h2>The route so far ↓</h2></div>
    <ol class="route">
      <li class="c-yellow"><span class="step">01 · Canterbury, England</span><span class="place">Visual &amp; brand design</span><span class="what">Five years making things look good, and wanting them to do more.</span></li>
      <li class="c-orange"><span class="step">02 · Amsterdam, NL</span><span class="place">MSc Digital Design</span><span class="what">Lab, field and showroom research on real projects for large companies.</span></li>
      <li class="c-blue"><span class="step">03 · USA</span><span class="place">5+ years of SaaS</span><span class="what">Pivotal design roles at early- and mid-stage companies, including Homebot and Trellis.</span></li>
      <li class="c-green"><span class="step">04 · Amsterdam, NL</span><span class="place">Hospitable</span><span class="what">Senior Staff Product Designer on software that runs short-term rentals on autopilot.</span></li>
    </ol>
  </section>

  <section class="wrap section" style="padding-top:8px">
    <div class="split">
      <div>
        <p class="sub">Credentials</p>
        <div class="creds">
          <div><b>MSc Digital Design, Cum Laude</b><span>Amsterdam</span></div>
          <div><b>UX Certification (UXC)</b><span>Nielsen Norman Group</span></div>
          <div><b>15+ years designing</b><span>10+ of them in product design</span></div>
        </div>
      </div>
      <div>
        <p class="sub">Experience</p>
        <ul class="xp">
          <li><span class="role">Senior Staff Product Designer</span><span class="when num">Mar 2024 — Now</span><a class="co" href="https://hospitable.com/">Hospitable</a></li>
          <li><span class="role">Lead Product Designer</span><span class="when num">Feb 2024 — Mar 2025</span><a class="co" href="https://www.carv.com/">Carv</a></li>
          <li><span class="role">Staff Product Designer, Growth</span><span class="when num">Jan 2022 — Feb 2023</span><a class="co" href="https://savvy.insure/">Trellis</a></li>
        </ul>
        <a class="small-link" href="{CV}">Download full resume (PDF) →</a>
      </div>
    </div>
  </section>
</main>
"""

PAGES = {
    "index.html": ("Matt Jongbloet — Senior Staff Product Designer", "Senior staff product designer at Hospitable with 15+ years of experience, based in Amsterdam.", "Home", HOME),
    "case-pmi.html": ("PMI Savings — Matt Jongbloet", "Helping ≈1 million US homeowners discover they can drop private mortgage insurance early.", "Work", CASE),
    "about.html": ("About — Matt Jongbloet", "From brand design in Canterbury to research in Amsterdam, five years of SaaS in the US, and back to Amsterdam.", "About", ABOUT),
}

if __name__ == "__main__":
    for name, (title, desc, cur, body) in PAGES.items():
        open(os.path.join(OUT, name), "w").write(head(title, desc) + header(cur) + "\n" + body + "\n" + CONTACT)
    print("built p-sentence")
