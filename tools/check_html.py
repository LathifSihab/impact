"""Structural check over every page in site/ (and the generated site/en/).

Written after a lost `<div class="expert-slots">` opening tag went unnoticed on
two pages: its orphaned `</div>` closed the page's own column wrapper instead,
which threw the FAQ section into the event page's sidebar column and dropped the
waitlist card to the bottom of the document. Nothing errored, nothing looked
wrong in the markup, and the browser silently reflowed around it.

    python tools/check_html.py        exits non-zero if anything is off

Checks:
  - balanced open/close counts for the container elements that carry layout
  - every referenced local asset exists on disk
  - no page links to a .html file that is missing
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

# elements whose imbalance silently changes layout rather than failing loudly
CONTAINERS = ("div", "section", "figure", "aside", "article", "main", "header",
              "footer", "ul", "ol", "li", "form", "picture", "table")

VOID = re.compile(r"<(?:img|br|hr|input|source|meta|link|col|track|wbr)[\s>/]", re.I)


def tag_balance(html, name):
    problems = []
    for tag in CONTAINERS:
        opens = len(re.findall(r"<%s[\s>]" % tag, html, re.I))
        closes = len(re.findall(r"</%s\s*>" % tag, html, re.I))
        if opens != closes:
            problems.append("%s: <%s> %d open vs %d close (%+d)"
                            % (name, tag, opens, closes, opens - closes))
    return problems


def assets(html, page):
    problems = []
    base = page.parent
    for m in re.finditer(r'(?:href|src|poster)="([^"]+)"', html):
        # drop the cache-busting query and any fragment before resolving
        ref = m.group(1).split('#')[0].split('?')[0]
        if not ref:
            continue
        if ref.startswith(("http", "mailto:", "tel:", "data:", "//")):
            continue
        target = (SITE / ref.lstrip("/")) if ref.startswith("/") else (base / ref)
        if not target.exists():
            problems.append("%s: missing %s" % (page.name, ref))
    return problems


def main():
    problems = []
    pages = sorted(SITE.glob("*.html")) + sorted((SITE / "en").glob("*.html"))
    for page in pages:
        html = page.read_text(encoding="utf8")
        label = str(page.relative_to(SITE))
        problems += tag_balance(html, label)
        problems += assets(html, page)

    print("checked %d pages" % len(pages))
    if problems:
        for p in problems:
            print("  FAIL", p)
        print("%d problem(s)" % len(problems))
        return 1
    print("  all balanced, every local reference resolves")
    return 0


if __name__ == "__main__":
    sys.exit(main())
