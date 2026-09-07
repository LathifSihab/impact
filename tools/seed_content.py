"""Seed the Astro content collections from the approved static site + branddeck.

These files are the interim source of truth. When Payload goes live the loaders in
`web/src/content.config.ts` point at its REST API instead and the shapes stay identical,
so no component changes.
"""
import json
import pathlib

C = pathlib.Path(__file__).resolve().parent.parent / "web/src/content"
(C / "events").mkdir(parents=True, exist_ok=True)
(C / "journal").mkdir(parents=True, exist_ok=True)


def write(name, data):
    (C / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf8")
    print("  ", name, len(data) if isinstance(data, list) else "")


write("formats.json", [
    {"id": "days", "name": "Days", "bracketName": "[Days]", "order": 1, "meta": "Één dag",
     "description": "Korte, krachtige experiences waarin de fundamenten zelf het vertrekpunt zijn.",
     "body": "Korte, krachtige en toegankelijke experiences waarmee jongeren op een laagdrempelige manier kennismaken met de visie en de fundamenten van IMPACT: van workshops en schooldagen tot talks, community events en hosted experiences.",
     "image": "assets/img/field-169.jpg",
     "ticks": ["Eén dag, op onze locatie of bij jou",
               "Of een langer traject met verschillende contactmomenten",
               "Modulair: één workshop tot een volledig programma",
               "Voornamelijk 14–18 jaar en schoolgroepen"]},
    {"id": "camps", "name": "Camps", "bracketName": "[Camps]", "order": 2, "meta": "Meerdaags",
     "description": "Meerdaagse, intensieve experiences rond één centraal medium.",
     "body": "Meerdaagse experiences waarin jongeren via één centraal medium intensiever werken rond teamwork, discipline, mindset en beweging. Het medium creëert de context; de fundamenten bepalen de inhoud.",
     "image": "assets/img/camp/court-169.jpg",
     "ticks": ["Meerdaags, met overnachting", "Vaste experts en coaches per fundament",
               "Voornamelijk 8–14 en 14–18 jaar", "Aftermovie en recap achteraf in Journal"]},
    {"id": "retreats", "name": "Retreats", "bracketName": "[Retreats]", "order": 3, "meta": "Traject",
     "description": "Trajecten met focus op student-ondernemers.",
     "body": "Begeleide trajecten voor student-zelfstandigen en jonge ondernemers rond ondernemerschap, persoonlijk leiderschap en purpose. Kleiner in groep, langer in tijd.",
     "image": "assets/img/mountain-169.jpg",
     "ticks": ["Traject in plaats van eenmalige activatie", "18–25 jaar",
               "Focus op ownership, richting en netwerk", "Beperkt aantal plaatsen per editie"]},
    {"id": "community", "name": "Community", "bracketName": "[Community]", "order": 4, "meta": "Doorlopend",
     "description": "Online en offline verbonden blijven met coaches, experts en elkaar.",
     "body": "Community is voor ons meer dan een lijst mensen die onze nieuwsbrief ontvangen. Het is de omgeving waarin jongeren op een toegankelijke manier verbonden blijven — ook tussen twee activaties.",
     "image": "assets/img/hands-169.jpg",
     "ticks": ["Contact met elkaar, coaches, experts en inspirerende mensen",
               "Kennis, ervaringen en opportuniteiten", "Online en offline, doorlopend",
               "Op termijn het verbindende element tussen alle formats"]},
    {"id": "hosted", "name": "Hosted Experiences", "bracketName": "[Hosted]", "order": 5,
     "meta": "Maatwerk", "isHosted": True,
     "description": "Days en Camps, samen met een externe club, organisatie of host georganiseerd.",
     "body": "Days en Camps die we samen met een externe club, organisatie of host bouwen. Zij hosten, IMPACT bouwt de ervaring.",
     "image": "assets/img/house-169.jpg", "ticks": []},
])

write("foundations.json", [
    {"id": "self-knowledge", "number": "01", "name": "Self-knowledge",
     "enOneLiner": "Understanding who you are, how you work and what you need.",
     "nlBody": "Zelfkennis is voor ons één van de belangrijkste fundamenten voor persoonlijke groei. Hoe beter jongeren zichzelf begrijpen, hoe sterker ze leren omgaan met keuzes, emoties, energie, druk en uitdagingen.",
     "workOn": ["Hoe ze reageren onder druk", "Wat hen energie geeft of net leegmaakt",
                "Hoe hun lichaam en mindset samen werken", "Wat hun sterktes, valkuilen en noden zijn",
                "Beter leren luisteren naar zichzelf"],
     "image": "assets/img/portrait-45.jpg", "alt": "Jongere in gesprek"},
    {"id": "healthy-habits", "number": "02", "name": "Healthy habits & lifestyle",
     "enOneLiner": "Sleep, movement, nutrition, recovery and energy.",
     "nlBody": "De manier waarop jongeren slapen, eten, bewegen en herstellen heeft een enorme impact op hoe ze zich voelen, functioneren en presteren.",
     "workOn": ["Beweging en lichaamsbewustzijn", "Gezonde voeding", "Slaap en herstel",
                "Routines en structuur", "Energiemanagement en duurzame gewoontes"],
     "image": "assets/img/running-45.jpg", "alt": "Beweging en warming-up"},
    {"id": "resilience", "number": "03", "name": "Resilience",
     "enOneLiner": "Handling pressure, setbacks and uncertainty with strength and awareness.",
     "nlBody": "Opgroeien brengt druk, onzekerheid en uitdagingen met zich mee. Het doel is jongeren leren hoe ze zichzelf kunnen dragen in moeilijke momenten.",
     "workOn": ["Omgaan met druk en verwachtingen", "Emotionele weerbaarheid", "Vertrouwen opbouwen",
                "Leren omgaan met falen en tegenslag", "Flexibiliteit en aanpassingsvermogen"],
     "image": "assets/img/cartwheel-45.jpg", "alt": "Moment van inspanning"},
    {"id": "ownership", "number": "04", "name": "Ownership",
     "enOneLiner": "Taking responsibility for your growth, choices and direction.",
     "nlBody": "Verantwoordelijkheid leren nemen voor jezelf, je keuzes, je energie en je groei vanuit bewustzijn en zelfstandigheid. We helpen jongeren beseffen dat groei niet iets is dat iemand anders voor hen doet.",
     "workOn": ["Initiatief nemen", "Verantwoordelijkheid dragen", "Discipline opbouwen",
                "Bewust keuzes leren maken", "Zelfstandig leren denken"],
     "image": "assets/img/mountain-45.jpg", "alt": "Jongere neemt initiatief"},
    {"id": "human-connection", "number": "05", "name": "Human connection",
     "enOneLiner": "Communicating, trusting and growing with others.",
     "nlBody": "Mensen groeien niet alleen. In een wereld die steeds digitaler en individueler wordt, geloven wij sterk in de kracht van echte menselijke verbinding.",
     "workOn": ["Leren communiceren", "Samenwerken en verbinden", "Vertrouwen opbouwen",
                "Zich gezien voelen en anderen zien", "Offline connectie ervaren"],
     "image": "assets/img/hands-45.jpg", "alt": "Groep, echte interactie"},
    {"id": "talent-passion", "number": "06", "name": "Talent & passion",
     "enOneLiner": "Discovering what energizes you and what you want to build.",
     "nlBody": "We creëren ruimte om talenten, interesses en passies te ontdekken — zonder de druk om al te weten wie je bent. Wanneer jongeren dichter komen bij wat hen écht energie geeft, ontstaat vanzelf meer richting en zelfvertrouwen.",
     "workOn": ["Waar ze energie van krijgen", "Wat hen motiveert", "Waar hun talenten liggen",
                "Wat hen nieuwsgierig maakt", "Wat ze verder willen ontwikkelen"],
     "image": "assets/img/field-45.jpg", "alt": "Talent in actie"},
])

write("age-groups.json", [
    {"id": "8-14", "label": "8–14", "tagline": "De fundering",
     "body": "Focus op de fundering van zelfvertrouwen, beweging, sociale verbinding, plezier en bewustwording. Jongeren leren zichzelf beter kennen via sport, ervaring en begeleiding in een veilige en motiverende omgeving.",
     "formats": ["Camps", "Days"], "image": "assets/img/beach-jump-45.jpg", "alt": "Kind in het spel"},
    {"id": "14-18", "label": "14–18", "tagline": "Mindset & identiteit",
     "body": "Focus op mindset, identiteit, weerbaarheid, ambitie, gezonde gewoontes en persoonlijke verantwoordelijkheid. We helpen jongeren beter omgaan met druk, sociale verwachtingen en ambitie.",
     "formats": ["Days", "Scholen"], "image": "assets/img/pair-45.jpg", "alt": "Tiener, portret"},
    {"id": "18-25", "label": "18–25", "tagline": "Ownership & richting",
     "body": "Focus op ownership, ondernemerschap, leiderschap en het omzetten van talenten en passies in iets tastbaars. IMPACT reikt jongvolwassenen de tools aan om richting te vinden en initiatief te nemen.",
     "formats": ["Retreats", "Community"], "image": "assets/img/path-45.jpg", "alt": "Jongvolwassene onderweg"},
])

write("experts.json", [
    {"id": "julie-dingemans", "name": "Julie Dingemans", "org": "Second Sense",
     "bio": "Ontwikkeling van zelfkennis, veerkracht en vertrouwen. Expertise in patronen en BMIT.",
     "foundations": ["01", "03"], "confirmed": False},
    {"id": "tapas-city-crew", "name": "TaPas City Crew", "org": "Talent & passie",
     "bio": "Begeleidt jongeren in het ontdekken van hun kwaliteiten.",
     "foundations": ["06"], "confirmed": False},
    {"id": "olivier-goetgeluck", "name": "Olivier Goetgeluck",
     "org": "Movement, performance & body awareness",
     "bio": "Lichaamsbewustzijn, ademhaling en bewegingsvaardigheden.",
     "foundations": ["02"], "confirmed": False},
])

write("tiers.json", [
    {"id": "support", "name": "Support", "investmentFrom": "€2.000+", "order": 1,
     "benefits": ["Vermelding op website", "Impactrapport"]},
    {"id": "community", "name": "Community", "investmentFrom": "€3.000+", "order": 2,
     "benefits": ["Vermelding op website", "Impactrapport", "Bedrijfsmateriaal in goodiebag"]},
    {"id": "growth", "name": "Growth", "investmentFrom": "€4.000+", "order": 3,
     "benefits": ["Vermelding op website", "Impactrapport", "Bedrijfsmateriaal in goodiebag",
                  "Storytelling & contentmogelijkheden"]},
    {"id": "legacy", "name": "Legacy", "investmentFrom": "€7.000+", "order": 4,
     "benefits": ["Vermelding op website", "Impactrapport", "Bedrijfsmateriaal in goodiebag",
                  "Storytelling & contentmogelijkheden", "Selectie professionele foto's",
                  "Mogelijkheid collab partnership"]},
])

PERIOD = "na IMPACT Camp: Basketball Edition 2026"
write("figures.json", [
    {"id": "participants", "value": 30, "display": "30", "label": "Participants", "group": "forAll",
     "explanation": "jongeren namen deel aan onze eerste IMPACT Camp", "period": PERIOD, "confirmed": False},
    {"id": "for-all", "value": 11, "display": "11", "label": "IMPACT FOR ALL", "group": "forAll",
     "explanation": "jongeren namen deel via onze jeugdwerking, dankzij gesponsorde tickets",
     "period": PERIOD, "confirmed": False},
    {"id": "sponsors", "value": 4, "display": "4", "label": "Sponsors", "group": "forAll",
     "explanation": "bedrijven en ondernemers maakten die deelname mee mogelijk", "period": PERIOD,
     "confirmed": False},
    {"id": "visitors", "value": 1500, "display": "1.500", "suffix": "+", "label": "Website visitors",
     "group": "reach", "period": PERIOD, "confirmed": False},
    {"id": "signups", "value": 200, "display": "200", "suffix": "+", "label": "Newsletter sign-ups",
     "group": "reach", "period": PERIOD, "confirmed": False},
    {"id": "followers", "value": 600, "display": "600", "suffix": "+", "label": "Instagram followers",
     "group": "reach", "period": PERIOD, "confirmed": False},
])

PARTNERS = [("Talenco Group", "talenco", "https://talenco.be/"),
            ("SNM Event Agency", "snm", "https://saynomore.events/"),
            ("ODTH First Class Logistics", "odth", "https://www.odth.be/en/homepage/"),
            ("Les Plumes", "les-plumes", "https://lesplumes.be/"),
            ("Foodmaker", "foodmaker", "https://www.foodmaker.be/"),
            ("Boshi", "boshi", "https://www.boshi.be/"),
            ("Decathlon", "decathlon", "https://www.decathlon.be/nl"),
            ("Één Pot Nat", "eenpotnat", "https://www.eenpotnat.be/"),
            ("Flourish by Magnolia", "flourish", "https://flourishbymagnolia.com/")]
write("partners.json", [{"id": s, "name": n, "logo": "assets/brand/partners/%s.png" % s, "url": u}
                        for n, s, u in PARTNERS])

# nothing renders until consent is on file (doc 02 §3)
write("testimonials.json", [])

# --- events -------------------------------------------------------------
EVENTS = [
    {"slug": "camp-basketball-edition-2027",
     "title": "IMPACT Camp — Basketball Edition 2027", "format": "camps", "editionYear": 2027,
     "dateText": "Juli 2027", "location": "Antwerpen", "ageMin": 8, "ageMax": 14,
     "price": "Volgt bij bevestiging", "status": "waitlist",
     "standfirst": "Basketbal is het medium. Ontwikkeling is de missie. Een vijfdaagse experience waarin we de IMPACT-fundamenten tot leven brengen via basketbal.",
     "intro": "Het medium creëert een context waarin jongeren samenkomen, plezier maken en zichzelf kunnen ontwikkelen. Tegelijk gebruiken we die omgeving om onze bredere IMPACT-fundamenten tot leven te brengen. Naast basketbal integreren we bewust sessies rond movement, mentale skills, relaxatie, communicatie, verbinding en gezonde gewoontes.",
     "heroImage": "assets/img/court-169.jpg",
     "gallery": [{"src": "assets/img/camp/court-169.jpg", "alt": "Basketball Edition 2026 op het veld"},
                 {"src": "assets/img/camp/socks-45.jpg", "alt": "Deelnemer tijdens Basketball Edition 2026"},
                 {"src": "assets/img/camp/drinks-45.jpg", "alt": "Gezonde lunches en tussendoortjes"}],
     "programmeDays": [
         {"day": "Dag 01", "title": "Aankomst & kennismaking", "body": "Het volledige dagschema volgt bij de bevestiging van deze editie."},
         {"day": "Dag 02", "title": "Fundamenten in beweging", "body": "Het volledige dagschema volgt bij de bevestiging van deze editie."},
         {"day": "Dag 03", "title": "Mentale skills & herstel", "body": "Het volledige dagschema volgt bij de bevestiging van deze editie."},
         {"day": "Dag 04", "title": "Teamwork & verbinding", "body": "Het volledige dagschema volgt bij de bevestiging van deze editie."},
         {"day": "Dag 05", "title": "Showcase & afsluiting", "body": "Het volledige dagschema volgt bij de bevestiging van deze editie."}],
     "foundations": ["self-knowledge", "healthy-habits", "resilience", "ownership", "human-connection", "talent-passion"],
     "experts": ["julie-dingemans", "tapas-city-crew", "olivier-goetgeluck"],
     "faq": [{"q": "Moet mijn kind al basketbal spelen?", "a": "Antwoord volgt bij de bevestiging van deze editie."},
             {"q": "Wat is er inbegrepen in de prijs?", "a": "Antwoord volgt bij de bevestiging van deze editie."},
             {"q": "Waar en hoe verloopt het vervoer?", "a": "Antwoord volgt bij de bevestiging van deze editie."},
             {"q": "Wat als de editie niet doorgaat?", "a": "Antwoord volgt bij de bevestiging van deze editie."},
             {"q": "Kan mijn kind deelnemen via IMPACT FOR ALL?", "a": "Antwoord volgt bij de bevestiging van deze editie."}],
     "practical": [{"k": "Format", "v": "Camp · 5 dagen"}, {"k": "Leeftijd", "v": "8–14 jaar"},
                   {"k": "Locatie", "v": "Antwerpen"}, {"k": "Taal", "v": "Nederlands"},
                   {"k": "Status", "v": "Wachtlijst open"}],
     "seo": {"title": "IMPACT Camp — Basketball Edition 2027 | Wachtlijst open",
             "description": "Vijfdaagse IMPACT Camp in Antwerpen, juli 2027, voor 8–14 jaar. Basketbal is het medium, ontwikkeling het doel. Zet je gratis op de wachtlijst."}},
    {"slug": "day-brussels-2027", "title": "IMPACT Day — Brussels", "format": "days", "editionYear": 2027,
     "dateText": "Augustus 2027", "location": "Brussel", "ageMin": 14, "ageMax": 18,
     "status": "waitlist",
     "standfirst": "Eén dag waarin de fundamenten zelf het vertrekpunt zijn.",
     "intro": "Een korte, krachtige experience waarin jongeren kennismaken met de visie en de fundamenten van IMPACT.",
     "heroImage": "assets/img/field-169.jpg",
     "seo": {"title": "IMPACT Day — Brussels | Wachtlijst open",
             "description": "Eendaagse IMPACT Day in Brussel, augustus 2027, voor 14–18 jaar. Zet je gratis op de wachtlijst."}},
    {"slug": "retreat-student-entrepreneurs", "title": "IMPACT Retreat — Student Entrepreneurs",
     "format": "retreats", "editionYear": 2027, "dateText": "Datum volgt", "location": "Locatie volgt",
     "ageMin": 18, "ageMax": 25, "status": "waitlist",
     "standfirst": "Een begeleid traject rond ondernemerschap, persoonlijk leiderschap en purpose.",
     "intro": "Voor student-zelfstandigen en jonge ondernemers. Kleiner in groep, langer in tijd.",
     "heroImage": "assets/img/mountain-169.jpg",
     "seo": {"title": "IMPACT Retreat — Student Entrepreneurs",
             "description": "Begeleid traject voor student-zelfstandigen rond ondernemerschap, persoonlijk leiderschap en purpose. 18–25 jaar."}},
    {"slug": "camp-basketball-edition-2026", "title": "IMPACT Camp — Basketball Edition 2026",
     "format": "camps", "editionYear": 2026, "dateText": "Juli 2026", "location": "Antwerpen",
     "ageMin": 8, "ageMax": 14, "status": "past",
     "standfirst": "Onze eerste editie. Basketbal was het medium, ontwikkeling was de missie.",
     "intro": "Dertig jongeren, vijf dagen, zes fundamenten. Elf deelnemers namen deel via IMPACT FOR ALL.",
     "heroImage": "assets/img/camp/court-169.jpg",
     "gallery": [{"src": "assets/img/camp/group-32.jpg", "alt": "Het camp in het veld"},
                 {"src": "assets/img/camp/grass-32.jpg", "alt": "Verbinding op het gras"}],
     "seo": {"title": "This was IMPACT Camp: Basketball Edition 2026",
             "description": "De recap van onze eerste IMPACT Camp: dertig jongeren, vijf dagen, zes fundamenten."}},
]
for e in EVENTS:
    slug = e.pop("slug")
    (C / "events" / (slug + ".json")).write_text(
        json.dumps(e, indent=2, ensure_ascii=False) + "\n", encoding="utf8")
print("   events:", len(EVENTS))

JOURNAL = [
    ("this-was-basketball-edition-2026", "past-event", "This was IMPACT Camp: Basketball Edition 2026",
     "assets/img/camp/court-32.jpg", "Recap Basketball Edition 2026", "Recap · aftermovie", "2026-07-20",
     "camp-basketball-edition-2026"),
    ("het-verhaal-van-een-deelnemer", "story", "Het verhaal van een deelnemer",
     "assets/img/camp/group-32.jpg", "Het camp in het veld", "Interview", "2026-08-05", None),
    ("waarom-resilience-een-fundament-is", "insight", "Waarom resilience één van onze fundamenten is",
     "assets/img/camp/grass-32.jpg", "Verbinding tijdens een activatie", "Expert content · fundament 03",
     "2026-08-19", None),
    ("wat-er-gebeurt-na-een-activatie", "social", "Wat er gebeurt na een IMPACT-activatie",
     "assets/img/camp/socks-32.jpg", "Detail van een deelnemer", "IMPACT FOR ALL", "2026-08-28", None),
]
for slug, cat, title, image, alt, meta, date, rel in JOURNAL:
    fm = ["---", 'category: "%s"' % cat, 'title: "%s"' % title, 'image: "%s"' % image,
          'alt: "%s"' % alt, 'meta: "%s"' % meta, "publishedAt: %s" % date]
    if rel:
        fm.append('relatedEvent: "%s"' % rel)
    fm.append("---")
    body = "\nDe volledige tekst van dit artikel wordt door IMPACT aangeleverd.\n"
    (C / "journal" / (slug + ".md")).write_text("\n".join(fm) + "\n" + body, encoding="utf8")
print("   journal:", len(JOURNAL))
