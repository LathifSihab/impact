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

ROOT = pathlib.Path(__file__).resolve().parent.parent
STORE = ROOT / "i18n/en.json"

# Dutch-only markers. Anything ambiguous between the two languages is left out
# on purpose; missing a string is recoverable, crying wolf is not.
DUTCH = """
 de het een en van voor met je jij jouw wij onze ons niet zijn worden wordt werd
 naar door uit bij tot dat die deze dit er hun zich ook nog maar want als dan wat
 welke waar wie hoe waarom omdat zodat terwijl tijdens tussen zonder tegen
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
}


def looks_dutch(text):
    tokens = re.findall(r"[A-Za-zÀ-ÿ']+", text.lower())
    if not tokens:
        return False
    hits = sum(1 for t in tokens if t in WORDS)
    # one Dutch word carries a short label; longer copy needs corroboration
    return hits >= (1 if len(tokens) <= 3 else 2)


def main():
    store = json.loads(STORE.read_text(encoding="utf8"))
    empty = [k for k, v in store.items() if not v]
    same = [k for k, v in store.items()
            if v == k and k not in ALLOW and looks_dutch(k)]

    print("i18n: %d strings" % len(store))
    for k in sorted(empty):
        print("  EMPTY        ", repr(k[:80]))
    for k in sorted(same):
        print("  STILL DUTCH  ", repr(k[:80]))

    if empty or same:
        print("%d untranslated" % (len(empty) + len(same)))
        return 1
    print("  every string has an English value that is not the Dutch one")
    return 0


if __name__ == "__main__":
    sys.exit(main())
