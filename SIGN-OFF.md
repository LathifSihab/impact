# Sign-off list — content published on staging that IMPACT has not confirmed

Per `brief/docs/02-CONTENT-UNLOCKED.md`: *"nothing in here gets published without the client
confirming it."* The craft pass publishes it on the **staging URL only** so she reviews real
content instead of empty slots. Every item below needs a yes/no before the site goes to the
live domain.

## Figures — `social-impact.html` and `samenwerken.html`

Taken from branddeck slide 10, captioned "na IMPACT Camp: Basketball Edition 2026".

| Figure | Label | Where |
|---|---|---|
| 30 | Participants | social-impact |
| 11 | IMPACT FOR ALL | social-impact |
| 4 | Sponsors | social-impact |
| 1.500+ | Website visitors | samenwerken |
| 200+ | Newsletter sign-ups | samenwerken |
| 600+ | Instagram followers | samenwerken |

**Question:** are these current as of September 2026, or 2026-camp-only? The caption says the
latter. If they are current, the caption changes and the block moves forward in time cleanly.

## Named experts — `over.html` and `event.html`

- **Julie Dingemans** — Second Sense. Zelfkennis, veerkracht, vertrouwen. Patronen en BMIT.
- **TaPas City Crew** — Talent & passie.
- **Olivier Goetgeluck** — Movement, performance & body awareness.

**Questions:** may we name them publicly, are the descriptions right, and can we have portraits?
The grid is built for a variable count, so a fourth or fifth expert drops in without a rebuild.

## Partnership pricing — `samenwerken.html`

Support €2.000+ · Community €3.000+ · Growth €4.000+ · Legacy €7.000+, with the six benefit
rows from deck slide 15, cumulative.

**Question:** publish the prices openly (built, and what we recommend — it filters inbound and
builds trust with professional parties), or gate them behind a contact form?

## Hero line — every page

Switched to the deck's own closing line: **BUILDING FOUNDATIONS FOR LIFE.** The previous line
was BUILDING FOUNDATIONS FOR THE NEW GENERATION.

**Question:** confirm, or revert.

## Age band — site-wide

Changed from 15–18 to **14–18**, which is what the branddeck (slide 6), the ecosystem brief and
the brochure all say. Only the website brief said 15–18.

**Question:** confirm 14–18.

## Participant videos — needs an explicit yes before launch

Four clips arrived from IMPACT: portrait phone recordings from Basketball Edition 2026,
mostly **participants (minors) speaking on camera**. They are now on staging: three as the
homepage feedback section, four on the media page, one in the event gallery. Staging carries
`noindex`, so nothing is indexable yet.

Before the site goes to the live domain we need, in writing:

1. **Parental consent for each identifiable minor on camera**, for publication on a public
   website. This is stricter than photo consent and it is the one item that can stop the
   launch. If consent covers only some clips, name which ones and we publish only those.
2. **Whether faces may stay unblurred** and whether first names may be used in captions.
   Right now every caption reads "Deelnemer · Basketball Edition 2026" — no names.
3. **Captions or transcripts.** The clips carry speech, so without captions they fail
   WCAG 1.2.2 and are unusable for deaf visitors and in silent autoplay contexts. A plain
   text transcript per clip is enough; we generate the caption files from it.

If consent is not in hand, the section comes out again — it is one block to remove.

## Removed rather than faked

- **Written testimonials.** The deck has real parent messages, but they are private-message
  attributions and consent is unknown, so no written quotes are published. Send the quotes you
  have written consent for, with the attribution you want ("Ouder · Basketball Edition 2026",
  or a first name), and they slot in alongside the video.
- **LinkedIn and TikTok links.** No URLs supplied — the icons were dead links, so only
  Instagram is linked for now.
- **Privacy policy and algemene voorwaarden.** No copy exists, so the footer links were
  removed rather than pointing nowhere. Both are legally required before launch, and a privacy
  policy is required before the waitlist and newsletter forms collect real data.
- **EN language switch.** Cut for this milestone per `00-INDEX.md` decision 4 — a switcher
  leading to untranslated pages is worse than no switcher. The `hreflang` scaffolding stays.
- **Journal article links.** No articles exist yet, so the cards are not links. They become
  links the moment the CMS has posts.

## Still needed from the client, unchanged

Brand font files · logo and beeldmerk as SVG · partner logos as SVG · **the landscape 16:9
banner video and the Basketball Edition 2026 aftermovie** (the four clips received are 480x848
portrait phone recordings — good for the feedback section, not usable as a full-bleed landscape
header) · the photo library as a drive folder · the 1–2 September events with
dates, price and capacity · FAQ answers · the Basketball Edition 2027 day programme · which
accounting system · Mollie KYC started.
