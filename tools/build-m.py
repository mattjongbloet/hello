"""Build Direction M decks from redesigns/m-deck/src/*.html, injecting the shared chrome at <!--CHROME:key-->."""
import glob, os, re
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "redesigns", "archive", "m-deck")
chrome = open(os.path.join(D, "_chrome.html")).read()
for src in glob.glob(os.path.join(D, "src", "*.html")):
    s = open(src).read()
    m = re.search(r"<!--CHROME:(\w+)-->", s)
    c = chrome.replace(f'data-d="{m.group(1)}"', f'data-d="{m.group(1)}" aria-current="page"')
    open(os.path.join(D, os.path.basename(src)), "w").write(re.sub(r"<!--CHROME:\w+-->", c, s))
    print("built", os.path.basename(src))
