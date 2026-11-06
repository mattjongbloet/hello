"""Regenerate the web-sized JPEGs from the full PNGs and update sizes in shots/_manifest/*.json.

  python3 tools/rethumb.py [site-id ...]
"""
import json, os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
from img import Image  # noqa: E402  (img.py lifts PIL's pixel limit)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIDTH = {"1440": 640, "390": 390}

for f in sorted(glob.glob(os.path.join(ROOT, "shots/_manifest/*.json"))):
    site = os.path.basename(f)[:-5]
    if len(sys.argv) > 1 and site not in sys.argv[1:]:
        continue
    entry = json.load(open(f))
    for page in entry["pages"].values():
        for w, shot in (page.get("shots") or {}).items():
            if shot.get("error") or not shot.get("file"):
                continue
            src, out = os.path.join(ROOT, shot["file"]), os.path.join(ROOT, shot["web"])
            with Image.open(src) as im:
                im = im.convert("RGB")
                tw = WIDTH[w]
                if im.width > tw:
                    im = im.resize((tw, round(im.height * tw / im.width)), Image.LANCZOS)
                im.save(out, "JPEG", quality=78, optimize=True, progressive=True)
                shot["web_width"], shot["web_height"] = im.size
    json.dump(entry, open(f, "w"), indent=2, ensure_ascii=False)
    print("rethumbed", site)
