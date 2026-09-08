# IMPACT — handoff for the new repository

Written 9 September 2026, from a working project. Everything stated here was
checked against the code or tested live, not recalled.

**You are picking up a finished bilingual marketing site and building the thing
it never had: a content management system.** The site is live, verified and not
in question. Your job is the backoffice.

---

## Read these in order

| File | What it answers |
|---|---|
| [01-BRIEF.md](01-BRIEF.md) | What the client asked for, in their words, and which parts are still unmet |
| [02-CURRENT-STATE.md](02-CURRENT-STATE.md) | What exists and is proven working, and what does not exist at all |
| [03-DATA-MODEL.md](03-DATA-MODEL.md) | The ten content types, every field, ready to become Postgres tables |
| [04-INTEGRATIONS.md](04-INTEGRATIONS.md) | Brevo, Ticket Tailor, Plausible — the live contracts you must not break |
| [05-DESIGN-SYSTEM.md](05-DESIGN-SYSTEM.md) | Type, colour, spacing and components, so the CMS looks like it belongs |
| [06-CMS-SCOPE.md](06-CMS-SCOPE.md) | What to build, what was decided and why, what is explicitly out of scope |
| [07-DECISIONS.md](07-DECISIONS.md) | Judgement calls already made, with reasoning, so they are not relitigated |

## What is in this folder

```
site/          24 HTML pages — 12 Dutch, 12 English. The live site, as shipped
assets/        css, js, brand — the complete design system (~450 KB)
reference/     content.config.ts, the two serverless functions, all content
               files, the translation store, the env var names
```

**Not included:** photography (17 MB), video (19 MB) and the brochure PDF. They
live in the original repo under `site/assets/img`, `site/assets/video` and
`site/assets/impact-brochure.pdf`. The HTML references them by those paths, so
copy them across when the site moves, or the pages render without images.

**No secrets are in this folder.** `reference/env.example.txt` carries the
variable *names* and what each is for. Every value lives in the deploying
platform's environment settings and nowhere else — that is deliberate, so
handover is editing boxes in a UI rather than a code change.

---

## The one-paragraph version

IMPACT is a Belgian youth development brand for ages 8–25. The site is Dutch and
English, built as static HTML with a Python build pipeline, deployed on Netlify.
Signups flow to Brevo already segmented by event, locale and campaign. Events,
tickets and waitlists are handled by Ticket Tailor, not by us. Analytics is
Plausible behind a consent banner. **There is no CMS: content is JSON and
Markdown files edited by developers**, which is the gap you are closing.

## The one thing that will bite you

The client's stated top priority is *"manage data, registrations, events and
participants cleanly from day one."* It has never been delivered. Every previous
plan for it slipped. Read [06-CMS-SCOPE.md](06-CMS-SCOPE.md) before designing
anything, because two of the four nouns in that sentence — registrations and
participants — are already handled by Ticket Tailor, and rebuilding them would
be the most expensive mistake available.
