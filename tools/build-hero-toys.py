"""Working demos for the right-hand side of A6.1's hero (Matt's chosen home page):
  a6-1-hero-untangle      — 1 · a tangled 3D cord that becomes a clean ring as the cursor approaches
  a6-1-hero-object-face   — 2 · a face made of 3D objects Matt likes; each piece wakes on hover and opens on click
Both render with three.js (WebGL): physically based materials, reflections, soft shadows.
Each is a copy of redesigns/a6-1-feel-simple with the toy from tools/toys/ added to the home page.
Run after tools/build-a-cv.py:  python3 tools/build-hero-toys.py
"""
import os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "redesigns", "a6-1-feel-simple")
TOYS = os.path.join(ROOT, "tools", "toys")
VARIANTS = {"a6-1-hero-untangle": ("a6-1-feel-simple", "untangle"), "a6-1-hero-object-face": ("a6-1-feel-simple", "object-face"),
            "site": ("site", "object-face")}   # the current site gets the object face in place
THREE = '<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>'  # classic build: also works from file://


def read(name):
    return open(os.path.join(TOYS, name)).read()


def build():
    for folder, (src, toy) in VARIANTS.items():
        out = os.path.join(ROOT, "redesigns", folder)
        if src != folder:
            if os.path.isdir(out):
                shutil.rmtree(out)
            shutil.copytree(os.path.join(ROOT, "redesigns", src), out)
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
        s = s.replace(js, js + '\n' + THREE + '\n<script src="toy.js"></script>')
        open(p, "w").write(s)
        open(os.path.join(out, "toy.css"), "w").write(read("toy-base.css") + "\n" + read(toy + ".css"))
        open(os.path.join(out, "toy.js"), "w").write(read("three-common.js") + "\n" + read(toy + ".js"))
        print("built", folder)


if __name__ == "__main__":
    build()
