# Current state — what exists, and what does not

Verified 8–9 September 2026 with live requests against the deployed site, not
inferred from the code.

---

## What is deployed and working

Staging: `https://demo-impact-c399e3.netlify.app`
Production domain `wemakeimpact.be` is **not yet under our control** — the client
had not provided DNS access. Staging carries `X-Robots-Tag: noindex` on every
non-production host so it cannot compete with the real domain in search.

| Thing | Proven by |
|---|---|
| 24 static HTML pages, 12 NL + 12 EN | In `site/` here |
| Newsletter signup → Brevo | Posted live; contact appeared in list 3 |
| Waitlist signup → Brevo | Same contact then in lists 3 and 4 — each branch picks its own list |
| Signup attribution | Contact carried `EVENT`, `FORM`, `LOCALE`, `GEMEENTE`, `LEEFTIJD`, `UTM_SOURCE` |
| Server-side validation | Waitlist without name and consent returns `422` with Dutch errors |
| Ticket Tailor webhook | Answers `401 bad signature` to unsigned requests |
| Ticket Tailor API | Key valid, `/v1/events` answers — returns empty, no events entered yet |
| Stripe test keys | `/v1/balance` answers, `livemode: false` |
| Plausible analytics | Meta tag in page, script loads only after consent |
| Box office link on `/events` | Present, with a no-JS fallback link |
| Function test suite | `node tools/test-functions.mjs` — 14 passed, 0 failed |

## What does not exist

- **A CMS.** No admin UI, no login, no database. Content is JSON and Markdown
  files edited by developers.
- **Participant management.** Registrations, attendance, guardians, dietary and
  medical notes, payment state — none of it modelled. Ticket Tailor holds what
  exists.
- **The automated "registration opened" email.** The data to target it is in
  place; the automation is not.
- **Any deployed dynamic app.** Everything live is static files plus two small
  serverless functions.

---

## How the live site is built — this will surprise you

There is **no build step at deploy time.** `netlify.toml` sets `command = ""`
and publishes `site/` directly. The HTML in `site/` is **committed to git** and
generated locally by a Python pipeline:

```
python tools/build.py     # inject → seo → fingerprint → i18n → check → i18n-check
```

Consequences you must not learn the hard way:

1. **`PUBLIC_SITE_URL` and `PUBLIC_PLAUSIBLE_DOMAIN` are build-time values.**
   Setting them in the hosting platform's UI does nothing — the domain is baked
   into the committed HTML. They must be passed on the command line when
   building, and the output committed.
2. **English is generated, not written.** The 12 Dutch pages are hand-authored;
   `tools/i18n.py` produces the English ones from `i18n/en.json`, keyed by the
   exact Dutch string. Editing an English page directly is pointless — it is
   overwritten on the next build.
3. **Assets are fingerprinted.** CSS and JS carry `?v=<content hash>` so they can
   be cached forever. Adding a JS file means registering it in
   `tools/fingerprint.py`.

If the new repo keeps the static site, keep this pipeline or replace it
deliberately. If the CMS eventually renders the pages, this all goes away — but
that is a bigger job than it looks, because the pipeline also does the i18n, the
SEO head blocks, the sitemap and an HTML validity check.

---

## The Astro app — read before you reuse it

There is a second, **undeployed** implementation in `web/` of the original repo:
an Astro 5 app with content collections. It is not included here as a runnable
app, but its schema file is: `reference/content.config.ts`.

**Why it is not deployed:** it builds only 6 of the 20 pages, and has no English
routing. Seven pages exist only as static HTML. Publishing it would ship a site
missing most of itself.

**Why it still matters to you:** those Zod schemas are the most carefully
considered artefact in the project. They were written to mirror a planned Payload
CMS data model, and they translate almost directly into Postgres tables. See
[03-DATA-MODEL.md](03-DATA-MODEL.md). **Do not re-derive the data model from the
HTML — start from that file.**

**A defect worth knowing:** its `/api/waitlist` route originally accepted
submissions with no guardian consent and returned `200`, and the event page had
no consent checkbox at all. Both were fixed on 9 September. If you port anything
from that app, port the fixed version and keep the server-side consent check.
This form collects a child's first name and age.

---

## Known-good behaviours you must not regress

**A `200` from the signup endpoint does not mean the contact was stored.** It is
built so a Brevo outage never loses a signup: the visitor always gets a friendly
answer, the failure goes to the log, and Netlify Forms keeps an audit copy. If
you rebuild this, keep that property — but also keep the log, because it is the
only way to tell success from silent failure.

**Brevo silently discards what it does not recognise.** A `tags` array is
accepted and thrown away entirely on this account. An attribute that has not been
created on the account is accepted and thrown away too — with a `201` response.
A form field added without first creating its Brevo attribute will look like it
works and lose the data every time.

**Consent gates third-party scripts.** Plausible and the Ticket Tailor widget
both load only after the visitor accepts the relevant category in the cookie
banner. Failing closed is deliberate.
