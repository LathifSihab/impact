# IMPACT — static site

Static HTML/CSS/JS, no build step. Serve the folder (`python -m http.server 8080`)
rather than opening the files directly — the hero video and the webfonts behave
differently over `file://`.

**How to test it: [../TESTING.md](../TESTING.md).**

The craft pass of 7 September 2026 executed `brief/docs/` (01 art direction, 02 content,
03 components) against this site. What changed, and why, is below. Unconfirmed content that is
now live on staging is listed in `../SIGN-OFF.md`.

## Art direction (doc 01)

- **Colour corrected from the branddeck**, sampled not guessed: `--red #CA0013`,
  `--burgundy #560216` (+ `--burgundy-card #631628`), `--ink #0F1015`, `--bone #F4F2EB`.
  Burgundy is the new proof/retrospective ground; red is the conviction ground. Red-on-burgundy
  display type, as the deck does it.
- **Display face split from the text face**: `--font-display` (Archivo Black) and
  `--font-text` (Figtree). Doc 01 suggested Anton/Bebas as "compressed"; the actual deck face
  is *not* condensed, so Archivo Black is the closer substitute — flagged and agreed before
  building. Swapping in the real brand font is two lines.
- **Four display steps, violent gaps**: `--t-hero`, `--t-display`, `--t-head`, plus body and
  meta. The dense 88/60/56/52/48/44 midrange is gone.
- **No `<br>` in any heading** — 47 removed. Line count is now a property of the type block
  (`text-wrap: balance`, `ch` measures, `line-height: .86`).
- **Bracket eyebrows demoted** to one mono running header per section, top right, as in the
  deck. Heroes keep a visible label.
- **Stop list applied**: no trailing `→` on links, no middle-dot meta strings, no
  fade-and-slide-up on scroll, no autoplay on the fundamentals track.

## Components (doc 03)

- `photo-strip` — the fundamentals as a full-bleed row on red, 4:5 portraits, `[01]` chips on
  the image, prev/next controls, snap, bleeding off the right edge. No auto-advance.
- `stat-block` — 3-up cards on burgundy, tinted one step lighter, count-up once on entry, with
  a period caption so the numbers age honestly.
- `tier-table` — the four partnership tiers as a real `<table>` with `scope`, transposing to
  one card per tier on mobile from the *same markup* (rows become `display:contents`, flex
  `order` groups each tier's cells).
- `newsletter-dome` — the Capital Belgium modal the client singled out: wide bone dome rising
  from the bottom, exit-intent on desktop, 60% scroll on mobile, once per visitor, suppressed
  90 days via `localStorage`, never on the event page, Escape closes, focus trapped,
  background `inert`, no rise under reduced motion.
- `cta-card-row` — three colour-blocked closing cards (ink/red/burgundy) with the newsletter
  inline as one of them, on events, samenwerken and social-impact.
- Hero rebuilt as a locked 3–4 line block with a checkmark trust row, and the video wiring
  generalised so **every** page hero can carry one (`assets/video/<slug>.webm|.mp4`).
- `expert-grid` variable count with the three real experts; `format-row` as four peers then a
  rule then Hosted; `event-row` meta without middle dots.

## Two-column sections

`.two-col` was one 1.05fr/.95fr grid with `align-items:start` doing duty for three
different pairings, and it showed: nine of thirteen instances had columns whose heights
differed by 250–1.360px. It now has variants that match the content:

- **`.two-col--media`** — copy beside a photograph. The photo gets a real height
  (`clamp(340px, 50vh, 620px)`) and sticks at `top: 96px`, so it stays alongside a long
  column instead of floating at its own ratio with dead space under it. Capped
  deliberately: stretching a 16:9 source to a 1.100px column crops it to a vertical sliver.
  Sticky and the fixed height are dropped below 820px, where there is nothing to sit beside.
- **`.two-col--form`** — copy beside a form: narrower form column, vertically centred.
- **`.two-col--story`** — copy beside one portrait video card.
- Plain `.two-col` stays for two comparable text columns.

Two bugs fixed along the way: `fr` tracks floor at min-content, so the contact table on the
media page was squeezing the boilerplate column into a 150px ribbon (`min-width: 0` on the
children fixes the ratio), and "JOURNALISTEN" was overflowing its column into the next one
(display type now has `overflow-wrap: break-word` + `hyphens: auto`, and a smaller display
step inside a half-width column).

## Global

- Skip link, `<main>` landmark, visible `:focus-visible` on everything, `aria-expanded` +
  `inert` on the mobile menu, `scroll-margin-top` on every anchor target.
- Zero dead `href="#"` links left on any page.
- Responsive images: AVIF + WebP `srcset` at 3–4 widths per photo including a 2880px hero,
  with the original JPEG as fallback.
- Brochure recompressed 12.1 MB → 2.0 MB (verified page-by-page that it still renders).
- One signup form per page: the footer band is suppressed where a page already carries the
  newsletter (homepage section 08, or a CTA card row).

## Tooling

- `../tools/inject.py` — shared utility bar, nav, mobile menu, newsletter band and footer.
- `../tools/seo.py` — titles, descriptions, canonical, hreflang, OG/Twitter, JSON-LD,
  `sitemap.xml`, `robots.txt`. `SITE_URL` must become the production domain before launch.
- Run both after editing their templates.

## Not in this pass

Astro migration, Payload CMS, waitlist automation, payments, analytics and EN — see
`../brief/docs/04-ARCHITECTURE.md` and `05-EXECUTION.md`. This pass is the 10 September
milestone only.
