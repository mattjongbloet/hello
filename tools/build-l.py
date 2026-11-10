"""Build Direction L pages from redesigns/l-terminal/src/*.html: injects shared tabs (<!--TABS:key-->) and prompt (<!--PROMPT-->)."""
import glob, os, re
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "redesigns", "l-terminal")
tabs, prompt = open(os.path.join(D, "_tabs.html")).read(), open(os.path.join(D, "_prompt.html")).read()
for src in glob.glob(os.path.join(D, "src", "*.html")):
    s = open(src).read()
    m = re.search(r"<!--TABS:(\w+)-->", s)
    t = tabs.replace(f'data-t="{m.group(1)}"', f'data-t="{m.group(1)}" aria-current="page"') if m else tabs
    s = re.sub(r"<!--TABS:\w+-->", t, s).replace("<!--PROMPT-->", prompt)
    open(os.path.join(D, os.path.basename(src)), "w").write(s)
    print("built", os.path.basename(src))
