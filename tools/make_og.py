"""Build the 1200x630 share card.

    python tools/make_og.py

Regenerate it whenever the photography or the brand font changes — a share card
is the one image that gets seen by people who never reach the site.

Two things it is deliberately not doing. It does not typeset the wordmark: it
composites `impact-logo.png`, so no font licence is involved and the mark is
exactly the mark. And the headline currently falls back to Arial Bold, because
Archivo Black is a substitute we do not hold a licence for either — swap
HEADLINE_FONT the day the real display face is bought, and rerun.
"""
import pathlib

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

W, H = 1200, 630                       # the ratio every platform crops toward
INK = (15, 16, 21)
RED = (202, 0, 19)

SOURCE = "assets/img/court-169.jpg"
OUT = "assets/img/og-default.jpg"
HEADLINE = "BUILDING FOUNDATIONS FOR LIFE."
STANDFIRST = "Youth development · 8–25 · Antwerpen"
HEADLINE_FONT = "C:/Windows/Fonts/arialbd.ttf"
STANDFIRST_FONT = "C:/Windows/Fonts/segoeuib.ttf"


def build():
    src = Image.open(SITE / SOURCE).convert("RGB")
    scale = max(W / src.width, H / src.height)
    img = src.resize((round(src.width * scale), round(src.height * scale)), Image.LANCZOS)
    left = (img.width - W) // 2
    top = int((img.height - H) * 0.42)          # keep the subject, lose the sky
    img = img.crop((left, top, left + W, top + H))

    # a share card competes with a busy feed: calm the picture and give the type
    # somewhere to sit rather than letting the two fight
    img = ImageEnhance.Color(img).enhance(0.88)
    scrim = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(scrim)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=int(30 + 200 * ((y / H) ** 1.7)))
    img = Image.composite(Image.new("RGB", (W, H), INK), img, scrim)

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dl = ImageDraw.Draw(layer)

    logo = Image.open(SITE / "assets/brand/impact-logo.png").convert("RGBA")
    lw = 300
    logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    layer.alpha_composite(logo, (72, H - 72 - logo.height - 96))

    dl.text((72, H - 134), HEADLINE, font=ImageFont.truetype(HEADLINE_FONT, 46),
            fill=(255, 255, 255, 255))
    dl.text((72, H - 74), STANDFIRST, font=ImageFont.truetype(STANDFIRST_FONT, 21),
            fill=(255, 255, 255, 190))
    dl.rectangle([(0, H - 8), (W, H)], fill=RED + (255,))

    out = SITE / OUT
    Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB").save(
        out, quality=88, optimize=True, progressive=True)
    print("  %s  %dx%d  %.0f KB" % (OUT, W, H, out.stat().st_size / 1024))


if __name__ == "__main__":
    build()
