"""Three working demos for the right-hand side of A6.1's hero (Matt's chosen home page):
  a6-1-hero-untangle      — 1 · a tangled line that becomes a clean circle as the cursor approaches
  a6-1-hero-object-face   — 2 · a face made of things Matt likes; each piece wakes on hover and opens on click
  a6-1-hero-face-follows  — 4 · an illustrated portrait that turns to follow the cursor
Each is a copy of redesigns/a6-1-feel-simple with the toy from tools/toys/ added to the home page.
Run after tools/build-a-cv.py:  python3 tools/build-hero-toys.py
"""
import os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "redesigns", "a6-1-feel-simple")
TOYS = os.path.join(ROOT, "tools", "toys")
VARIANTS = {"a6-1-hero-untangle": "untangle", "a6-1-hero-object-face": "object-face", "a6-1-hero-face-follows": "face-follows"}


def read(name):
    return open(os.path.join(TOYS, name)).read()


def build():
    for folder, toy in VARIANTS.items():
        out = os.path.join(ROOT, "redesigns", folder)
        if os.path.isdir(out):
            shutil.rmtree(out)
        shutil.copytree(SRC, out)
        p = os.path.join(out, "index.html"); s = open(p).read()
        a = '<section class="wrap hero hero-text">'
        assert s.count(a) == 1, folder
        s = s.replace(a, '<section class="wrap hero hero-text has-toy">')
        end = "    </div>\n  </section>"
        i = s.index(end, s.index("has-toy")) + len("    </div>\n")
        s = s[:i] + read(toy + ".html") + s[i:]
        link = '<link rel="stylesheet" href="variant.css">'
        assert s.count(link) == 1
        s = s.replace(link, link + '\n<link rel="stylesheet" href="toy.css">')
        js = '<script src="script.js"></script>'
        assert s.count(js) == 1
        s = s.replace(js, js + '\n<script src="toy.js"></script>')
        open(p, "w").write(s)
        open(os.path.join(out, "toy.css"), "w").write(read("toy-base.css") + "\n" + read(toy + ".css"))
        shutil.copy(os.path.join(TOYS, toy + ".js"), os.path.join(out, "toy.js"))
        print("built", folder)


if __name__ == "__main__":
    build()
