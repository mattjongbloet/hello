"""Shared parts for Matt's current site (redesigns/site + redesigns/case-studies):
the header (face, name, role · Work, About, Resume, theme toggle, Let's talk), the light/dark theme, and their CSS.
Used by tools/build-a-cv.py and tools/build-case-studies.py.
"""
import re

CV = "https://cdn.prod.website-files.com/63b35214bc1dc0317e22bd99/668ae1b79c5572bfad32e508_Matt_Jongbloet_CV_2024.pdf"

# Set the theme before first paint (saved choice, else light) so there is no flash.
THEME_HEAD = """<script>try { document.documentElement.dataset.theme = localStorage.getItem('mj-theme') || 'light'; } catch (e) { document.documentElement.dataset.theme = 'light'; }</script>"""

SUN = '<svg class="i-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="1.8"/><g stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M12 2.5v2.4M12 19.1v2.4M2.5 12h2.4M19.1 12h2.4M5.3 5.3l1.7 1.7M17 17l1.7 1.7M5.3 18.7 7 17M17 7l1.7-1.7"/></g></svg>'
MOON = '<svg class="i-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.2A8.2 8.2 0 0 1 9.8 4a8.2 8.2 0 1 0 10.2 10.2Z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>'


def header(home, current, work_href=None, about_href=None):
    """home: path prefix to the site's home folder ('' on the home page itself)."""
    work_href = work_href or f"{home}index.html#work"
    about_href = about_href or f"{home}about.html"
    cur = lambda k: ' aria-current="page"' if k == current else ""
    keep = ' class="keep"' if current == "about" else ""
    return f"""<header class="top">
  <div class="wrap">
    <a class="brand" href="{home}index.html"><img class="face" src="../assets/headshot.jpg" alt=""><span class="brand-name">Matt Jongbloet</span><span class="brand-role">Product Designer</span></a>
    <nav class="nav" aria-label="Main">
      <a href="{work_href}"{cur("work")}>Work</a>
      <a href="{about_href}"{cur("about")}{keep}>About</a>
      <a href="{CV}">Resume</a>
    </nav>
    <button class="theme-toggle" type="button" aria-label="Switch to dark mode" aria-pressed="false">{MOON}{SUN}</button>
    <a class="btn ghost talk" href="#contact">Let’s talk</a>
  </div>
</header>"""


HEADER_RE = re.compile(r'<header class="top">.*?</header>', re.S)

THEME_JS = """
// Light / dark theme: remembers the choice, swaps mockups that have a dark version.
(() => {
  const root = document.documentElement; let theme = root.dataset.theme || 'light';
  const apply = () => {
    root.dataset.theme = theme;
    document.querySelectorAll('.theme-toggle').forEach((b) => { b.setAttribute('aria-pressed', String(theme === 'dark')); b.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'); });
    document.querySelectorAll('img[data-dark]').forEach((img) => { if (!img.dataset.light) img.dataset.light = img.getAttribute('src'); const src = theme === 'dark' ? img.dataset.dark : img.dataset.light; if (img.getAttribute('src') !== src) img.setAttribute('src', src); });
  };
  apply();
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.theme-toggle')) return;
    theme = theme === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem('mj-theme', theme); } catch (err) { /* private mode: the choice just won't persist */ }
    apply();
  });
})();
"""

HEADER_CSS = """
/* Header: face, name and role on the left; Work, About, Resume, theme toggle and Let's talk on the right. */
.top .wrap { gap: 28px; }
.brand { gap: 12px; font-weight: 600; font-size: 16px; }
.brand img.face { width: 34px; height: 34px; border-radius: 50%; object-fit: cover; object-position: 50% 30%; }
.brand-role { font-weight: 400; color: var(--ink-2); }
.nav { gap: 26px; }
.nav a { padding: 8px 0; border-radius: 0; font-size: 16px; color: var(--ink); background: none !important; }
.nav a:hover, .nav a[aria-current="page"] { color: var(--ink); text-decoration: underline; text-underline-offset: 6px; text-decoration-thickness: 1.5px; }
.theme-toggle { display: grid; place-items: center; width: 40px; height: 40px; padding: 0; border: 0; border-radius: 50%; background: none; color: var(--ink); box-shadow: inset 0 0 0 1.5px var(--line); cursor: pointer; transition: box-shadow .15s; }
.theme-toggle:hover { box-shadow: inset 0 0 0 1.5px var(--ink); }
.theme-toggle svg { width: 20px; height: 20px; }
.theme-toggle .i-sun { display: none; }
:root[data-theme="dark"] .theme-toggle .i-sun { display: block; }
:root[data-theme="dark"] .theme-toggle .i-moon { display: none; }
.top .btn.talk { padding: 10px 20px; color: var(--ink); background: transparent; box-shadow: inset 0 0 0 1.5px var(--ink); }
.top .btn.talk:hover { background: var(--ink); color: var(--paper); }
@media (max-width: 760px) { .brand-role { display: none; } .top .wrap { gap: 14px; } .nav { gap: 16px; } }
@media (max-width: 560px) { .top .btn.talk { padding: 9px 14px; } .brand-name { font-size: 15px; } }
@media (max-width: 350px) { .brand-name { display: none; } }
"""

DARK_CSS = """
/* Dark theme (the toggle in the header). Same palette as the earlier A4 Night variant. */
:root[data-theme="dark"] {
  color-scheme: dark;
  --paper: #0e0f11; --mist: #18191d; --line: #2a2c32;
  --ink: #f1f2f4; --ink-2: #a2a6ae;
  --signal: #ff6a2b; --signal-soft: #2a1a12; --signal-ink: #ff8a57;
}
:root[data-theme="dark"] .btn:hover { background: #ffffff; }
:root[data-theme="dark"] .btn.ghost:hover { box-shadow: inset 0 0 0 1.5px var(--ink); background: transparent; }
:root[data-theme="dark"] .top .btn.talk:hover { background: var(--ink); color: var(--paper); }
:root[data-theme="dark"] .prose p, :root[data-theme="dark"] .prose li, :root[data-theme="dark"] .plate-cap p, :root[data-theme="dark"] .phase-body p { color: #c9ccd2; }
:root[data-theme="dark"] .video .play { background: #1d1f24; color: var(--ink); }
:root[data-theme="dark"] .contact { background: #17181c; color: var(--ink); border-top: 1px solid var(--line); }
:root[data-theme="dark"] .contact .btn { background: var(--ink); color: var(--paper); }
:root[data-theme="dark"] .contact .btn:hover { background: var(--signal); color: #fff; }
:root[data-theme="dark"] .contact p, :root[data-theme="dark"] .contact .plain { color: var(--ink-2); }
:root[data-theme="dark"] .contact .plain:hover { color: var(--ink); }
:root[data-theme="dark"] .foot { background: #17181c; color: var(--ink-2); }
:root[data-theme="dark"] .foot .wrap { border-top-color: var(--line); }
:root[data-theme="dark"] .foot a:hover { color: var(--ink); }
:root[data-theme="dark"] .work-band { background: #131417; }
:root[data-theme="dark"] .pcard { background: var(--mist); border-color: var(--line); }
:root[data-theme="dark"] .pcard:hover { box-shadow: 0 20px 44px -26px rgb(0 0 0 / .9); }
:root[data-theme="dark"] .pc-shot.has-dark { background: #0d0e11; }
:root[data-theme="dark"] .pc-logo { opacity: .92; }
:root[data-theme="dark"] .cs-cover.has-dark { background: #0d0e11; }
:root[data-theme="dark"] .ph { background: #3a2f0d; color: #ffd978; border-bottom-color: #b98c00; }
:root[data-theme="dark"] .todo-card { background: #1c1809; border-color: #8a6a00; }
:root[data-theme="dark"] .todo-card .eyebrow { color: #ffd978; }
:root[data-theme="dark"] .cover-ph, :root[data-theme="dark"] .snap-visual { background: repeating-linear-gradient(45deg, #18191d, #18191d 12px, #1f2126 12px, #1f2126 24px); }
:root[data-theme="dark"] .next-ph { background: var(--mist); }
"""
