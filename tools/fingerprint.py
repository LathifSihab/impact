"""Stamp the CSS and JS references with a content hash.

    python tools/fingerprint.py        rewrites site/*.html in place

Why this exists. netlify.toml caches /assets/* hard, because that is right for
photography and video. But style.css and main.js are not fingerprinted, so a
returning visitor kept the old copy for the whole cache window — which meant
pushing a fix and being told the bug was still there, because it was, in that
browser. After launch the same thing applies to real visitors: a CSS correction
would take a week to reach anyone who had already visited.

The fix is the standard one: the URL changes when the bytes change. Then the
cache can be as long as we like and still never serve a stale file, because HTML
revalidates on every request and carries the new query string with it.

Run order matters — this rewrites the Dutch pages, so i18n.py has to run after
it for the English pages to inherit the same stamps:

    python tools/inject.py && python tools/seo.py \
      && python tools/fingerprint.py && python tools/i18n.py
"""
import hashlib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

# only the files that change often enough to matter; images and video keep their
# own (shorter) cache window in netlify.toml instead
TARGETS = [
    "assets/css/style.css",
    "assets/js/main.js",
    "assets/js/consent.js",
    "assets/js/cinema.js",
    "assets/js/preloader.js",
]


def short_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()[:10]


def run():
    stamps = {}
    for rel in TARGETS:
        f = SITE / rel
        if not f.exists():
            print("  missing, skipped:", rel)
            continue
        stamps[rel] = short_hash(f)

    if not stamps:
        return 1

    changed = 0
    for page in sorted(SITE.glob("*.html")):
        html = page.read_text(encoding="utf8")
        before = html
        for rel, h in stamps.items():
            # match the path with or without a leading slash and with or without
            # an existing stamp, so the tool is safe to run repeatedly
            pattern = re.compile(r'(["\'])(/?' + re.escape(rel) + r')(\?v=[0-9a-f]+)?\1')
            html = pattern.sub(lambda m: '%s%s?v=%s%s' % (m.group(1), m.group(2), h, m.group(1)),
                               html)
        if html != before:
            page.write_text(html, encoding="utf8")
            changed += 1

    for rel, h in stamps.items():
        print("  %-28s v=%s" % (rel, h))
    print("  stamped %d page(s)" % changed)
    return 0


if __name__ == "__main__":
    sys.exit(run())
