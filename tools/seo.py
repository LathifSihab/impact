"""Writes the SEO head block into every page in site/, plus sitemap.xml and robots.txt.

One place to edit titles, descriptions and structured data. Run after editing:
    python tools/seo.py

Each page gets, between <!--SEO--> / <!--/SEO--> markers:
  canonical, hreflang (nl default + en placeholder), Open Graph, Twitter card,
  and JSON-LD (Organization + WebSite on the homepage, Event on an event page,
  BreadcrumbList elsewhere).

SITE_URL must be the production domain before launch — Netlify preview URLs in a
canonical tag will keep the real domain out of the index.
"""
import json
import pathlib
import re

SITE_URL = "https://www.wemakeimpact.be"          # ← switch to the live domain at launch
SITE_NAME = "IMPACT"
LOCALE = "nl_BE"
OG_IMAGE = "/assets/img/court-169.jpg"            # ← replace with a 1200x630 share image

ORG = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "IMPACT",
    "alternateName": "IMPACT Collective Antwerp",
    "url": SITE_URL + "/",
    "logo": SITE_URL + "/assets/brand/impact-logo.png",
    "description": "Youth development brand voor jongeren van 8 tot 25 jaar. "
                   "Camps, Days, Retreats, Community en Hosted Experiences rond zes fundamenten.",
    "email": "hello@wemakeimpact.be",
    "telephone": "+32495370044",
    "areaServed": "BE",
    "address": {"@type": "PostalAddress", "addressCountry": "BE", "addressLocality": "Antwerpen"},
    "sameAs": ["https://www.instagram.com/impact___collective/"],
    "founder": [
        {"@type": "Person", "name": "Mirte Rens"},
        {"@type": "Person", "name": "Jean-Marc Mwema"},
    ],
}

WEBSITE = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": SITE_NAME,
    "url": SITE_URL + "/",
    "inLanguage": ["nl-BE", "en"],
}

# page: (title, description, priority, changefreq, extra JSON-LD)
EVENT_LD = {
    "@context": "https://schema.org",
    "@type": "Event",
    "name": "IMPACT Camp — Basketball Edition 2027",
    "description": "Vijfdaagse experience waarin basketbal het medium is en ontwikkeling het doel.",
    "eventStatus": "https://schema.org/EventScheduled",
    "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
    "startDate": "2027-07",
    "location": {"@type": "Place", "name": "Antwerpen",
                 "address": {"@type": "PostalAddress", "addressLocality": "Antwerpen",
                             "addressCountry": "BE"}},
    "organizer": {"@type": "Organization", "name": "IMPACT", "url": SITE_URL + "/"},
    "typicalAgeRange": "8-14",
    "image": SITE_URL + "/assets/img/court-169.jpg",
    "offers": {"@type": "Offer", "availability": "https://schema.org/PreOrder",
               "url": SITE_URL + "/event.html#wachtlijst",
               "description": "Wachtlijst open — prijs volgt bij bevestiging"},
}

PAGES = {
    "index.html": (
        "IMPACT — Building foundations for life",
        "Youth development voor jongeren van 8 tot 25 jaar. Camps, Days, Retreats, Community en "
        "Hosted Experiences, opgebouwd rond zes fundamenten. Bekijk de upcoming events.",
        "1.0", "weekly", [ORG, WEBSITE]),
    "over.html": (
        "Over IMPACT — founders, fundamenten, team & experts",
        "Waarom IMPACT bestaat, wie de founders zijn, de zes fundamenten achter elke activatie, "
        "voor welke leeftijdsgroepen we bouwen en welke experts onze programma's dragen.",
        "0.9", "monthly", None),
    "events.html": (
        "Events — upcoming IMPACT events, Camps, Days & Retreats",
        "Alle upcoming IMPACT events en de formats waarin we werken: Camps, Days, Retreats, "
        "Community en Hosted Experiences. Schrijf je in op de wachtlijst.",
        "1.0", "weekly", None),
    "event.html": (
        "IMPACT Camp — Basketball Edition 2027 | Wachtlijst open",
        "Vijfdaagse IMPACT Camp in Antwerpen, juli 2027, voor 8–14 jaar. Basketbal is het medium, "
        "ontwikkeling het doel. Zet je gratis op de wachtlijst.",
        "0.9", "weekly", [EVENT_LD]),
    "hosted-experiences.html": (
        "Hosted Experiences — IMPACT bouwt, jij host",
        "Days en Camps in co-creatie met een club, school, organisatie of bedrijf. Jij hebt de "
        "community en de locatie, IMPACT brengt methodiek, experts en experience-design.",
        "0.8", "monthly", None),
    "samenwerken.html": (
        "Samenwerken met IMPACT — partners, bedrijven, experts & hosts",
        "Partner worden, een Hosted Experience bouwen, als expert meebouwen of als bedrijf "
        "bijdragen aan IMPACT FOR ALL. Vijf manieren om mee te bouwen aan sterkere fundamenten.",
        "0.9", "monthly", None),
    "social-impact.html": (
        "IMPACT FOR ALL — Talent is everywhere. Opportunity isn't.",
        "Het sociale programma van IMPACT: via partnerships, sponsoring en bijdragen geven we "
        "jongeren een plaats voor wie die kansen minder vanzelfsprekend zijn.",
        "0.8", "monthly", None),
    "journal.html": (
        "Journal — recaps, verhalen en insights van IMPACT",
        "Het levende archief van IMPACT: recaps van afgelopen events, verhalen van deelnemers, "
        "insights rond onze fundamenten, partnerverhalen en nieuws.",
        "0.7", "weekly", None),
    "media.html": (
        "Media & press — foto, video, aftermovies & downloads",
        "Fotografie, aftermovies, persinformatie en downloads van IMPACT. Voor journalisten, "
        "partners en hosts.",
        "0.5", "monthly", None),
    "contact.html": (
        "Contact — IMPACT",
        "Ouders, jongeren, scholen, clubs, bedrijven, experts en pers: contacteer IMPACT "
        "rechtstreeks. Antwoord doorgaans binnen twee werkdagen.",
        "0.6", "yearly", None),
}


def head_for(name, title, desc, extra_ld):
    url = SITE_URL + "/" + ("" if name == "index.html" else name)
    ld = [json.dumps(x, ensure_ascii=False, separators=(",", ":")) for x in (extra_ld or [])]
    if not extra_ld:
        ld = [json.dumps({
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"},
                {"@type": "ListItem", "position": 2, "name": title.split(" — ")[0], "item": url},
            ]}, ensure_ascii=False, separators=(",", ":"))]
    scripts = "\n".join('<script type="application/ld+json">%s</script>' % x for x in ld)
    return f"""
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="nl-BE" href="{url}">
<link rel="alternate" hreflang="en" href="{SITE_URL}/en/{'' if name == 'index.html' else name}">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:locale" content="{LOCALE}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}{OG_IMAGE}">
<meta property="og:image:alt" content="Jongeren in actie tijdens een IMPACT-activatie">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE_URL}{OG_IMAGE}">
<meta name="robots" content="index,follow,max-image-preview:large">
{scripts}
"""


def run():
    site = pathlib.Path(__file__).resolve().parent.parent / "site"
    for name, (title, desc, _prio, _freq, extra) in PAGES.items():
        f = site / name
        html = f.read_text(encoding="utf8")
        block = "<!--SEO-->" + head_for(name, title, desc, extra) + "<!--/SEO-->"
        if "<!--SEO-->" in html:
            html = re.sub(r"<!--SEO-->.*?<!--/SEO-->", lambda _m: block, html, flags=re.S)
        else:
            # replace the hand-written title + description with the managed block
            html = re.sub(r"<title>.*?</title>\s*<meta name=\"description\"[^>]*>", block, html,
                          count=1, flags=re.S)
        f.write_text(html, encoding="utf8")
        print("seo:", name)

    def entry(path, prio, freq, slug):
        """Each URL declares both locales, so search engines pair them themselves."""
        return (f"  <url><loc>{SITE_URL}{path}</loc>"
                f"<changefreq>{freq}</changefreq><priority>{prio}</priority>"
                f'<xhtml:link rel="alternate" hreflang="nl-BE" href="{SITE_URL}/{slug}"/>'
                f'<xhtml:link rel="alternate" hreflang="en" href="{SITE_URL}/en/{slug}"/>'
                "</url>")

    rows = []
    for n, (_t, _d, prio, freq, _e) in PAGES.items():
        slug = "" if n == "index.html" else n
        rows.append(entry("/" + slug, prio, freq, slug))
        rows.append(entry("/en/" + slug, prio, freq, slug))
    urls = "\n".join(rows)
    (site / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"'
        ' xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + "\n</urlset>\n",
        encoding="utf8")
    (site / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n"
        f"Sitemap: {SITE_URL}/sitemap.xml\n", encoding="utf8")
    print("wrote sitemap.xml + robots.txt")


if __name__ == "__main__":
    run()
