"""Catch Dutch that is pretending to be English in i18n/en.json.

    python tools/check_i18n.py        exits non-zero if anything looks untranslated

`i18n.py --extract` seeds every new string with an empty value, and an empty
value is obvious. The failure mode that is not obvious is an entry whose English
value is identical to its Dutch key — sometimes correct ("Instagram", "IMPACT",
"[Events]") and sometimes a string that was simply never translated and now sits
on the English site in Dutch. "[bedrijven]" shipped that way, under a heading
that had been translated around it, which is exactly why it went unnoticed.

So: for entries where value == key, look for words that only occur in Dutch. The
list is deliberately free of words English shares — no "we", no "over", no
"mail" — because a false positive here trains people to ignore the check.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from i18n import segments, TRANSLATABLE_ATTRS, SKIP_RE   # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
STORE = ROOT / "i18n/en.json"
REVIEWED = ROOT / "i18n/identical-reviewed.txt"
EN = ROOT / "site/en"

# Dutch-only markers. Anything ambiguous between the two languages is left out
# on purpose; missing a string is recoverable, crying wolf is not.
DUTCH = """
 de het een en van voor met je jij jouw wij onze ons niet zijn worden wordt werd
 naar door uit bij tot dat die deze dit er hun zich ook nog maar als dan wat
 welke waar wie hoe waarom omdat zodat terwijl tijdens tussen zonder tegen
 bekijken wachten hoort krijgen sturen willen kunnen moeten mogen
 bedrijven bedrijf jongeren deelnemer deelnemers ouder ouders wachtlijst gegevens
 inschrijven inschrijving nieuwsbrief samenwerken samenwerking fundamenten leeftijd
 jaar dagen dag meerdaags doorlopend traject trajecten sociaal programma verhaal
 verhalen bekijk ontdek elke iedere geen altijd nooit vandaag straks volgt
 bevestiging bevestigd editie edities plaatsen vragen vraag antwoord sturen ontvang
 krijg zet schrijf laat bouw bouwen samen mee zelf zijn haar hen ik mijn u uw
"""
WORDS = set(DUTCH.split())

# strings that are identical in both languages on purpose
ALLOW = {
    'IMPACT', 'Instagram', 'Journal', 'Media', 'Contact', 'Community', 'Events',
    'NL', 'EN',          # the language switch labels; "en" is also Dutch for "and"
}


def looks_dutch(text):
    tokens = re.findall(r"[A-Za-zÀ-ÿ']+", text.lower())
    if not tokens:
        return False
    hits = sum(1 for t in tokens if t in WORDS)
    # one Dutch word carries a short label; longer copy needs corroboration
    return hits >= (1 if len(tokens) <= 3 else 2)


def scan_pages():
    """The map can be perfect and the page still wrong.

    A string only gets translated if it was extracted, and extraction only sees
    text nodes and a fixed list of attributes inside the body slice. Anything
    outside that — an attribute nobody listed, copy written by JavaScript — is
    invisible to the map and shows up in Dutch on an English page anyway. That is
    how the tier table shipped with data-label="Investering" while its own row
    heading said "Investment". So read the generated pages instead, which cannot
    lie about what a visitor sees.
    """
    problems = []
    for page in sorted(EN.glob("*.html")):
        seen = set()
        for kind, chunk in segments(page.read_text(encoding="utf8")):
            found = []
            if kind == "text":
                t = chunk.strip()
                if t and not SKIP_RE.match(t):
                    found.append(t)
            elif kind == "tag":
                for attr in TRANSLATABLE_ATTRS:
                    for m in re.finditer(r'%s="([^"]+)"' % attr, chunk):
                        found.append(m.group(1).strip())
            for text in found:
                if text in seen or text in ALLOW or not looks_dutch(text):
                    continue
                seen.add(text)
                problems.append("%s: %s" % (page.name, repr(text[:74])))
    return problems


def main():
    store = json.loads(STORE.read_text(encoding="utf8"))
    empty = [k for k, v in store.items() if not v]

    # A word list can only catch the Dutch it knows, and it did not know
    # "Voordeel". So the rule is stricter than a heuristic: every identical pair
    # must appear in the reviewed list, which is a record of someone having
    # actually looked at it.
    reviewed = set()
    if REVIEWED.exists():
        for line in REVIEWED.read_text(encoding="utf8").splitlines():
            if line and not line.startswith("#"):
                reviewed.add(line)
    same = [k for k, v in store.items() if v == k and k not in reviewed]

    print("i18n: %d strings" % len(store))
    for k in sorted(empty):
        print("  EMPTY        ", repr(k[:80]))
    for k in sorted(same):
        print("  IDENTICAL, UNREVIEWED", repr(k[:70]))
    if same:
        print("      -> translate each, or add the line to i18n/identical-reviewed.txt")

    onpage = scan_pages()
    for line in onpage:
        print("  DUTCH ON /en/", line)

    total = len(empty) + len(same) + len(onpage)
    if total:
        print("%d untranslated" % total)
        return 1
    print("  map clean, and no Dutch found on any English page")
    return 0


if __name__ == "__main__":
    sys.exit(main())
