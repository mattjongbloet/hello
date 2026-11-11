"""Make dark-background versions of the light-grey mockup images.

Background = every neutral (r≈g≈b) pixel brighter than the black phone bezel that connects to the image border,
including the soft drop shadow and the anti-aliased ring. The bezel stops the fill, so screen content is untouched.
python3 -I tools/darken-mockups.py
"""
import os
from collections import deque
from PIL import Image

ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "redesigns", "assets")
BG = (13, 14, 17)
JOBS = [("pmi-mockup.png", "pmi-mockup-dark.png"), ("pmi-thumb.png", "pmi-thumb-dark.png"),
        ("home-search.jpg", "home-search-dark.jpg"), ("home-value.png", "home-value-dark.png")]


def is_bg(p):
    r, g, b = p[:3]
    return max(r, g, b) - min(r, g, b) <= 10 and (r + g + b) / 3 > 34


for src, dst in JOBS:
    im = Image.open(os.path.join(ASSETS, src)).convert("RGB")
    w, h = im.size
    px = im.load()
    seen = bytearray(w * h)
    # Seed from the top and side edges only: the phones are cropped at the bottom edge, so seeding there
    # would let the fill run up into the screens.
    q = deque((x, 0) for x in range(w))
    q.extend((x, y) for y in range(h) for x in (0, w - 1))
    filled = 0
    while q:
        x, y = q.popleft()
        i = y * w + x
        if seen[i]:
            continue
        seen[i] = 1
        if not is_bg(px[x, y]):
            continue
        # Anti-aliased ring: darker neutral pixels keep their relative darkness against the new ground.
        v = sum(px[x, y]) / 3
        k = max(0.0, min(1.0, (v - 34) / (225 - 34)))  # 1 = pure background, 0 = bezel
        px[x, y] = tuple(round(BG[c] * k + 8 * (1 - k)) for c in range(3))
        filled += 1
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx]:
                q.append((nx, ny))
    out = os.path.join(ASSETS, dst)
    im.save(out, quality=90) if dst.endswith(".jpg") else im.save(out)
    print(f"{dst}: {filled / (w * h):.0%} of pixels were background")
