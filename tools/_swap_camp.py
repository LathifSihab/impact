"""Put the real IMPACT Camp photography from the deck into the card slots."""
import pathlib, re
SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

def pic(name, ratio, alt, sizes, cls=""):
    base = f"assets/img/camp/{name}-{ratio}"
    ws = [420, 720, 1080]
    def ss(ext):
        import os
        avail = [w for w in ws if (SITE / f"{base}-{w}.{ext}").exists()]
        return ", ".join(f"{base}-{w}.{ext} {w}w" for w in avail)
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source type="image/avif" srcset="{ss("avif")}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{ss("webp")}" sizes="{sizes}">'
            f'<img src="{base}.jpg" alt="{alt}" loading="lazy"{c}></picture>')

CARD = "(max-width: 820px) 92vw, 400px"
WIDE = "(max-width: 820px) 100vw, 640px"

# --- event page: the 2026 gallery becomes actual Basketball Edition photography ---
p = SITE / "event.html"; t = p.read_text(encoding="utf8")
gal = ('    <div class="gallery">\n      '
       + pic("court", "169", "Basketball Edition 2026 op het veld", WIDE) + "\n      "
       + pic("socks", "45", "Deelnemer tijdens Basketball Edition 2026", CARD) + "\n      "
       + pic("drinks", "45", "Gezonde lunches en tussendoortjes op het camp", CARD) + "\n    </div>")
t = re.sub(r'    <div class="gallery">.*?</div>', gal, t, count=1, flags=re.S)
p.write_text(t, encoding="utf8")

# --- journal: real camp images on the cards ---
p = SITE / "journal.html"; t = p.read_text(encoding="utf8")
swaps = [
    ("past-event", "group",  "Het IMPACT Camp in het veld"),
    ("story",      "court",  "Deelnemers op het basketbalveld"),
    ("insight",    "grass",  "Verbinding tijdens een activatie"),
    ("social",     "socks",  "Detail van een deelnemer"),
]
for cat, name, alt in swaps:
    t = re.sub(r'(<article class="jcard" data-cat="%s">)<picture>.*?</picture>' % cat,
               lambda m, n=name, a=alt: m.group(1) + pic(n, "32", a, CARD), t, count=1, flags=re.S)
    t = re.sub(r'(<article class="jcard" data-cat="%s">)<img[^>]*>' % cat,
               lambda m, n=name, a=alt: m.group(1) + pic(n, "32", a, CARD), t, count=1, flags=re.S)
# the featured recap
t = re.sub(r'(<article class="feature" data-cat="past-event">)\s*<picture>.*?</picture>',
           lambda m: m.group(1) + "\n      " + pic("court", "32", "Recap Basketball Edition 2026", WIDE),
           t, count=1, flags=re.S)
p.write_text(t, encoding="utf8")

# --- media: the archive shows the camp, not only the brochure shoot ---
p = SITE / "media.html"; t = p.read_text(encoding="utf8")
grid = ("    <div class=\"photo-grid\">\n      "
        + "\n      ".join(pic(n, "45", a, CARD) for n, a in [
            ("court", "Basketball Edition 2026"),
            ("group", "Het camp in het veld"),
            ("socks", "Deelnemer in beweging"),
            ("grass", "Verbinding op het gras"),
            ("drinks", "Gezonde tussendoortjes"),
            ("boots", "Onderweg in het veld")])
        + "\n    </div>")
t = re.sub(r'    <div class="photo-grid">.*?</div>', grid, t, count=1, flags=re.S)
p.write_text(t, encoding="utf8")
print("camp photography wired into event, journal and media")
