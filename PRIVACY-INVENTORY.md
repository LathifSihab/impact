# Data-processing inventory — wemakeimpact.be

For IMPACT's lawyer or accountant, so the privacy statement can be written without
first having to work out what the site collects.

Compiled 8 September 2026 by DRP BuildLab, **read out of the code rather than from
memory** — every field below was enumerated from the deployed forms. Where a value
is unknown to us it says so rather than guessing; those are the questions back.

IMPACT is the **controller**. DRP BuildLab is a **processor** while it builds and
operates the site. Each third party named below is a sub-processor.

---

## 1. What the site collects today

Four forms. Nothing else on the site collects personal data — no account, no
comments, no chat, no advertising pixel.

### 1a. Waitlist for an event — `event.html`

The only place a **minor's** data is collected, and therefore the most sensitive
thing on the site.

| Field | Type | Required | About |
|---|---|---|---|
| `naam` | text | yes | **The child's first name** |
| `leeftijd` | number | yes | **The child's age**, validated against the edition's range |
| `email` | email | yes | The parent or guardian |
| `gemeente` | text | no | Municipality |
| `consent` | checkbox | yes | Explicit confirmation: parent or guardian, agrees to the privacy statement |

- **Purpose** — notify the parent when registration for that edition opens; check the age group fits.
- **Legal basis** — consent, given by the adult. The form blocks submission without the tick.
- **Children** — no child ever supplies their own data: the contactable identity is the adult's.
- **Retention** — *to be decided.* Proposal: twelve months after the edition, then delete.

### 1b. Newsletter — all 22 pages

| Field | Type | Required |
|---|---|---|
| `email` | email | yes |

- **Purpose** — one email a month about upcoming editions.
- **Legal basis** — consent. Double opt-in is planned but **not yet implemented**; today a
  submission subscribes directly. Worth confirming whether the lawyer wants double opt-in
  before launch — we would recommend it, and Brevo does it natively.
- **Retention** — until the person unsubscribes.

### 1c. Contact — `contact.html`

| Field | Type | Required |
|---|---|---|
| `naam` | text | yes |
| `email` | email | yes |
| `onderwerp` | select | yes |
| `bericht` | free text | yes |

- **Purpose** — answering the question.
- **Legal basis** — legitimate interest, or pre-contractual steps where it concerns a booking.
- **Note** — free text. Someone may volunteer far more than we ask for, including health or
  family circumstances. Worth a line in the policy.
- **Retention** — *to be decided.* Proposal: two years after the last contact.

### 1d. Hosted Experience request — `hosted-experiences.html`

| Field | Type | Required |
|---|---|---|
| `contactnaam` | text | yes |
| `org` | text | yes |
| `email` | email | yes |
| `idee` | free text | yes |

- **Purpose** — assessing and answering a partnership request.
- **Legal basis** — pre-contractual steps. Usually business rather than personal data, but the
  named contact is a person.
- **Retention** — *to be decided.* Proposal: as for contact.

---

## 2. Attached to every submission

Not typed by the visitor, added by the page. This is the *"which campaign drove this
signup"* requirement, and it is personal data because it is attached to an identifiable
record.

| Field | Value | Source |
|---|---|---|
| `page` | the page submitted from | current URL |
| `locale` | `nl` or `en` | `<html lang>` |
| `landing_page` | first page of the session | `sessionStorage` |
| `referrer` | where they arrived from | `document.referrer` |
| `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term` | campaign tags | the landing URL |
| `gclid`, `fbclid` | Google / Meta click identifiers | the landing URL, if present |

**No IP address, device fingerprint or profile is recorded by us.** The campaign values are
read from the URL the visitor arrived on and held in `sessionStorage` for that visit only —
they are attached to the submission, not accumulated across visits.

`gclid` and `fbclid` only ever appear if IMPACT runs paid advertising. They are worth naming
in the policy anyway, because the site would capture them the day a campaign starts.

---

## 3. Browser storage

**No cookies are set by this site.** Everything below is `localStorage` or
`sessionStorage`, first-party, and never sent to a server.

| Key | Type | Purpose | Lifetime |
|---|---|---|---|
| `impact.consent` | localStorage | The cookie-banner choice | Until changed |
| `impact.dome.until` | localStorage | Do not show the newsletter panel again | 90 days after dismissal, 365 after signing up |
| `hasSeenPreloader` | sessionStorage | Intro animation already shown | The tab session |
| `impact.campaign`, `impact.landing`, `impact.referrer` | sessionStorage | Attribution for §2 | The tab session |

Our reading is that all of these are *strictly necessary* for functionality the visitor
asked for, and none identifies anyone. **Worth the lawyer confirming**, particularly the
attribution keys, which is why the consent banner exists and lists them.

---

## 4. Processors and where the data goes

| Processor | What it holds | Where | Status |
|---|---|---|---|
| **Netlify** | Hosting, and today **every form submission** | EU/US, DPA + SCCs published | Live. Interim sink only |
| **Brevo** | Newsletter and waitlist contacts | France (EU) | **Not yet connected** |
| **Ticket Tailor** | Ticket buyers, waitlist entries, attendees | UK, UK GDPR adequacy | **Not yet connected** |
| **Stripe** | Payment data. Card details never touch our servers | EU/US, DPA + SCCs | **Not yet connected** |
| **Plausible** | Aggregate traffic. No cookies, no personal data | EU (Germany) | **Not yet installed** |
| **Google Fonts** | Serves two webfonts; the browser's IP reaches Google | US | **Live today** — see below |

**Two things for the lawyer specifically.**

Form submissions currently land in **Netlify Forms** and nowhere else. That is a temporary
sink until the backend decision is made, and it should be named in the policy only if it is
still true at launch.

**Google Fonts is loaded from Google's CDN**, which discloses the visitor's IP address to
Google before any consent is asked. German courts have ruled against exactly this. It is a
twenty-minute fix — self-host the two font files — and we recommend doing it before launch
rather than defending it. Flagging it because it is the one live third-party request on the
site today, and it is not in anyone's list of asks.

---

## 5. Rights, and what has to be possible

The policy will promise access, correction, deletion and withdrawal of consent. Practically:

- **Today** — submissions live in Netlify Forms; deletion is manual, through their UI.
- **After the backend decision** — deletion has to work across Brevo, the ticketing platform
  and our own store at once. Worth building a single "delete this person" path rather than
  three manual ones.
- **Withdrawal of consent** — unsubscribe in every email (Brevo does this natively), and the
  cookie banner is reopenable from the footer on every page.

---

## 6. Questions only IMPACT can answer

The policy cannot be finished without these. Everything else above is settled.

1. Legal name, legal form (vzw or bv), registered office, company number.
2. Retention period per category — three proposals are in §1 to react to.
3. Who is the contact point for a data request, and within what period do you answer?
4. **Photography and video of minors**: who consents, in what form, and how is it withdrawn?
   Separate from the site, and currently blocking the participant clips.
5. Is there a DPO, or is that not required at your size?
6. Do you already have a processor agreement template, or should we propose one?

---

*Prepared by DRP BuildLab. This is an inventory, not legal advice — it exists so that the
person giving the legal advice does not have to reverse-engineer the site first.*
