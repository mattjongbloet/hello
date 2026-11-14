"""Matt's case studies, all in his chosen format:
  opening  — title, intro, facts row, cover image, metric tiles
  body     — contents menu on the left; Context → Opportunity → Approach → Outcome
Content: the seven case studies from mjongbloet.com (text tightened, facts kept; images from the live site),
plus Trellis (from Matt's deck) and two templates (Carv, Hospitable) with placeholders.
Shared pieces come from tools/build-cases.py, tools/build-pmi-formats.py and tools/site_parts.py.
Re-run: python3 tools/build-case-studies.py
"""
import importlib.util, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import site_parts as sp


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, file))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


bc = load("build_cases", "build-cases.py")
pf = load("build_pmi_formats", "build-pmi-formats.py")
ph, HOME, IMG = bc.ph, bc.HOME, "../assets/"
C = IMG + "cases/"
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


def meta(rows):
    return f'<dl class="meta{" meta5" if len(rows) == 5 else ""}">' + "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in rows) + "</dl>"


def team(people, note=""):
    """Teammates as linked avatars. A photo at assets/team/<linkedin-handle>.jpg is used if present, otherwise initials."""
    out = []
    for name, handle in people:
        photo = os.path.join(HERE, "..", "redesigns", "assets", "team", handle + ".jpg")
        face = f'<img src="{IMG}team/{handle}.jpg" alt="">' if os.path.exists(photo) else "".join(w[0] for w in name.split()[:2])
        out.append(f'<a class="mate" href="https://www.linkedin.com/in/{handle}/" target="_blank" rel="noopener" aria-label="{name} on LinkedIn" title="{name}"><span class="mate-face">{face}</span></a>')
    return '<span class="team">' + "".join(out) + "</span>" + (f'<span class="team-note">{note}</span>' if note else "")   # avatars only: names live in the link label and tooltip


def opening(crumb, title, dek, rows, cover, tiles):
    t = "".join(f'<div><b class="num">{n}</b><span>{label}</span></div>' for n, label in tiles)
    return f"""  <section class="wrap cs-hero">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{HOME}index.html#work">Work</a><span>/</span><span>{crumb}</span></nav>
    <h1>{title}</h1>
    <p class="dek">{dek}</p>
    {meta(rows)}
  </section>

  <div class="wrap">
    {cover}
    {f'<div class="results n{len(tiles)}">{t}</div>' if tiles else ''}
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
    return html.replace(HOME, SITE)


def ul(*items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def p(*paras):
    return "".join(f"<p>{x}</p>" for x in paras)


def cover(src, alt, dark=None):
    d = f' data-dark="{IMG}{dark}"' if dark else ""
    return f'<div class="cs-cover{" has-dark" if dark else ""}"><img src="{IMG}{src}"{d} alt="{alt}"></div>'


def pair(a, a_alt, a_cap, b, b_alt, b_cap):
    f = lambda src, alt, cap: f'<figure class="fig"><div class="frame"><img src="{C}{src}" alt="{alt}" loading="lazy"></div><figcaption>{cap}</figcaption></figure>'
    return f'<div class="fig-pair">{f(a, a_alt, a_cap)}{f(b, b_alt, b_cap)}</div>'


def video(href, still, alt, label="Watch the walkthrough"):
    return f"""<a class="video" href="{href}">
          <img src="{still}" alt="{alt}" loading="lazy">
          <span class="play"><i></i>{label}</span>
        </a>"""


YT = "https://www.youtube.com/watch?v="
ROLE = "Senior Product Designer"

# ---------------------------------------------------------------- the case studies, in the order they appear on the home page
# key: (file, card title for "next project", next-project visual)
ORDER = ["trellis", "pmi", "home-search", "internal-admin", "scaling-research", "digital-health", "home-value-estimates", "location-based-game"]
NEXT_INFO = {
    "trellis": ("Trellis: growth experiments", f'<img src="{T}cover-v2.jpg" alt="">'),
    "pmi": ("Private Mortgage Insurance", f'<img src="{IMG}pmi-thumb.png" alt="">'),
    "home-search": ("Home Search", f'<img src="{IMG}home-search.jpg" alt="">'),
    "internal-admin": ("Internal Admin", f'<img src="{IMG}internal-admin.jpg" alt="">'),
    "scaling-research": ("Scaling Research", f'<img src="{IMG}scaling-research.png" alt="">'),
    "digital-health": ("Digital Health", f'<img src="{IMG}digital-health.jpg" alt="">'),
    "home-value-estimates": ("Home Value Estimates", f'<img src="{IMG}home-value.png" alt="">'),
    "location-based-game": ("Location-Based Game", f'<img src="{IMG}wwf-game.jpg" alt="">'),
}


def nxt(key):
    k = ORDER[(ORDER.index(key) + 1) % len(ORDER)]
    return nextp(f"{k}.html", *NEXT_INFO[k])


PAGES = {}

# ---- PMI (Homebot, July 2022)
LI_PRICES = 'Home prices rose faster than ever in 2021. The typical home gained <strong>$50,000</strong> in value (<a href="https://www.npr.org/2022/01/20/1074377076/home-prices-rose-faster-than-ever-in-2021-the-typical-home-gained-50-000-in-valu">NPR</a>).'
LI_COVID = 'Nearly two-thirds of US households struck by COVID-19 faced financial trouble (<a href="https://www.npr.org/sections/health-shots/2020/09/28/916605221/nearly-two-thirds-of-u-s-households-struck-by-covid-19-face-financial-trouble">NPR</a>).'
PAGES["pmi"] = page("PMI Savings — Matt Jongbloet", "Helping ≈1 million US homeowners discover they can drop private mortgage insurance early.",
    opening("Private Mortgage Insurance", pf.TITLE, pf.DEK, pf.META, cover("pmi-mockup.png", pf.COVER_ALT, "pmi-mockup-dark.png"),
            [("≈$200M", "a month in estimated savings for homeowners"), ("≈1M", "US homeowners on Homebot eligible to remove PMI early"), ("$195", "estimated monthly saving per homeowner"),
             ("4.8/5", "rating for value and confidence in usability testing"), ("500+", "requests to learn about PMI removal in the first sprint")])
    + body([
        ("context", "Context", "Why it mattered in 2022", ul(LI_PRICES, LI_COVID, pf.LI_PMI) + f'<p class="callout">{pf.CALLOUT}</p>'),
        ("opportunity", "Opportunity", "An opportunity hiding in our data", p(pf.P_OPPORTUNITY, pf.P_SIZE)),
        ("approach", "Approach", "Prototype widely, test hard, ship in slices", ul(pf.LI_EXPLORE, pf.LI_TEST, pf.LI_PLAN) + pf.FIG_PAIR),
        ("outcome", "Outcome", "500 requests in the first sprint", ul(pf.LI_REQUESTS, pf.LI_PRESENT) + pf.VIDEO),
    ]) + nxt("pmi"))

# ---- Home Search (Homebot, October 2021)
PAGES["home-search"] = page("Home Search — Matt Jongbloet", "Helping ≈10 million people find their next home.",
    opening("Home Search", "Helping ≈10 million people find their next home",
            "Homebot bought a home search product and integrated it in 100 days. I then redesigned the parts that mattered most, so it could stand next to Zillow, Redfin and Realtor.",
            [("Company", "Homebot"), ("My role", ROLE), ("Team", "Consumer Team"), ("Date", "October 2021")],
            cover("home-search.jpg", "Home Search on mobile: a search screen and a map of listings in Denver", "home-search-dark.jpg"),
            [("≈10M", "people helped to find their next home"), ("100 days", "to integrate the newly acquired NestReady search"), ("5 areas", "redesigned: search, navigation, map clusters, map markers and the landing page")])
    + body([
        ("context", "Context", "A new product, integrated in 100 days",
         ul("Homebot acquired NestReady, a home search product, in August 2021 and set a target to integrate it within 100 days.",
            "That meant adding an entirely new channel, search, to our product, with knock-on effects for styling, navigation, core emails and customers.",
            "We hit the launch date, with a lot of de-scoping and porting, and a sub-par user experience.")),
        ("opportunity", "Opportunity", "Table stakes against Zillow, Redfin and Realtor",
         p("After the 100-day launch we ran moderated usability sessions. They identified the table-stakes areas we needed to improve to even be considered against the likes of Zillow, Redfin and Realtor: <strong>searching, the map and list display of results, the listing detail page, clusters and map markers</strong>.")),
        ("approach", "Approach", "Prototype, test, prioritise, and bring the engineers along",
         ul("<strong>Sketched and prototyped.</strong> I rapidly prototyped responsive designs for the key jobs to be done in search. I focused on search, navigation, map clusters, map markers and the landing page, and paired with another designer on listing results and listing detail.",
            "<strong>Tested before building.</strong> I usability tested low- and high-fidelity prototypes to raise confidence in the direction before committing to code.",
            "<strong>Prioritised with the squad.</strong> We groomed the improvements by impact and effort and created a product backlog.",
            "<strong>Put engineers in the room.</strong> I ran usability sessions on Lookback.io where every engineer on the team watched people use our experience, building empathy and a team of missionaries.")
         + pair("home-search-1.jpg", "Map designs for Home Search with clusters and price markers", "Map clusters and markers.", "home-search-2.jpg", "A listing screen with an option to schedule a tour", "Listing detail on mobile.")),
        ("outcome", "Outcome", "A search people could use, and a team that cared",
         ul("A significantly improved, usable and useful home search, measured through Amplitude and UX benchmarking (SEQ and time on task).",
            "An organisation that understood why, how and what the product team was building to create value for customers.",
            "A team rapidly delivering small chunks of value, following a process similar to the Double Diamond.",
            "Engineers presented a demo of the improvements to the entire company, speaking in the voice of the user.",
            "Engineers were so keen to solve problems for users that they picked this work up during HIP sprints.")
         + video(YT + "9kOzyQfzoiM", C + "home-search-video.jpg", "Video still: a walkthrough of the Home Search experience")),
    ]) + nxt("home-search"))

# ---- Internal Admin (Homebot, January 2020)
PAGES["internal-admin"] = page("Internal Admin — Matt Jongbloet", "≈80% decrease in the time needed to complete 20+ key tasks.",
    opening("Internal Admin", "Cutting the time for 20+ key tasks by ≈80%",
            "Homebot’s internal team had spent three years working around a tool that was built in three days. I redesigned it around the tasks they actually do.",
            [("Company", "Homebot"), ("My role", ROLE), ("Team", "Homebotters"), ("Date", "January 2020")],
            cover("internal-admin.jpg", "The redesigned Homebot admin: a contracts table with status and plan columns"),
            [("≈80%", "less time needed to complete key tasks"), ("20+", "key tasks made faster"), ("15+ → 3", "steps in workflows after the redesign"), ("26", "team members surveyed about their tasks"), ("3 years", "of workarounds replaced")])
    + body([
        ("context", "Context", "Built in three days, used for three years",
         ul("A developer had used a CSS Bootstrap template to build an internal tool for managing customers and users. It was built in three days.",
            "Over the following three years, our internal team struggled with it and came to rely on workarounds.")),
        ("opportunity", "Opportunity", "A team working around its own tool",
         p("Early on at Homebot, I discovered that our internal team had developed a list of “workarounds” to use the admin tool effectively. We decided to fix the critical problems in the current tool while also designing a new version around the team’s key tasks, so they could work more efficiently and effectively.")),
        ("approach", "Approach", "Ask the whole team, then design for their key tasks",
         ul("<strong>Built rapport, then surveyed.</strong> After building rapport with key stakeholders across the org, I gathered feedback from every team leader and member. The survey captured all tasks from a team of 26: the three most important, the most time-consuming, and what they would fix first.",
            "<strong>Played it back.</strong> I synthesised the key tasks by group (Data, CSS, CSM) and sent them back to the team leaders to confirm they had been heard.",
            "<strong>Went deeper.</strong> I ran jobs-to-be-done style interviews to learn more about the tasks.",
            "<strong>Chose the stack together.</strong> With the tech leads on my team we selected Tailwind CSS, React and internal data for the new tool.",
            "<strong>Redesigned around tasks.</strong> I reorganised the information architecture and redesigned the UI with the key tasks in mind.",
            "<strong>Tested with the team.</strong> In usability tests with low- and high-fidelity prototypes, team members imagined doing their current tasks in the new tool. The interface and workflow were entirely different, yet they completed their tasks with no prompting.",
            "<strong>Shipped in small chunks.</strong> We built the new interface piece by piece and redirected from the old tool to the new one, so the team moved over naturally.")
         + pair("internal-admin-1.jpg", "Screens from the redesigned admin tool", "Screens from the new admin.", "internal-admin-2.jpg", "A list of the team’s key tasks grouped by team", "Key tasks, grouped by team.")),
        ("outcome", "Outcome", "≈80% less time on 20+ key tasks",
         ul("An <strong>≈80% decrease</strong> in the time needed to complete 20+ key tasks.",
            "Workflows that used to take <strong>15+ steps</strong> were redesigned to take <strong>3</strong>.",
            "Significant improvements in efficiency, effectiveness and usability, which made for happier employees.",
            "Key stakeholders supported, and felt connected to, the work and the direction of the roadmap.",
            "Our product squad became enthusiastic about the project, because they could empathise with the challenges the internal team faced.")
         + video(YT + "19XjXqNr1Ug", C + "internal-admin-video.jpg", "Video still: a walkthrough of the redesigned internal admin")),
    ]) + nxt("internal-admin"))

# ---- Scaling Research (Homebot, January 2021)
PAGES["scaling-research"] = page("Scaling Research — Matt Jongbloet", "Empowering 30+ product people to learn in rigorous ways.",
    opening("Scaling Research", "Empowering 30+ product people to learn in rigorous ways",
            "As Homebot’s product team tripled, I built the repository, roadmap and habits that let non-researchers do research well.",
            [("Company", "Homebot"), ("My role", ROLE), ("Team", "Homebot R&amp;D"), ("Date", "January 2021")],
            cover("scaling-research.png", "The research repository in Dovetail, with project planning templates"),
            [("30+", "product people, up from around 10"), ("47", "research projects in the repository’s first year"), ("5,862", "highlights captured"), ("117", "insights shared"), ("50%", "average exposure of R&amp;D to users’ experiences")])
    + body([
        ("context", "Context", "From 10 product people to more than 30",
         ul("When I joined, the company was at an early stage of research maturity.",
            "Most user research consisted of haphazard customer interviews and scrappy unmoderated usability tests.",
            "Many employees had little exposure to customers.",
            "The number of product people grew from around 10 to more than 30 during my time there.")),
        ("opportunity", "Opportunity", "Better research, done by more people",
         p("Democratisation, involving non-researchers in research, is frequently debated in the product research field. I think it’s more useful to recognise the research these people already do and improve its quality than to ignore it.",
           "So I focused on scaling research: creating a research repository, establishing a research roadmap, leading an Exposure Hours KPI and managing the UXR tools budget.")),
        ("approach", "Approach", "A repository, a roadmap and exposure hours",
         ul("<strong>Research repository.</strong> I created a repository in Dovetail with structured templates for common methods and workshops, a co-created global tagging taxonomy, onboarding materials and an FAQ for new hires.",
            "<strong>Research roadmap.</strong> I created a roadmap aligned with business strategy that gave the right stakeholders visibility.",
            "<strong>Journey mapping.</strong> I led a workshop to produce a foundational map of how we support people through their homeowner and buying journeys.",
            "<strong>Exposure Hours KPI.</strong> I led the KPI, resulting in an average of 50% exposure for R&amp;D to our users’ experiences.",
            "<strong>Teaching.</strong> I presented on the importance of user research and the skill of listening deeply.",
            "<strong>Tools.</strong> I managed the UXR tools budget so the team had the right tools: Lookback, User Interviews, UserTesting, FullStory and Dovetail.")
         + pair("scaling-research-1.png", "The research roadmap layout", "The research roadmap.", "scaling-research-2.png", "A single module from the research roadmap", "One roadmap module.")),
        ("outcome", "Outcome", "47 projects, 5,862 highlights, 117 insights",
         ul("Within the first year of the repository’s launch, we had created <strong>47 projects</strong>, <strong>5,862 highlights</strong> and <strong>117 insights</strong>.",
            "Confidence in conducting research improved, communication about ongoing research improved, and findings were shared more widely, creating teams of missionaries rather than mercenaries.",
            "One of my highlights was watching a team of engineers present user findings, problems and solutions, and how they’re helping people to be more successful, to the entire company.")
         + f'<figure class="fig wide"><div class="frame light"><img src="{C}scaling-research-3.png" alt="The foundational journey map of the homeowner and home buying journeys" loading="lazy"></div><figcaption>The foundational journey map from the workshop.</figcaption></figure>'),
    ]) + nxt("scaling-research"))

# ---- Digital Health (Human API, July 2021)
PAGES["digital-health"] = page("Digital Health — Matt Jongbloet", "Helping convince investors with a compelling story and prototype.",
    opening("Digital Health", "A story and a prototype to convince investors",
            "Human API wanted funding to build a digital health marketplace. In a one-day workshop with the CEO and COO, we found the story, and I built the prototype that told it.",
            [("Company", "Human API"), ("My role", "Consultant"), ("Worked with", "CEO and COO"), ("Date", "July 2021")],
            cover("digital-health.jpg", "A hand holding a phone showing the digital health prototype"),
            [("1 day", "workshop with the CEO and COO"), ("1 story", "chosen as the selling point for investors"), ("Hi-fi", "interactive prototype for the investor presentation")])
    + body([
        ("context", "Context", "A marketplace that needed funding",
         p("Human API wanted to acquire funding to build a digital health marketplace, and needed a compelling story to convince investors.")
         + ul("Consumers who visit healthcare providers and create accounts with Human API demonstrate a willingness to use and leverage the system.")),
        ("opportunity", "Opportunity", "Show people what their health data can do for them",
         p("Human API believed that, given access to their health data and guidance on how to use it, consumers would change their behaviour and make purchasing decisions based on it.",
           "But consumers were unaware of the benefits they could get from personalised savings based on their health data, such as medical ID theft protection, coordinated drug cost savings and special payment programmes for healthcare debt.")),
        ("approach", "Approach", "One day, one story, one prototype",
         ul("<strong>A one-day workshop.</strong> I ran a workshop focused on defining the key persona’s journey and the problem to solve, ideating and sketching possible solutions, and confirming the direction through prototyping.",
            "<strong>Co-created with the CEO and COO.</strong> Together we created the core user journey and persona, and identified the opportunity areas.",
            "<strong>Wireframes, then a prototype.</strong> I created low-fidelity wireframes and a high-fidelity interactive prototype of the chosen solution for presentation to investors.")
         + pair("digital-health-1.png", "Workshop sketches for the digital health marketplace", "Sketches from the workshop.", "digital-health-2.png", "Low-fidelity wireframes of the chosen solution", "Low-fidelity wireframes.")),
        ("outcome", "Outcome", "A story the CEO and COO could take to investors",
         p("The CEO and COO felt confident in the story, the prototype and the presentation slides they would use to acquire funding for a digital marketplace.")
         + video(YT + "4cRYlB7s_Dk", C + "digital-health-video.jpg", "Video still: a walkthrough of the digital health prototype")),
    ]) + nxt("digital-health"))

# ---- Home Value Estimates (Homebot, November 2022)
PAGES["home-value-estimates"] = page("Home Value Estimates — Matt Jongbloet", "Increasing trust and confidence in home value estimates.",
    opening("Home Value Estimates", "Increasing trust and confidence in home value estimates",
            "Every financial insight Homebot gives starts from the estimated value of your home. I redesigned how that number is explained, so homeowners could trust it.",
            [("Company", "Homebot"), ("My role", ROLE), ("Team", "Consumer Team"), ("Date", "November 2022")],
            cover("home-value.png", "Two phone screens showing the redesigned home value estimate", "home-value-dark.png"),
            [("60", "participants in generative and evaluative sessions"), ("9/10", "understood the calculation and trusted it more"), ("3 sprints", "planned with engineering, each the smallest chunk of value")])
    + body([
        ("context", "Context", "The number every insight depends on",
         ul("Homeowners receive a monthly home report with actionable insights based on their monthly home valuation.",
            "The majority of these financial insights use the estimated home value as their baseline.",
            "The home value experience had been designed two years earlier and had several usability and usefulness issues.")),
        ("opportunity", "Opportunity", "Trust in the estimate is trust in the product",
         p("Insights from a variety of sources (UserVoice, customers, clients, Homebotters, data, usability markup and competitor analysis) pointed to an opportunity to increase trust in our home values. That would empower homeowners and customers to make more informed financial decisions, and so increase trust and confidence in our product.")),
        ("approach", "Approach", "Sketch, test with 60 people, plan three sprints",
         ul("<strong>Explored broadly.</strong> I sketched and rapidly prototyped variations on copy, animations, infographics, visualisations and interactions.",
            "<strong>Tested with 60 people.</strong> I ran generative and evaluative usability sessions with 60 participants, landing on a design where <strong>9 out of 10</strong> participants had a general understanding of the calculation and more confidence in its accuracy.",
            "<strong>Planned delivery with engineering.</strong> With the engineering leads I broke the design into three sprints, each the smallest chunk of deliverable value.")
         + pair("home-value-1.png", "Sketches and explorations for the home value estimate", "Sketches and explorations.", "home-value-2.png", "Handoff board for the home value estimate design", "Handoff.")),
        ("outcome", "Outcome", "A solution the whole company had confidence in",
         ul("I presented the project to the entire company using the Double Diamond framework, giving them confidence in a solution to a poorly performing experience and showing how the product org works.",
            "The iteration was in the product backlog and had not reached production when I left Homebot.")
         + video(YT + "-k72Zs1n0C0", C + "home-value-video.jpg", "Video still: a walkthrough of the home value estimate design")),
    ]) + nxt("home-value-estimates"))

# ---- Location-Based Game (WWF, January 2018)
PAGES["location-based-game"] = page("Location-Based Game — Matt Jongbloet", "Using technology to enhance nature experiences for families.",
    opening("Location-Based Game", "Using technology to enhance nature experiences for families",
            "WWF asked us to digitally enhance nature. We designed Delta Rangers, an audio-led adventure that gets families outside and keeps their eyes on the wild.",
            [("Client", "WWF"), ("My role", "Student consultant"), ("Context", "MSc Digital Design project"), ("Date", "January 2018")],
            cover("wwf-game.jpg", "The Delta Rangers app on a phone, lying on a map with binoculars and a camera"),
            [("6–12", "the age of the children it was designed for"), ("3 roles", "for children to play: biologist, explorer or team leader"), ("2nd team", "WWF had a second student team continue the work")])
    + body([
        ("context", "Context", "Nature and technology, working together",
         p("WWF asked us to digitally enhance nature as part of a project for my Master’s. How could these apparent opposites, the artificial and the natural, reinforce one another?",
           "The primary goal was to create awareness of WWF’s active role in local nature preservation and development, and its relevance to the world we live in. The project targeted families with children aged 6–12.")),
        ("opportunity", "Opportunity", "Meaning, not more screen time",
         p("Like most of us, children spend a lot of time behind screens. If we truly want this generation to appreciate the value of nature, there’s nothing like experiencing it for themselves. A location-based game was the way to go.",
           "The temptation of technologies such as AR and VR was strong. But according to research, for children who grow up with an overload of technology, the only way to spark engagement is by creating meaning. So alongside the narrative, striking the right balance between the natural and the artificial was crucial.")),
        ("approach", "Approach", "Delta Rangers: an adventure led by audio",
         p("After comparing different technological and conceptual directions, we decided on an app that:")
         + ul("lets families embark on an adventure together as “Delta Rangers”;",
              "tells the story of the animals primarily through audio, so nobody disconnects from their surroundings;",
              "lets you earn badges by completing direct interactions with nature itself;",
              "gives children a sense of agency, as they take on the role of biologist, explorer or team leader;",
              "adds an educational layer about the animals you encounter;",
              "lets you save your journey, retrace your steps and share the experience through a web-based platform, maximising the reach of WWF’s activities.")
         + pair("wwf-1.png", "Field research for the WWF project", "Field research.", "wwf-2.png", "Research notes and concepts for the game", "Research and concepts.")),
        ("outcome", "Outcome", "WWF kept it going",
         p("Working on a meaningful case like this, for a client like the World Wildlife Fund, was a truly satisfying experience. And the fact that WWF decided to let a second student team keep working on it throughout the final semester pretty much says it all.")
         + video("https://vimeo.com/252616697", C + "wwf-video.jpg", "Video still: a demo of the Delta Rangers app", "Watch the demo")),
    ]) + nxt("location-based-game"))

# ---- Trellis (from Matt's deck)
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


def tfig(src, alt, cap, wide=False):
    return f'<figure class="fig{" wide" if wide else ""}"><a class="frame light" href="{T}{src}"><img src="{T}{src}" alt="{alt}" loading="lazy"></a><figcaption>{cap}</figcaption></figure>'


PAGES["trellis"] = page("Trellis: Growth experiments — Matt Jongbloet", "In 3 months, a small growth team and I ran experiments on around 15 parts of Savvy’s car insurance quote flow: $3.5MM in predicted gross annual revenue.",
    opening("Trellis", "Finding $3.5MM in a car insurance quote flow",
            "In three months, a small growth team and I ran experiments on around 15 parts of Savvy’s car insurance quote flow, and proved we could get more people from “I want a quote” to “here are my offers”.",
            [("Company", "Trellis / Savvy.Insure"), ("My role", "Staff Product Designer, Growth"), ("Team", team([("Drew Bolles", "drew-bolles"), ("Chuong Nguyen", "chuongtnguyen"), ("Alexey Komissarouk", "alexeymk")])), ("Timeframe", "3 months, 2023"), ("Surface", "Car insurance quote flow")],
            open(os.path.join(HERE, "anims", "trellis.html")).read(),   # animated cover: homepage → three questions → offers
            [])   # metric tiles removed on Trellis at Matt's request ($3.5MM, ~15 parts, 3 months, 69.0% vs 60.4%, +14% lift)
    + body([
        ("context", "Context", "Where the business wins or loses",
         p("Savvy.Insure, by Trellis, set out to make insurance easier for everyone. Someone who wants car insurance comes to Savvy, tells us about themselves, their cars and their drivers, and gets quotes back. That flow is where the business makes or loses money.")),
        ("opportunity", "Opportunity", "Four in ten people gave up before their quote",
         f'<p>From 17 to 31 May 2023, <strong>44,846</strong> people started the unlinked application and <strong>26,333</strong> finished it: a completion rate of <strong>58.7%</strong>. Every drop-off was a quote, and revenue, lost.</p>'
         + '<p>Customers could shop in one of two ways. The <strong>linked</strong> path let them sign in to their current insurer, say Progressive, so we could pull their details from that account and find comparable quotes. The <strong>unlinked</strong> path was for anyone without insurance, or who couldn’t sign in: a series of questions asking for the minimum we needed to quote them. This flow is the unlinked path.</p>'
         + tfig("baseline-chart.jpg", "Bar chart: 44,846 started the unlinked application, 26,333 completed it, 58.7% total conversion, 17 to 31 May 2023", "Baseline, 17–31 May 2023: 58.7% of people who started the application completed it.")),
        ("approach", "Approach", "Learn cheaply, decide with evidence",
         ul("<strong>The cheapest way to learn.</strong> Not every experiment needs to be an A/B test. We framed each change as a hypothesis, picked the lightest method that could confirm or disconfirm it, and used A/B tests where we needed statistical confidence.",
            "<strong>One small team, a steady cadence.</strong> With a front-end engineer, a back-end engineer and a growth engineering consultant, I designed and shipped experiments on around 15 parts of the flow in three months.",
            "<strong>Making it a habit.</strong> I co-wrote and presented <em>How do we make good decisions about product investment?</em>, sharing how we chose methods, from interviews to A/B tests, and why learning matters more than being right.")
         + XLOG
         + '<h3 class="sub">Featured experiment: ask for the car before the phone number</h3>'
         + '<p class="callout">Hypothesis: changing the order of the unlinked application flow will increase conversion.</p>'
         + "<p>The control flow opened by asking for name, phone, email and date of birth, before Savvy had given anything back. V2 starts with the car and the drivers, builds up to the policy, and only asks for contact details at the very end, as <em>“Where should we send your offers?”</em></p>"
         + tfig("flow-control.jpg", "Control flow, nine phone screens: basic information with phone and email first, then address, own or rent, vehicle information, vehicles, driver information, drivers, current premium, review", "Control: contact details on the very first screen.", True)
         + tfig("flow-v2.jpg", "V2 flow, nine phone screens: vehicle information, vehicles, tell us about yourself, drivers, home address, own or rent, current premium, review, and where should we send your offers", "V2: vehicles and drivers first, contact details last. Stars mark the steps that moved.", True)
         + tfig("result-chart.jpg", "Bar chart, 1 to 9 June 2023: control 60.4% (8,108 of 13,419 completed), V2 69.0% (8,498 of 12,319 completed)", "1–9 June 2023: control completed 60.4% (8,108 of 13,419); V2 completed 69.0% (8,498 of 12,319).")),
        ("outcome", "Outcome", "$3.5MM in predicted annual revenue",
         ul("Over three months, the experiments added up to <strong>$3.5MM in predicted gross annual revenue</strong>.",
            f'The re-order test lifted completion by <strong>8.6 points</strong>, a 14% relative improvement. {ph("Did V2 ship to everyone? Say so here.")}',
            "We left the team with the infrastructure to run similar tests with ease, and a shared way of deciding what to build.")
         + '<h3 class="sub">What we learned</h3>'
         + ul("<strong>People need Trellis to feel valuable before they give their info.</strong> Order matters.",
              "<strong>Learning is more important than being right.</strong> Good testing infrastructure means more people share ideas, and it takes the HiPPO out of decisions.")),
    ]) + nxt("trellis"),
    bc.todo(["The other experiments: change, hypothesis and result for 4–6 of the ~15.",
             "Whether V2 shipped, and anything you know about the effect after launch.", "How the $3.5MM was predicted. One line makes it far more credible."]))


# ---- Templates for the projects still to write (not linked from the home page yet)
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


PAGES["carv"] = template("Carv", "Carv", "Lead Product Designer", "Helping recruiters cut admin and boost hires.", "hospitable.html", "Hospitable", '<span class="next-ph">Hospitable</span>',
                ["Which Carv project to feature, and a title that sells the outcome.", "Team and timeframe.", "Five numbers for the tiles (results, scope, pace).",
                 "Context, opportunity, approach, outcome: a few lines each. Worth including: how you set the future vision with the C-level, and what the research changed.", "Visuals: cover, process, shipped screens."])
PAGES["hospitable"] = template("Hospitable", "Hospitable", "Senior Staff Product Designer", "Helping hosts run their short-term rentals on autopilot.", "trellis.html", *NEXT_INFO["trellis"],
                ["Which Hospitable project to show, and how much you can share.", "Team and timeframe.", "Five numbers for the tiles (or fewer; the row adapts).",
                 "Context, opportunity, approach, outcome: a few lines each.", "Visuals you’re allowed to show (crop or blur where needed)."])

CSS = """/* Matt's case-study format (tools/build-case-studies.py). Adds to style.css + case.css. */
/* Team in the facts row: linked avatars (photo or initials) with names, then a short note. */
.team { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 4px; }
.mate { display: inline-flex; border-radius: 50%; transition: transform .15s, box-shadow .15s; }
.mate:hover { transform: translateY(-2px); box-shadow: 0 0 0 2px var(--paper), 0 0 0 3.5px var(--signal); }
.mate-face { display: grid; place-items: center; width: 44px; height: 44px; border-radius: 50%; overflow: hidden; flex: none; background: color-mix(in srgb, var(--ink) 8%, transparent); font-size: 11px; font-weight: 600; letter-spacing: .02em; color: var(--ink-2); }
.mate-face img { width: 100%; height: 100%; object-fit: cover; }
.team-note { display: block; margin-top: 6px; font-size: 13px; color: var(--ink-2); }
.cs-hero { padding-bottom: 32px; }
.cs-hero h1 { max-width: 19ch; }
.cs-cover, .cover { margin-top: 0; }
.cs-cover img { width: 100%; }

/* Metric tiles under the cover: three to five */
.results { gap: 12px; margin-top: 12px; }
.results.n3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.results.n4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
.results.n5 { grid-template-columns: repeat(5, minmax(0, 1fr)); }
.results div { padding: 20px; }
.results b { padding-top: 2px; }
.results span { font-size: 14px; }

/* Body */
.cs-body { padding-top: 96px; }
.toc a { border-radius: 0 8px 8px 0; }
.prose h3.sub { font-size: 22px; font-weight: 700; letter-spacing: -0.02em; line-height: 1.25; margin-top: 28px; }
.prose a { color: var(--ink); }
.cover-ph.small { min-height: 220px; border-radius: 14px; }
.fig-pair .frame { height: 100%; }
.fig-pair .frame img { width: 100%; height: 100%; object-fit: cover; }

@media (max-width: 1000px) {
  .results.n5 { grid-template-columns: repeat(6, minmax(0, 1fr)); }
  .results.n5 div { grid-column: span 2; }
  .results.n5 div:nth-child(-n+2) { grid-column: span 3; }
}
@media (max-width: 560px) {
  .results.n5, .results.n4 { grid-template-columns: 1fr 1fr; }
  .results.n5 div, .results.n5 div:nth-child(-n+2) { grid-column: auto; }
  .results.n5 div:first-child { grid-column: 1 / -1; }
  .results.n3 { grid-template-columns: 1fr; }
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
    for name, html in PAGES.items():
        open(os.path.join(OUT, name + ".html"), "w").write(html)
    print("built case-studies:", ", ".join(PAGES))


if __name__ == "__main__":
    build()
