"""Lay a tall screenshot out as side-by-side vertical slices so a whole page fits in one view.
python3 tools/strip.py in.png out.png [slice_height] [scale]"""
import sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
src, out = sys.argv[1], sys.argv[2]
sh = int(sys.argv[3]) if len(sys.argv) > 3 else 1800
sc = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
im = Image.open(src).convert("RGB")
n = max(1, -(-(im.height - 2) // sh))
w, h = round(im.width * sc), round(sh * sc)
c = Image.new("RGB", (n * (w + 12), h), "#777")
for i in range(n):
    part = im.crop((0, i * sh, im.width, min(im.height, (i + 1) * sh)))
    part = part.resize((w, round(part.height * sc)))
    c.paste(part, (i * (w + 12), 0))
c.save(out)
print(n, c.size)
