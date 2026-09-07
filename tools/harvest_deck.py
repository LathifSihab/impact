"""Harvest the text-free photo regions from the branddeck slides into site assets.

The deck slides are composites, so each region is a hand-picked box in original
slide pixels (slides are 1919x1035). Heroes stay on the higher-res brochure crops;
these fill the cards, galleries and the media archive with real IMPACT Camp
photography instead of brochure lifestyle shots.
"""
import pathlib
from PIL import Image, ImageEnhance

ROOT = pathlib.Path(__file__).resolve().parent.parent
DECK = ROOT / "brief/deck"
OUT = ROOT / "site/assets/img/camp"
OUT.mkdir(parents=True, exist_ok=True)

REGIONS = {
    "court":  ("impact10", (148, 215, 868, 945)),   # basketball court, Basketball Edition 2026
    "socks":  ("impact16", (787, 118, 1294, 885)),  # participant detail
    "drinks": ("impact16", (1315, 110, 1858, 880)), # in-house lunches
    "group":  ("impact1",  (20, 90, 760, 950)),     # the camp group in the field
    "grass":  ("impact17", (143, 82, 916, 620)),    # hands in the grass
    "boots":  ("impact18", (34, 90, 560, 940)),     # red boots in the field
}

RATIOS = {"32": (3, 2), "45": (4, 5), "169": (16, 9)}

# the slide grounds — any edge row/column that is mostly one of these is slide,
# not photograph, so it gets trimmed off before we crop to ratio
GROUNDS = [(0x56, 0x02, 0x16), (0x0F, 0x10, 0x15), (0xFF, 0xFF, 0xFF), (0xF4, 0xF2, 0xEB),
           (0xCA, 0x00, 0x13)]


def is_ground(px, tol=42):
    return any(abs(px[0] - g[0]) < tol and abs(px[1] - g[1]) < tol and abs(px[2] - g[2]) < tol
               for g in GROUNDS)


def autotrim(im, max_trim=0.12, share=0.80):
    """Shave edge lines that are mostly slide background."""
    w, h = im.size
    px = im.load()
    left, right, top, bottom = 0, w, 0, h
    for _ in range(int(w * max_trim)):
        if sum(is_ground(px[left, y]) for y in range(0, h, 4)) > share * len(range(0, h, 4)):
            left += 1
        else:
            break
    for _ in range(int(w * max_trim)):
        if sum(is_ground(px[right - 1, y]) for y in range(0, h, 4)) > share * len(range(0, h, 4)):
            right -= 1
        else:
            break
    for _ in range(int(h * max_trim)):
        if sum(is_ground(px[x, top]) for x in range(left, right, 4)) > share * len(range(left, right, 4)):
            top += 1
        else:
            break
    for _ in range(int(h * max_trim)):
        if sum(is_ground(px[x, bottom - 1]) for x in range(left, right, 4)) > share * len(range(left, right, 4)):
            bottom -= 1
        else:
            break
    return im.crop((left, top, right, bottom))


def crop_ratio(im, rw, rh, yfocus=0.4):
    w, h = im.size
    tr, cr = rw / rh, w / h
    if cr > tr:
        nw = int(h * tr)
        return im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    nh = int(w / tr)
    y = int((h - nh) * yfocus)
    return im.crop((0, y, w, y + nh))


for name, (slide, box) in REGIONS.items():
    src = Image.open(DECK / (slide + ".png")).convert("RGB").crop(box)
    src = autotrim(src)
    src = ImageEnhance.Color(src).enhance(0.94)          # one grade across the site
    for tag, (rw, rh) in RATIOS.items():
        c = crop_ratio(src, rw, rh)
        if c.width < 320:
            continue
        for w in (420, 720, 1080):
            if w > c.width * 1.25:
                continue
            r = c.resize((w, round(c.height * w / c.width)), Image.LANCZOS)
            r.save(OUT / f"{name}-{tag}-{w}.webp", quality=76, method=5)
            r.save(OUT / f"{name}-{tag}-{w}.avif", quality=48)
        base = c.resize((min(1080, c.width), round(c.height * min(1080, c.width) / c.width)), Image.LANCZOS)
        base.save(OUT / f"{name}-{tag}.jpg", quality=84, optimize=True, progressive=True)
        print(f"  {name}-{tag}: {base.size}")
