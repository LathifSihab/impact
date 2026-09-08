# How to test this end to end

Two things live in this repo and they are tested differently:

| | What it is | How to run |
|---|---|---|
| `site/` | The static craft-pass site. What staging serves today, what the client reviews on 10 Sep. | Any static server |
| `web/` | The Astro app that replaces it. CMS-driven event pages and real form endpoints. **Lives on the `feat/astro-cms` branch.** | `git checkout feat/astro-cms` then `npm run dev` |

Work through part 1 or part 2 depending on what you want to check. Part 3 is the
cross-cutting stuff (responsive, keyboard, reduced motion) and applies to both.

---

## 0. Structural check — run this first, it takes a second

```bash
python tools/check_html.py
```

Balanced container tags across all 20 pages, and every local `href`/`src`/`poster`
resolving to a file that exists. Run it after any hand edit to a page.

It exists because a lost `<div class="expert-slots">` opening tag shipped
unnoticed on two pages: the orphaned `</div>` closed the page's own column
wrapper instead, which threw the FAQ section into the event page's sidebar column
and dropped the waitlist card to the bottom of the document. Nothing errored and
the markup looked fine — the browser just silently reflowed around it. The same
run also found a duplicate `</main>` on the homepage.

Also worth knowing, for the event page specifically: the waitlist column is taller
than a laptop viewport, so it only sticks at `min-height: 1320px`. Below that it
scrolls normally, on purpose — a stuck column that does not fit puts its own
bottom permanently out of reach. The sticky metabar carries the waitlist CTA at
every viewport, so nothing is lost.

## 0b. Responsive audit

```bash
cp tools/audit_responsive.html site/_audit.html
python -m http.server 8099 -d site &
for w in 320 360 390 768; do for p in index over events event samenwerken     social-impact hosted-experiences journal media contact; do
  for loc in "" "en/"; do
    chrome --headless=new --disable-gpu --dump-dom       "http://localhost:8099/_audit.html?p=$loc$p.html&w=$w" | grep -o "AUDIT .*"
  done
done; done
rm site/_audit.html
```

It loads each page inside an iframe of a given CSS width — headless Chrome
clamps its own window to about 500px, so measuring the top-level viewport can
never reach phone sizes — and reports document overflow, the outermost elements
crossing the viewport edge, content clipped by a non-scrolling box, buttons whose
label does not fit, and images wider than their container.

**Serve it over HTTP, not `file://`.** The English pages reference `/assets/...`
root-absolute, which under `file://` resolves to the drive root: they load with
no stylesheet and every number is then meaningless. That cost a full round of
false findings.

`docOverflowX=-15px` on a clean page is the reserved scrollbar gutter, not a
problem. Known-intentional overflow (marquee track, cinema track, the oversized
preloader word, `.sr-only`, the skip link) is filtered by the `ALLOW` list in the
harness.

## 1. The static site (`site/`)

```bash
cd site
python -m http.server 8080
# then open http://localhost:8080
```

Use a server, not `file://` — the hero video and the fonts behave differently on
the file protocol.

### 1.1 Homepage

| Step | Expect |
|---|---|
| Open `/` | Hero fills the screen: **BUILDING FOUNDATIONS FOR LIFE.** in three ragged lines, Archivo Black, white on the photo |
| Watch the first second | Each headline line rises into place, then the trust row, intro and buttons follow. Happens once, on load only |
| Wait ~2s | The still is replaced by a muted 12.8s looping video, fading in. It loops seamlessly with no black frame |
| Scroll to *Waarvoor kom je?* | Six route cards. Each has one obvious next step |
| Scroll to the red *Six foundations* band | Six 4:5 portraits, each with a `[01] SELF-KNOWLEDGE` chip on the image, bleeding off the right edge |
| Click the → arrow top-right of that band | The row scrolls one card. The `01 / 06` counter and the progress bar follow |
| Drag / wheel-scroll the row instead | Same. **Nothing auto-advances** — that was removed on purpose |
| Scroll to *Upcoming IMPACT events* | Three rows. Click the row → the event page; click the pill → the same page at `#wachtlijst`. Two separate targets, and the pill is not inside the row's link |
| Look at a row's label | `Camp` and `5 dagen` as separate meta cells, not "Camp · 5 dagen" |
| Scroll to the black *formats* section | Four numbered peers, then a rule, then Hosted Experiences set apart with `—` |
| Scroll to *IMPACT FOR ALL* | No counters here (the real figures live on the social-impact page) |
| Scroll to *Don't take our word for it.* | Three portrait players on burgundy. Nothing is downloaded before the section is near the viewport (`preload="none"`, then `auto` at 300px out — check the Network tab) |
| Keep it in view | The most visible clip starts playing **muted**, with a "tik voor geluid" pill top-left. The other two stay on their posters — only one clip ever plays |
| Scroll away | It pauses. Scroll back and it resumes |
| Click the pill | Sound on, the pill disappears, the clip keeps playing |
| Switch tabs and back | It paused while the tab was hidden |
| Turn on *Reduce motion* | Nothing autoplays; the posters stay and the pill never appears |
| Scroll to the bottom | Partner marquee runs continuously with nine real logos, greyscale, colour on hover, pausing while hovered |
| Look at the footer | "Built by DRP BuildLab", hyperlinked. Phone and Instagram are real links. No dead `#` links anywhere |

### 1.1a The sticky nav

Scroll any page. At the top the nav is spacious (22px padding, 26px logo, no
shadow); past 50px it compacts (10px padding, 21px logo, soft shadow) and stays
pinned to the top. Scrolling back under 24px restores it — the gap between 50
and 24 is deliberate hysteresis, so a nav sitting exactly on the threshold
cannot flicker on a trackpad.

The utility bar is not sticky and scrolls away; only the nav pins.

Two things to check that are easy to break:

- **Anchor links** (`/event.html#wachtlijst`, the nav dropdown links) must land
  below the nav, not underneath it. `[id]{scroll-margin-top}` reads `--nav-h`.
- **The event page metabar** sticks directly below the nav, never over it. Its
  `top` also reads `--nav-h`, which main.js writes from the nav's real measured
  height on load, on resize, and when the padding transition ends — so no
  number needs keeping in sync when the nav's padding or logo changes.

### 1.1b The preloader

It plays **once per browser session**, on the homepage. Any other page visited
first consumes the flag, so it never appears halfway through a session.

```js
// DevTools console — replay it
sessionStorage.removeItem('hasSeenPreloader'); location.reload();
```

What to look for, in 1.88s total:

- EXPERIENCES → CONNECTION → GROWTH, each rising in and out (0.24s each)
- `[IMPACT]` landing with red brackets, held briefly
- the two panels parting, tearing the wordmark in half as they go
- the hero headline revealing **as** the curtain opens, not before it

Things that should all end with the page visible and scrollable:

| Test | Expected |
|---|---|
| Reload immediately | No preloader (flag set) |
| New tab | Preloader plays again (session is per tab) |
| Block `cdnjs.cloudflare.com` in DevTools → Network → Block request domain | No preloader at all; page renders normally. The `<head>` failsafe clears the overlay after 3s at the latest, but the animation is skipped, not delayed |
| `prefers-reduced-motion: reduce` (DevTools → Rendering) | No animation, no black frame |
| Private window with site data blocked | No preloader, no error |
| Scroll during the animation | Locked, and the page must not shift sideways when it unlocks — the scrollbar gutter is reserved for exactly this |

The decision to run lives in an inline `<head>` script, not in `preloader.js`: by
the time a deferred script executes, the page has already painted, so a black
overlay applied there would flash the content first.

### 1.1c Signup capture and attribution

Every form now posts to Netlify Forms. Four collections, by `form-name`:
`newsletter` (all 20 pages, band + section + dome), `waitlist`, `contact`,
`hosted-experience`.

**Capture only works on the deployed site.** A local static server answers a POST
with 501, so `postForm` falls back to the optimistic success state on
localhost/127.0.0.1/file: — deliberately, so local work does not show a failure
nobody can act on. It never does that on a real host. To verify capture for real,
submit on the Netlify URL and look in **Netlify → Forms**.

What each submission carries, beyond its own fields:

| Field | From |
|---|---|
| `page` | the page submitted from |
| `locale` | `<html lang>` |
| `landing_page` | the first page of the session |
| `referrer` | `document.referrer` on arrival |
| `utm_*`, `gclid`, `fbclid` | the landing URL, kept for the session |

That last row is the brief's *"which campaign/page/waitlist drove each signup"*.
It has to travel with the row, because analytics can attribute a **visit** but not
a **record**. To test the session persistence: open
`/?utm_source=instagram&utm_campaign=test`, click through to another page, sign up
there, and the campaign should still be on the submission.

Verified body of a newsletter signup:

```
form-name=newsletter&bot-field=&email=ouder@example.be&page=/&locale=nl
&landing_page=/&referrer=&utm_source=instagram&utm_medium=story
&utm_campaign=camp-basketball-2027
```

Note the free Netlify tier is **100 submissions/month**. Fine for staging; the
real sink is whatever wins the backend decision.

### 1.2 The newsletter dome (the modal the client asked for)

```bash
# clear the 90-day suppression first
# DevTools console:
localStorage.removeItem('impact.dome.until')
```

| Step | Expect |
|---|---|
| Move the mouse out of the top of the window | A wide cream dome rises from the bottom |
| Press `Escape` | It closes |
| Reload and repeat the exit-intent | **It does not reappear** — dismissal is remembered for 90 days |
| Clear the key again, open it, press `Tab` repeatedly | Focus cycles inside the dome only. The page behind is `inert` |
| Submit a valid address | Success message, then it closes itself |
| Open `/event.html` and try exit-intent | **Never appears** — a waitlist form is the primary action there |
| At ≤820px wide | Opens at 60% scroll depth instead of exit-intent |

### 1.3 Event page — `/event.html`

| Step | Expect |
|---|---|
| Fill *Lena / 17 / ouder@example.be* and submit | Inline red error: "Deze editie is voor 8–14 jaar." **All typed values stay** |
| Empty the email and submit | Error under the email field, name and age still filled |
| Fix to age 11 and submit | The card is replaced by "Je staat op de wachtlijst" |
| Open the FAQ items | One opens at a time, `+` rotates to `×` |
| Scroll | The black meta bar sticks under the nav; the waitlist card sticks alongside the body |
| Resize to ≤820px | Meta bar un-sticks, waitlist moves inline, a fixed CTA bar appears at the bottom |

### 1.4 Pages that carry real content now

| Page | Check |
|---|---|
| `/over.html` | Hero is the **overlaid** variant: headline left, intro under it, the three age bands top-right, all set on the photo with no card (branddeck slide 6) · Six fundamenten with the brochure's own "Waar we op werken" lists · founders' own texts · two founder media cards · `#systeem` four-layer block · three named experts |
| `/social-impact.html` | Burgundy proof block: **30 / 11 / 4** counting up once on entry, with the "na Basketball Edition 2026" caption |
| `/samenwerken.html` | Partnership tier table (€2.000 → €7.000) · reach figures on burgundy · nine partner logos · three colour-blocked CTA cards |
| `/journal.html` | Category chips filter the grid. Cards use real camp photography |
| `/media.html` | Four real participant videos under *Bewegend beeld*, portrait with posters · six real camp photos in the archive grid · brochure download is 2.0 MB, not 12 |
| `/events.html` | Five upcoming rows, per-format sections, full overview table |

There should be **no string anywhere** that says content is missing —
"wordt aangeleverd", "demo", "placeholder". If you find one, that's a bug.

---

## 2. The Astro app (`web/`) — the CMS pipeline

The app is on the `feat/astro-cms` branch, so switch to it first:

```bash
git checkout feat/astro-cms
cd web
npm install        # first time only
npm run dev        # http://localhost:4321
```

`npm run dev` runs plain Astro. The Netlify adapter is only attached for
`npm run build`, because its local edge-function bridge needs the Netlify CLI.

### 2.1 The test that actually matters: adding an event without touching code

This is the acceptance criterion from `brief/docs/04-ARCHITECTURE.md` §4.

1. Copy an existing event:
   ```bash
   cp src/content/events/day-brussels-2027.json src/content/events/test-event.json
   ```
2. Edit `test-event.json` — change `title`, `dateText`, `ageMin`/`ageMax`, and set
   `"status": "waitlist"`.
3. Save. The dev server reloads.
4. Open **http://localhost:4321/events/test-event/**

Expect: a complete event page exists at that URL, with a waitlist form whose age
validation uses *your* `ageMin`/`ageMax`, and the event appears in
`/events#upcoming` and in the overview table — with no code change.

Then flip `"status"` to `"past"`: the event drops out of *Upcoming*, its page
shows "Deze editie is voorbij" pointing at Journal, and the overview row reads
*Afgelopen · in Journal*.

Delete `test-event.json` when you're done.

### 2.2 The form endpoints

Client-side validation blocks bad input **without a network request**; valid
input is POSTed and the server's own response drives the result.

```bash
# valid
curl -s -X POST http://localhost:4321/api/waitlist \
  -F event=camp-basketball-edition-2027 -F naam=Lena -F leeftijd=11 \
  -F email=ouder@example.be -F ageMin=8 -F ageMax=14
# {"ok":true,"message":"Je staat op de wachtlijst. We sturen een bevestiging naar ouder@example.be."}

# age outside the event's own range — rejected server-side too
curl -s -X POST http://localhost:4321/api/waitlist \
  -F event=camp-basketball-edition-2027 -F naam=Lena -F leeftijd=17 \
  -F email=ouder@example.be -F ageMin=8 -F ageMax=14
# {"ok":false,"errors":{"leeftijd":"Deze editie is voor 8–14 jaar."}}

# newsletter
curl -s -X POST http://localhost:4321/api/newsletter -F email=nope
# {"ok":false,"errors":{"email":"Vul een geldig e-mailadres in."}}
```

In the browser, on `/events/camp-basketball-edition-2027/`:

| Step | Expect |
|---|---|
| Submit with age 17 | Inline error, values kept, **no POST in the Network tab** |
| Change to 11 and submit | One `POST /api/waitlist`, button shows "Even geduld…", then the success state using the server's message |
| Watch the dev server terminal | A `[waitlist]` line with `event`, `locale`, `source` and `utm_*` — the attribution fields |
| Add `?utm_source=test&utm_campaign=demo` to the URL and submit again | Those values appear in the logged `utm` object |

Nothing is stored yet — Payload and Brevo are the 17 September milestone and
are marked `TODO(17 Sep)` at the two lines where they land.

### 2.3 Production build

```bash
npm run build
npx http-server dist -p 8081     # or: python -m http.server 8081 --directory dist
```

Expect: four event pages prerendered (one per content file), plus the SSR
function for `/api/*`. The build prints
`The collection "testimonials" does not exist or is empty` — that is **correct**:
testimonials stay empty until the client confirms consent.

---

## 2b. The English site

English is generated from the Dutch pages, so there is one set of pages to keep in
structural sync. `site/en/` is build output — never edit it by hand.

| Step | Expect |
|---|---|
| Open `/` and click **EN** top right | Same page in English at `/en/`, EN highlighted |
| Click **NL** | Back to the Dutch page you came from, not the Dutch homepage |
| Any `/en/` page | `<html lang="en">`, English nav (ABOUT · EVENTS · PARTNER WITH US · SOCIAL IMPACT), English title and description |
| View source on `/en/over.html` | `canonical` points at the **/en/** URL, and `hreflang` lists both locales |
| `/sitemap.xml` | 20 URLs — both locales, each declaring its counterpart |
| Change a Dutch string | `python tools/i18n.py --extract` lists it as untranslated; fill it in `i18n/en.json`, run `python tools/i18n.py` |

## 3. Cross-cutting checks (both)

### Responsive

Test at **1440 · 1180 · 834 · 390**. At every width:

- No horizontal scrollbar on any page. The only things that overflow on purpose
  are the partner marquee and the fundamenten strip.
- ≤820px: nav collapses to the burger, the overlay menu opens with the page
  behind it locked and `inert`, and closes on `×` or `Escape`.
- ≤820px: the partnership tier table **transposes to one card per tier** — same
  markup, no duplicated DOM.
- Headlines never clip. They were hard-broken with `<br>` before; now the line
  count comes from the type block.

### Keyboard only

Tab through a page without touching the mouse:

1. First stop is **"Naar de inhoud"** (skip link) — press Enter, focus lands on `#main`.
2. Every focused element has a visible red outline.
3. Nav dropdowns open on focus and close on `Escape`.
4. The fundamenten strip scrolls with ← → when focused.
5. Inside the dome, Tab cycles and never escapes to the page behind.

### Reduced motion

Turn on *Reduce motion* (macOS: Accessibility → Display; Windows: Settings →
Accessibility → Visual effects → Animation effects off), then reload:

- The hero shows the **still**, not the video, and does not animate.
- The partner marquee stops.
- Counters show their final values immediately.
- The dome appears without the rise.

### Console

There should be **zero** console errors on every page, in both `site/` and `web/`.

---

## 4. Known and deliberate

These will look like bugs and are not:

- **`testimonials` is empty** — nothing renders until IMPACT confirms consent for
  the parent quotes (`SIGN-OFF.md`).
- **Journal cards are not links** in `site/` — no articles exist yet. In `web/`
  they link to the CMS entry.
- **No Privacy / Algemene voorwaarden links** — no copy exists, so they were
  removed rather than pointing nowhere. Both are required before launch.
- **The English copy is our translation, not the client's voice.** She writes the Dutch;
  English was generated from it so the switch works end to end. When her Dutch copy lands,
  `tools/i18n.py --extract` reports exactly which English strings went stale.
- **No LinkedIn or TikTok links** — no URLs supplied.
- **The hero video is still a placeholder** built from their own stills. The four clips the
  client sent are 480x848 portrait phone recordings, so they are used as participant
  testimonials rather than as a landscape header. Drop a 16:9 `hero.webm` + `hero.mp4` into
  `assets/video/` to replace the placeholder.
- **The participant videos have no captions.** The clips carry speech and no transcript was
  supplied, so they currently fail WCAG 1.2.2. Transcripts are on the ask list; caption files
  get generated from them.
- **Video masters live in `brief/video-masters/`**, outside the publish directory, so the
  24 MB of WhatsApp originals is never deployed. `tools/process_client_video.py` regenerates
  the web assets from them.
- **`SITE_URL` is the production domain** in `tools/seo.py` and `web/src/lib/seo.ts`.
  Staging is kept out of the index by `netlify/edge-functions/noindex.ts`, which adds
  `X-Robots-Tag: noindex, nofollow` on every host that is not wemakeimpact.be. To verify
  after a deploy: `curl -sI https://<site>.netlify.app | grep -i x-robots-tag` should show
  it, and the same call against the production domain should not.
