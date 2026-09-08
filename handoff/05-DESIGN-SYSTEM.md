# Design system

The complete system is in `assets/css/style.css` — one file, tokens at the top.
The CMS should look like it belongs to this, not like a default admin template.
That is most of what makes a backoffice demo convincing to a client.

---

## Tokens

```css
/* Colour — sampled from the branddeck, not reconstructed from the brochure */
--white:#FFFFFF;
--bone:#F4F2EB;          /* alternating light ground */
--bone-card:#FAF9F4;     /* callouts, waitlist card */
--ink:#0F1015;           /* type, dark ground, footer */
--red:#CA0013;           /* CTAs, conviction ground, display type on light */
--red-dark:#9E000F;      /* primary hover */
--burgundy:#560216;      /* retrospective / proof ground */
--burgundy-card:#631628; /* stat cards, one step lighter than the ground */
--grey-warm:#8D877D; --grey-body:#6B665E; --grey-muted:#A09A90;
--border:#E7E4DB; --border-sand:#DAD5CA; --placeholder:#E2DDD4;

/* Type — display and text split so the brand-font swap is two lines */
--font-display:'Archivo Black','Arial Black',system-ui,sans-serif;
--font-text:'Figtree',system-ui,-apple-system,'Segoe UI',sans-serif;

--t-hero:clamp(32px,10vw,124px);
--t-display:clamp(30px,7vw,96px);
--t-head:clamp(20px,2.4vw,30px);
--t-body:16px;  --t-meta:12px;  --t-rule:10px;

--margin:72px; --pad:120px; --maxw:1296px;
--dur-fast:150ms; --dur-reveal:800ms; --ease:ease-out;
```

**Archivo Black is a substitute.** The real brand font had not been supplied. The
display/text split exists so swapping it is two lines.

## The look, in words

Editorial and high-contrast. Big display type in near-black or red on bone,
generous whitespace, full-bleed photography, thin rules and small uppercase
labels in brackets — `[ Praktisch ]`, `[ Camps ]`. Red is used sparingly and
always means action or emphasis; it is never decoration.

Sections alternate ground: white, bone, ink, burgundy. Buttons are pills —
`.pill--primary` is red on white text, `.pill--secondary` is outlined.

## Components worth copying

| Class | What it is |
|---|---|
| `.wrap` | Page container, `max-width:1296px`, side gutters |
| `.section`, `.section--sand`, `.section--black` | Alternating grounds |
| `.pill`, `.pill--primary`, `.pill--secondary`, `.pill--sm` | Buttons |
| `.tag`, `.tag--dim` | Small uppercase category labels |
| `.field`, `.field--check`, `.err` | Form row, checkbox row, inline error |
| `.event-row` | The events list row — the closest existing thing to a CMS list item |
| `.meta`, `.body`, `.running`, `.d-l` | Type roles |

`.field` and `.err` already carry the validation styling, including the Dutch
inline error pattern. Reuse them for CMS forms and it will look native.

## Behaviour already built

- **Sticky nav** — spacious at top, compacts past 50px scroll
- **Preloader** — kinetic wordmark, 1.88s, once per session
- **Cookie consent** — bottom banner, Necessary / Statistics / Marketing, opt-in
  and unticked by default, equal-weight buttons. `window.impactConsent.whenGranted(cat, fn)`
- **Reveal on scroll** — `data-reveal`
- **Cinema reel** — scroll-driven video, autoplaying muted, one at a time

`assets/js/` has each of these as a small standalone file. They are plain ES5-ish
browser JS with no build step and no dependencies.

## Responsive

The live site was audited at **20 pages × 15 widths, 320px to 1920px**: no
horizontal overflow, no clipped content, no sliced words, no labels that do not
fit. The gutter shrinks from 72px to 18px on small screens.

If the CMS is desktop-first that is defensible — a backoffice is used at a desk.
But the client will open it on a phone during the demo, so make the list views
survive 390px at least.

## Language

The site is **Dutch-first**; English is generated from `reference/i18n-en.json`,
keyed by the exact Dutch string. The CMS interface should be Dutch, or bilingual.
Content itself needs both languages per record — the `locale` field on `events`
and `journal` exists for that, though the current implementation is one file per
locale rather than paired translations. **If you improve one thing in the data
model, make it a proper translation pairing.**

Error messages the site already uses, worth matching:

```
Vul een geldig e-mailadres in.
Vul de voornaam van de deelnemer in.
Vul een leeftijd in.
Bevestig dit om je in te schrijven.
Deze editie is voor 8–14 jaar.
```
