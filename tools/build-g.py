"""Build Direction G pages: inject the shared sidebar into redesigns/g-doc/src/*.html.
The marker <!--SIDE:key--> marks which page is current (home, case, about)."""
import glob, os, re
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "redesigns", "archive", "g-doc")
side = open(os.path.join(D, "_side.html")).read()
for src in glob.glob(os.path.join(D, "src", "*.html")):
    s = open(src).read()
    m = re.search(r"<!--SIDE:(\w+)-->", s)
    cur = side
    for key in ([m.group(1), m.group(1) + "-m"] if m else []):
        cur = cur.replace(f'data-p="{key}"', f'data-p="{key}" aria-current="page"')
    s = re.sub(r"<!--SIDE:\w+-->", cur, s)
    open(os.path.join(D, os.path.basename(src)), "w").write(s)
    print("built", os.path.basename(src))
