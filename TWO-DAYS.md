# Two days — what actually gets finished

Written 9 September 2026. **Day 1 is today, Day 2 is 10 September.**

This replaces the October sequencing in `STATUS.md` for everything inside the
next 48 hours. `STATUS.md` stays the full picture; this file is only what fits.

---

## The decision this forces

Two days is not enough to build anything new and prove it works. So the plan is
**ship what is already built and verified, and close the gaps that would
embarrass us** — not start anything.

### Out of scope — say so now, not on Day 2

| Not happening | Why | Where it goes |
|---|---|---|
| A CMS Mirte can log into | Nothing to manage: the content collections live in `web/`, which is not deployed | October |
| Astro page parity | 6 of 20 pages built, no English routing. Days of work, not hours | October |
| Payload + Neon | Needs a server and a database nobody can operate by Thursday | October |
| Participant management (19) | Not modelled anywhere | Ticket Tailor's backoffice covers it for now |
| On-demand rendering (16) | Solved by events living in Ticket Tailor | Not needed |
| Automated "registration opened" email (11) | The **manual** version is a ten-minute Brevo campaign and is enough for one launch | Automate in October |

**The live site stays `site/` — the static build.** Do not switch `netlify.toml`
to publish `web/dist`. It would ship a site missing fourteen pages.

### In scope — what ships

The static site, both languages, with Brevo signups, Plausible, the Ticket
Tailor box office and the webhook. All of that is built and verified working
today. What is left is configuration, content and proof.

---

## Blocking — must come from IMPACT today, or Day 2 fails

Send these as **one message**, this morning, with the consequence of each
stated. `ASKS.md` has the Dutch text. Nothing in *Day 2* can start without them.

| # | Ask | If it does not arrive |
|---|---|---|
| 2 | **The 1–2 September events** — title, dates, location, age range, price, capacity | There is nothing to sell. The box office renders an empty list and the launch has no product |
| 3 | **Parental consent for the minors on camera**, in writing, per clip | The four homepage clips must come down. This one can stop a launch outright |
| 5 | **Privacy policy + terms — the actual text** | Every `[ bracket ]` on `/privacy` ships visible, on the page the forms link to for consent |
| 4 | **Domain + DNS access** | No cutover. The site stays on the staging URL, unindexed |

Item 1 (Stripe live keys) matters only if money must move on launch day. If it
can launch as free waitlists, it is not blocking.

---

## Day 1 — today

### Ours, no dependencies — do these first

- [ ] **Push the six pending commits.** The box office wiring, the consent fix
      and the docs are all local only. Nothing below is live until this happens.
- [ ] **Redeploy and re-run the sweep** in `setup/07-what-is-broken-now.md`.
      Expect `plausible: True`, `canonical: True`, `tt-webhook: 401 bad
      signature`, `subscribe: 422`.
- [ ] **Delete the test contacts** in Brevo — `agro.dude95@gmail.com` is on both
      lists, tagged `source:drp-selftest`.
- [ ] **The OG share image** (item 14). Currently a cropped content photo, and
      every shared link uses it. `tools/make_og.py` exists. One hour.

### Yours, in a dashboard — 30 minutes total

- [ ] **`BREVO_SENDER_EMAIL`** (item 21). It points at a personal gmail; the only
      verified sender is `lathif.sihab-dewantoro@drpbuildlab.com`. **No mail can
      go out until this is fixed** — not the double opt-in, not the Day 2
      campaign. Do this before anything else.
- [ ] **Connect Stripe inside Ticket Tailor** — Settings → Payments. That is the
      whole of item 1 for development. Test mode is enough today.
- [ ] **Check the Ticket Tailor webhook** points at
      `/.netlify/functions/tt-webhook` and not at a page. A page returns 200, so
      Ticket Tailor records a successful delivery and the signups vanish
      silently.

### If the events arrive today

- [ ] **Enter them in Ticket Tailor** — title, date, location, age range, price,
      capacity, and a waitlist per edition. Data entry, not code, and the single
      thing that turns the box office from empty to real.

---

## Day 2 — tomorrow

### Only if the events landed

- [ ] **Rebuild and deploy** with the box office set. One command — `STATUS.md`
      → *Building for a domain*.
- [ ] **One real end-to-end run:** join your own waitlist through the site,
      confirm the contact appears in Brevo list 4 carrying `EVENT`, `LOCALE` and
      `FORM`, and confirm Ticket Tailor logged the webhook delivery.
- [ ] **Send the "registration opened" campaign by hand** from Brevo, filtered on
      the `EVENT` attribute. This is item 11 without the automation, and for one
      launch it is indistinguishable from the automated version.

### Regardless

- [ ] **Privacy text in**, if it arrived. A copy-paste into `site/privacy.html`
      and `i18n/en.json`, then rebuild.
- [ ] **Full sweep again**, plus `node tools/test-functions.mjs` (14 checks) and
      `python tools/build.py` (HTML + i18n checks).
- [ ] **Responsive spot check on a real phone**, not an emulator. The box office
      section is the only markup added since the last full audit.
- [ ] **Write the handover note**: which four dashboards hold what, and that
      every key lives in Netlify rather than in code.

---

## Definition of done

The launch is real when all of these are true:

```powershell
$b='https://demo-impact-c399e3.netlify.app'
$h=(Invoke-WebRequest -UseBasicParsing $b/).Content
"plausible : " + [bool]($h -match 'plausible-domain')
"canonical : " + [bool]($h -match 'demo-impact-c399e3')
"boxoffice : " + [bool]($h -match 'tt-box-office')
```

- All three `True`, and `/events` shows real editions rather than an empty list.
- A waitlist signup made through the site appears in Brevo carrying its `EVENT`.
- `tt-webhook` answers `401 bad signature` to an unsigned request.
- No `[ bracket ]` text remains on `/privacy`.
- The four clips either have written consent, or are not on the page.

---

## What to tell IMPACT

Say the shape of it plainly, because the gap between "a website is live" and
"they can manage it themselves" is exactly where a client feels misled:

> The site launches on the static build, with Ticket Tailor handling events,
> tickets and waitlists. Everything a visitor touches works, in both languages,
> and signups land in Brevo already segmented by event and campaign.
>
> **Content changes still come through us this month.** The self-serve
> backoffice — one login for content, registrations and participants — is
> October work, and it is the next thing we build. Events are the exception:
> those she manages herself in Ticket Tailor from day one.

That last line is the honest version of "self-serve from day one", and it is
true today. Do not claim more than it.
