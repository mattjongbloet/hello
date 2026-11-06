"""Image helpers for capture.js.

  img.py size  <png>                                -> "W H"
  img.py thumb <png> <out.jpg> <width>              -> resized JPEG, prints "W H"
  img.py stitch <out.png> <width> <total_h> <frame.png:offset> ...
"""
import sys
from PIL import Image

Image.MAX_IMAGE_PIXELS = None


def size(p):
    with Image.open(p) as im:
        print(*im.size)


def thumb(src, out, width):
    width = int(width)
    with Image.open(src) as im:
        im = im.convert("RGB")
        if im.width > width:
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        im.save(out, "JPEG", quality=80, optimize=True, progressive=True)
        print(*im.size)


def stitch(out, width, total, frames):
    width, total = int(width), int(total)
    parts = []
    for f in frames:
        p, off = f.rsplit(":", 1)
        parts.append((p, int(off)))
    last_p, last_off = parts[-1]
    with Image.open(last_p) as im:
        total = min(total, last_off + im.height)
    canvas = Image.new("RGB", (width, total), "white")
    # Paste in order; later frames overwrite the overlap, so each region comes from the frame that scrolled to it.
    for p, off in parts:
        with Image.open(p) as im:
            canvas.paste(im.convert("RGB"), (0, off))
    canvas.save(out, optimize=False)


def compare(full, frame, offset):
    """Fraction of pixels that differ noticeably between a viewport shot and the same region of the full-page shot."""
    offset = int(offset)
    with Image.open(full) as a, Image.open(frame) as b:
        crop = a.convert("L").crop((0, offset, b.width, offset + b.height))
        small = (max(1, b.width // 4), max(1, b.height // 4))
        x, y = crop.resize(small), b.convert("L").resize(small)
        px, py_ = x.load(), y.load()
        bad = sum(1 for i in range(small[0]) for j in range(small[1]) if abs(px[i, j] - py_[i, j]) > 40)
        print(round(bad / (small[0] * small[1]), 4))


if __name__ == "__main__":
    cmd, *a = sys.argv[1:]
    {"size": lambda: size(*a), "thumb": lambda: thumb(*a), "stitch": lambda: stitch(a[0], a[1], a[2], a[3:]), "compare": lambda: compare(*a)}[cmd]()
