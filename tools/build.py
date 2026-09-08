"""One entry point for the whole static pipeline, in the order it has to run.

    python tools/build.py

The order is not arbitrary and getting it wrong fails quietly:

  1. inject     — shared chrome into the Dutch pages
  2. seo        — the managed <head> block, sitemap, robots
  3. fingerprint— stamps CSS/JS with a content hash, so a cached browser cannot
                  serve yesterday's file
  4. i18n       — generates the English pages *from* the Dutch ones, so it must
                  come last or /en/ misses whatever the earlier steps changed
  5. check      — tag balance and local references across all 20 pages

Run this rather than the individual tools. The one that bites is 3 before 4:
forget it and the English pages keep the previous hash, so /en/ silently serves
stale assets while / is fine.
"""
import pathlib
import subprocess
import sys

TOOLS = pathlib.Path(__file__).resolve().parent
STEPS = [
    ("inject", ["inject.py"]),
    ("seo", ["seo.py"]),
    ("fingerprint", ["fingerprint.py"]),
    ("i18n", ["i18n.py"]),
    ("check", ["check_html.py"]),
]


def main():
    for name, args in STEPS:
        print("\n[%s]" % name)
        r = subprocess.run([sys.executable, str(TOOLS / args[0])] + args[1:],
                           cwd=str(TOOLS.parent))
        if r.returncode != 0:
            print("\n%s failed (exit %d) — stopping." % (name, r.returncode))
            return r.returncode
    print("\nbuild ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
