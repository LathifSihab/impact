"""Generate the English site from the Dutch one.

The ten pages stay hand-written in Dutch; English is generated, so there is one
set of pages to keep in structural sync rather than twenty. Translations live in
`i18n/en.json`, keyed by the exact Dutch string, which means the client can edit
English copy without touching markup — and when she supplies her own Dutch copy,
the extractor lists exactly which English strings went stale.

    python tools/i18n.py --extract    refresh i18n/en.json with any new strings
    python tools/i18n.py              write site/en/*.html

Text nodes are translated, plus the attributes that are read aloud or shown:
alt, title, aria-label, placeholder, content (meta description).
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = SITE / "en"
STORE = ROOT / "i18n/en.json"

TRANSLATABLE_ATTRS = ("alt", "title", "aria-label", "placeholder")
SKIP_TAGS = ("script", "style")

# strings that carry no language: brand marks, numerals, punctuation
SKIP_RE = re.compile(r"^[\s\d.,:;·—–\-/|@€%+×✓\[\]()]*$")


def segments(html: str):
    """Yield (kind, text) where kind is 'tag' or 'text', skipping script/style."""
    pos = 0
    skip_until = None
    for m in re.finditer(r"<[^>]+>", html):
        if m.start() > pos:
            text = html[pos:m.start()]
            yield ("skip" if skip_until else "text", text)
        tag = m.group(0)
        name = re.match(r"</?\s*([a-zA-Z0-9]+)", tag)
        name = name.group(1).lower() if name else ""
        if skip_until and name == skip_until and tag.startswith("</"):
            skip_until = None
        elif not skip_until and name in SKIP_TAGS and not tag.startswith("</"):
            skip_until = name
        yield ("tag", tag)
        pos = m.end()
    if pos < len(html):
        yield ("text", html[pos:])


def collect(html: str) -> set:
    found = set()
    for kind, chunk in segments(html):
        if kind == "text":
            s = chunk.strip()
            if s and not SKIP_RE.match(s):
                found.add(s)
        elif kind == "tag":
            for attr in TRANSLATABLE_ATTRS:
                for m in re.finditer(r'%s="([^"]+)"' % attr, chunk):
                    v = m.group(1).strip()
                    if v and not SKIP_RE.match(v):
                        found.add(v)
    return found


def body_of(html: str) -> str:
    """Only the page's own content — the shared chrome is translated by inject.py."""
    if "<!--/NAV-->" in html and "<!--FOOTER-->" in html:
        return html[html.index("<!--/NAV-->"):html.index("<!--FOOTER-->")]
    return html


def extract():
    store = json.loads(STORE.read_text(encoding="utf8")) if STORE.exists() else {}
    before = len(store)
    for f in sorted(SITE.glob("*.html")):
        html = f.read_text(encoding="utf8")
        for s in collect(body_of(html)):
            store.setdefault(s, "")
        # the SEO block is per page and needs its own English
        m = re.search(r"<!--SEO-->(.*?)<!--/SEO-->", html, re.S)
        if m:
            for attr in ("<title>(.*?)</title>", r'name="description" content="([^"]+)"'):
                for x in re.findall(attr, m.group(1)):
                    store.setdefault(x.strip(), "")
    STORE.parent.mkdir(exist_ok=True)
    STORE.write_text(json.dumps(store, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
                     encoding="utf8")
    missing = [k for k, v in store.items() if not v]
    print(f"  strings: {len(store)} ({len(store) - before} new), untranslated: {len(missing)}")
    return store


def translate_html(html: str, store: dict) -> str:
    out = []
    for kind, chunk in segments(html):
        if kind == "text":
            s = chunk.strip()
            if s and s in store and store[s]:
                out.append(chunk.replace(s, store[s], 1))
                continue
            out.append(chunk)
        elif kind == "tag":
            for attr in TRANSLATABLE_ATTRS:
                def sub(m, attr=attr):
                    v = m.group(1).strip()
                    return '%s="%s"' % (attr, store.get(v) or v)
                chunk = re.sub(r'%s="([^"]+)"' % attr, sub, chunk)
            out.append(chunk)
        else:
            out.append(chunk)
    return "".join(out)


def localise_links(html: str) -> str:
    """EN pages sit one level down, so assets go root-absolute and page links
    stay inside /en/."""
    html = re.sub(r'(href|src|poster)="assets/', r'\1="/assets/', html)
    html = re.sub(r'srcset="([^"]*)"',
                  lambda m: 'srcset="%s"' % m.group(1).replace("assets/", "/assets/"), html)
    html = re.sub(r'(href)="([a-z0-9-]+\.html)([^"]*)"', r'\1="/en/\2\3"', html)
    return html


def localise_head(html: str, name: str) -> str:
    """An English page must be canonical to itself, or the two locales compete."""
    slug = "" if name == "index.html" else name
    nl_url = "https://www.wemakeimpact.be/" + slug
    en_url = "https://www.wemakeimpact.be/en/" + slug
    html = html.replace('<link rel="canonical" href="%s">' % nl_url,
                        '<link rel="canonical" href="%s">' % en_url)
    html = html.replace('<meta property="og:url" content="%s">' % nl_url,
                        '<meta property="og:url" content="%s">' % en_url)
    html = html.replace('<meta property="og:locale" content="nl_BE">',
                        '<meta property="og:locale" content="en">')
    return html


def localise_switch(html: str, name: str) -> str:
    """Flip the language switch: EN is the active one on an English page."""
    slug = "" if name == "index.html" else name
    return html.replace(
        '<a href="/%s" class="lang is-active" hreflang="nl">NL</a>' % slug,
        '<a href="/%s" class="lang" hreflang="nl">NL</a>' % slug
    ).replace(
        '<a href="/en/%s" class="lang" hreflang="en">EN</a>' % slug,
        '<a href="/en/%s" class="lang is-active" hreflang="en">EN</a>' % slug)


def build():
    if not STORE.exists():
        print("  no i18n/en.json — run with --extract first")
        return
    store = {k: v for k, v in json.loads(STORE.read_text(encoding="utf8")).items() if v}
    OUT.mkdir(exist_ok=True)
    for f in sorted(SITE.glob("*.html")):
        html = f.read_text(encoding="utf8")
        en = translate_html(html, store)      # body and chrome alike
        en = translate_html_head(en, store)
        en = en.replace('<html lang="nl">', '<html lang="en">')
        en = localise_head(en, f.name)
        en = localise_links(en)
        en = localise_switch(en, f.name)
        (OUT / f.name).write_text(en, encoding="utf8")
    print(f"  wrote {len(list(OUT.glob('*.html')))} English pages to site/en/")


def translate_html_head(html: str, store: dict) -> str:
    """Title and description live in the managed SEO block."""
    def one(m):
        block = m.group(0)
        for pattern in (r"<title>(.*?)</title>", r'name="description" content="([^"]+)"'):
            for src in re.findall(pattern, block):
                if src.strip() in store:
                    block = block.replace(src, store[src.strip()])
        return block
    return re.sub(r"<!--SEO-->.*?<!--/SEO-->", one, html, flags=re.S)


if __name__ == "__main__":
    if "--extract" in sys.argv:
        extract()
    else:
        build()
