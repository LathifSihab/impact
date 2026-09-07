# Open items blocking the next phase

Status 7 September 2026. The 10 September craft pass is done and on staging. Everything below
blocks a *later* milestone. Owner column: **C** = client (IMPACT), **D** = DRP BuildLab.

## Hard blockers — nothing moves without these

| # | Item | Owner | Blocks | If it is late |
|---|---|---|---|---|
| 1 | **Mollie account in the company name, KYC started** | C | 24 Sep (sellable), 30 Sep (launch) | Days of lead time outside anyone's control. Late KYC = no ticket sales in September. This is the single biggest risk. |
| 2 | **The 1–2 September events**: title, format, dates, location, age range, price, capacity | C | 17 Sep (CMS), 24 Sep, 30 Sep | Nothing to sell. The whole "live by end of September" goal disappears. |
| 3 | **Domain + DNS access for wemakeimpact.be**, and confirmation the new site takes the apex | C | 30 Sep (launch) | Cannot cut over. Also blocks the Wix 301 map, which must be pulled *before* the subscription lapses. |
| 4 | **Wix account access** (to export the existing URL list) | C | 30 Sep (SEO carry-over) | Existing ranking is lost at cutover. Time-limited: once Wix lapses the URLs are gone. |
| 5 | **NL copy per block** | C | 17 Sep | The structure is built to receive it. Without copy the site ships with structure and no voice — the exact failure we just corrected. |
| 6 | **Privacy policy + algemene voorwaarden** | C (lawyer/accountant) | 17 Sep | Legally required *before* the waitlist and newsletter collect real data. Currently the footer links are removed because there is no text. GDPR, not a nice-to-have. |

## Content blockers — the site works without them, but reads unfinished

| # | Item | Owner | Blocks | If it is late |
|---|---|---|---|---|
| 7 | Photo library as a drive folder | C | 17 Sep | Everything on the demo is cropped out of the brochure PDF. One grade across the site is impossible until we see the library. |
| 8 | **Landscape 16:9** banner video / aftermovie master | C | 17 Sep | Four clips arrived but they are 480x848 portrait phone recordings. They are now used as participant testimonials, which is what they are; a full-bleed landscape header still needs a 16:9 master. The wiring is built — drop the file in and it upgrades itself. |
| 8b | **Parental consent for the minors speaking on camera**, plus transcripts for captions | C | Before launch | Without consent the feedback section comes out. Without transcripts the videos fail WCAG 1.2.2. |
| 9 | Logo + beeldmerk as SVG; partner logos as SVG | C | 17 Sep | Currently rasters lifted off the live site. Visibly soft on retina, and the logo cannot be recoloured. |
| 10 | Brand font files | C | Post-launch swap is fine | Archivo Black is the agreed substitute. Two-line swap whenever the real font arrives. |
| 11 | Expert portraits (Julie, TaPas, Olivier) | C | 17 Sep | The expert grid is text-only until then. |
| 12 | FAQ answers + the Basketball Edition 2027 day programme | C | 24 Sep | The event page has the structure with honest "volgt bij bevestiging" lines. |
| 13 | Journal launch articles (3–4, reworked from the social content in the deck) | C | 30 Sep | Journal renders as non-clickable cards. |

## Decisions — one-line answers, but they change what we build

| # | Question | Owner | Blocks | Our recommendation |
|---|---|---|---|---|
| 14 | Are the deck figures (30 / 11 / 4 / 1.500+ / 200+ / 600+) current, or 2026-camp-only? | C | Now (live on staging) | Keep the "na Basketball Edition 2026" caption so they age honestly. |
| 15 | May we name Julie Dingemans, TaPas City Crew and Olivier Goetgeluck publicly? | C | Now (live on staging) | Yes, with portraits. |
| 16 | Partnership prices open or gated? | C | Now (live on staging) | **Open.** Builds trust with professional parties and filters inbound. |
| 17 | Confirm hero line "BUILDING FOUNDATIONS FOR LIFE." | C | Now (live on staging) | Confirm — it is the deck's own closing line. |
| 18 | Confirm age band 14–18 | C | Now (live on staging) | Confirm — deck, ecosystem brief and brochure all say 14–18. |
| 19 | Testimonials: which parents can we quote, under what attribution, consent on file? | C | 17 Sep | If consent is not in hand by 15 Sep, the section stays out. Do not chase. |
| 20 | Which accounting system, and who owns the login? | C | 24 Sep | Do not custom-build until we know. Nightly CSV export as the interim. |
| 21 | Brevo account owner + existing subscriber list | C | 17 Sep | Create under the company account, not a personal one. |
| 22 | EN in September, yes or no? | C/D | 24 Sep | **No.** October, when her EN copy exists. |
| 23 | Webshop in September? Is there a product catalogue? | C | 30 Sep | **Only if a catalogue exists.** Ticketing is the flow that matters for launch. |
| 24 | Consent for photography of minors in the library | C | 17 Sep | Needed before any participant photo is published. |

## What DRP does regardless

- `noindex` on the staging domain until cutover (canonicals currently point at
  wemakeimpact.be — staging must not be indexed).
- Astro migration and Payload models, which need no client input.
- Plausible install, goals and UTM plumbing.
- Rehearse the full waitlist → "registration opened" flow on a dummy event before handover.

---

# The message to send

Dutch, ready to copy-paste. Deliberately short: the full list above gets ignored, five things
with a date gets answered.

---

**Onderwerp: IMPACT website — wat we deze week van jou nodig hebben**

Dag Mirte,

De nieuwe versie staat online op staging — je kan alles al doorklikken. Het ziet er nu uit zoals
jullie deck: de juiste rood- en bordeauxtinten, jullie eigen headline-stijl, de zes fundamenten
als beeldstrip, de cijfers van Basketball Edition 2026, de partnerniveaus, en de nieuwsbrief-pop-up
zoals op de site die je doorstuurde.

Om verder te kunnen, hebben we een paar dingen van jou nodig. Ik heb ze gesorteerd op urgentie.

**Deze week — anders halen we eind september niet**

1. **Start vandaag de Mollie-aanvraag** (op naam van de vennootschap). De identiteitscontrole duurt
   enkele dagen en dat staat volledig buiten onze controle. Zonder Mollie kunnen we geen tickets
   verkopen in september.
2. **De 1 à 2 events van september**: titel, format, datum, locatie, leeftijd, prijs, aantal
   plaatsen. Zonder deze gegevens is er niets om te verkopen.
3. **Toegang tot de domeinnaam (wemakeimpact.be) en tot jullie Wix-account.** Wix hebben we nodig
   om de bestaande links te exporteren vóór het abonnement afloopt — anders verliezen jullie de
   Google-posities die er nu al zijn.
4. **Privacyverklaring en algemene voorwaarden.** Zodra de wachtlijst en de nieuwsbrief echte
   gegevens verzamelen, is dit wettelijk verplicht. Heeft jullie boekhouder of jurist hier een
   basistekst voor?

**Voor 12 september**

5. **De foto's** — liefst een Drive-map met de volledige bibliotheek. Alles wat er nu op staat,
   hebben we uit de brochure moeten halen.
6. **De bannervideo / aftermovie** in 16:9. Je zei dat je de video van de huidige site goed vindt,
   maar die staat er vandaag niet meer op — dus we hebben het originele bestand nodig.
7. **Logo en beeldmerk als SVG**, en idealiter ook de partnerlogo's.
8. **Jouw teksten.** De structuur staat klaar; jij schrijft. Als het later wordt dan 15 september,
   zetten we liever minder secties volledig af dan alle secties half.

**Even bevestigen (kort antwoord volstaat)**

9. De cijfers uit het deck (30 deelnemers, 11 via IMPACT FOR ALL, 4 sponsors, 1.500+ bezoekers,
   200+ inschrijvingen, 600+ volgers) — zijn die van vandaag, of enkel van Basketball Edition 2026?
   We hebben ze nu gelabeld als "na Basketball Edition 2026".
10. Mogen we Julie Dingemans, TaPas City Crew en Olivier Goetgeluck bij naam vermelden? En heb je
    portretten?
11. De partnerbedragen (€2.000 / €3.000 / €4.000 / €7.000): open op de site, of pas na contact?
    **Ons advies: open** — dat schept vertrouwen bij bedrijven en filtert je inbox.
12. De hero-zin is nu **"Building foundations for life"** (de slotzin uit jullie deck) in plaats van
    "for the new generation". Akkoord?
13. De middelste leeftijdsgroep staat nu op **14–18** — zo staat het in het deck, de brochure en de
    visietekst. Enkel de websitebriefing zei 15–18. Akkoord?
14. De ouderquotes uit het deck: van wie mogen we citeren, en onder welke naam? Zonder schriftelijke
    toestemming laten we die sectie voorlopig weg — liever niets dan een lege plaats.

**Twee voorstellen van onze kant**

- **Engels schuiven we op naar oktober.** Een taalknop die naar onvertaalde pagina's leidt, is
  slechter dan geen taalknop. In september focussen we op Nederlands.
- **De webshop bouwen we enkel als er een productlijst is.** Tickets verkopen is een andere flow, en
  dat is degene die eind september moet werken.

Laat je vooral weten wat er niet lukt — dan schuiven we op tijd, in plaats van op de valreep.

Groeten,
Lathif — DRP BuildLab
