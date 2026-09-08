# 5. Plausible — analytics

Plausible counts visitors. It was chosen over Google Analytics because it sets no
cookies, collects no personal data, and is hosted in the EU — the brief asked for
"privacy-friendly analytics", and Google Analytics is the opposite of that.

About 10 minutes. Roughly €9/month after the trial.

---

## Step 1 — Account and site

1. Sign up at [plausible.io](https://plausible.io).
2. **Add a website**.
3. Domain: `demo-impact-c399e3.netlify.app` — the staging address, not
   `wemakeimpact.be`, because that is what the site answers on today.
4. It will show you a `<script>` tag. **Ignore it.** It is already in the site,
   waiting for the domain.

> At launch, add `wemakeimpact.be` as a second site rather than renaming this
> one. Nothing of value is lost — pre-launch traffic is us testing.

## Step 2 — Into Netlify

| Key | Value |
|---|---|
| `PUBLIC_PLAUSIBLE_DOMAIN` | `demo-impact-c399e3.netlify.app` |

**Trigger deploy → Deploy site.**

Until this variable exists, the analytics tags are not in the site's HTML at all.
That is intentional: no half-configured tracker sitting in the page.

## Step 3 — Goals

A **goal** is something worth counting beyond a page view. The site already sends
these; you only have to name them so Plausible displays them.

**Site settings → Goals → Add goal → Custom event**, once for each:

| Goal name | Fires when |
|---|---|
| `newsletter_signup` | Someone subscribes to the newsletter |
| `waitlist_join` | Someone joins an event waitlist |
| `dome_signup` | Someone subscribes via the pop-up |
| `dome_shown` | The pop-up was shown |
| `dome_dismissed` | The pop-up was closed without subscribing |
| `section_view` | A visitor actually reached a section of a page |

Type each name exactly as written.

`section_view` is the one that answers the brief's "page and section
engagement". Plausible on its own counts page views, which tells you someone
opened a page — not whether they ever reached the part that mattered. Comparing
`dome_shown` against `dome_signup` and `dome_dismissed` also tells you whether
the pop-up is earning its interruption.

## Step 4 — Know what you will and will not see

Analytics only loads **after a visitor accepts the Statistics category** in the
cookie banner. So the numbers are lower than reality, always.

That is a deliberate choice: the site offers a banner with a Statistics option,
so tracking someone who declined would make that banner a lie. Plausible sets no
cookies and arguably needs no consent at all — if IMPACT's lawyer prefers it to
run unconditionally, that is defensible, and DRP removes the gate and the
category together. One without the other is the bad outcome.

- [ ] Account created, staging domain added
- [ ] `PUBLIC_PLAUSIBLE_DOMAIN` in Netlify, site redeployed
- [ ] Six goals created
- [ ] Understood that numbers are consent-limited
