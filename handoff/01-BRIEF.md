# The brief — what the client asked for

IMPACT is a youth development brand in Antwerp, Belgium, for young people aged
8–25. Camps, Days, Retreats, Community and Hosted Experiences, built around six
"foundations". Two founders: Mirte Rens and Jean-Marc Mwema.

This is the client's own brief, condensed, with an honest note on each part.

---

## Audiences — six visitor types, each needing an obvious next step

| Visitor | Their next step | Status |
|---|---|---|
| Young people / parents discovering or booking | Events → waiting list | ✅ built |
| Companies, sponsors, potential partners | Partner with us → For companies | ✅ built |
| Clubs / organisations wanting a co-developed experience | Hosted Experiences | ✅ built |
| Coaches / experts who might contribute | Partner with us → Experts & coaches | ✅ built |
| People who want to support the social mission | IMPACT FOR ALL → Contribute | ✅ built |
| First-time visitors just getting to know IMPACT | About IMPACT | ✅ built |

All six routes exist on the homepage, one click from their next step, in both
languages. **This part of the brief is done and is not your problem.**

## Visual direction

- Bilingual NL + EN — done, 12 pages each, translations in `reference/i18n-en.json`
- Heavy use of their own photography and video — done, from a large library
- Landscape video headers and horizontal image strips — done
- A partner/collaboration page that builds trust with professional parties — done
- "Built by DRP BuildLab" hyperlinked in the footer everywhere — done

## Conversion

- Recurring, contextual CTAs throughout, not one contact page — done
- Newsletter signup with real visibility, not a tiny footer form — done
- Very good SEO — technical foundation done; the rest is content and time

## Events & waitlists — *"this is a big one"*

- Every event gets its own page, with a separate waitlist where relevant — **built in the Astro app, which is not deployed**
- When registration opens, everyone on that event's waitlist gets an automatic, targeted email — **not built; see below**
- **"Build this so they can add new events/pages/waitlists themselves later without needing a rebuild each time — this needs to be genuinely self-serve"** — **not delivered**

## Backend & data

- Privacy-friendly analytics: visits, unique visitors, traffic source, page/section engagement, actions taken, signup conversion, **and which campaign/page/waitlist drove each signup** — done, including the custom part
- All newsletter + waitlist signups in one place, usable for targeted comms — done via Brevo, segmented on arrival
- **"CMS/backoffice structure is a big priority — they want to manage data, registrations, events and participants cleanly from day one"** — **not delivered. This is your job.**
- They still pay for Wix for another year and asked whether to link backend functionality to it — **answered: no.** Wix is a closed platform whose data layer cannot be queried by an external stack and whose automations cannot be triggered from these forms. It is kept only as the 301 redirect source until the subscription lapses.

## Integrations

- Payment provider — Stripe, via Ticket Tailor. Test keys verified working; live keys need the client's legal entity
- Accounting system — undecided by the client, nothing built
- Full SEO starter package — foundation done, submissions and content plan outstanding
- Webshop + events live by end of September — blocked on the client supplying event details

---

## The gap, stated plainly

Everything a **visitor** touches is built and working. Almost nothing the
**client** touches exists. They cannot add an event, edit a page, see their
signups in one place, or manage participants — except in Ticket Tailor, which
covers events, tickets, waitlists and participants but not site content.

That asymmetry is the whole reason for the CMS.

---

## Two client obligations that are not yours but affect what you build

1. **Parental consent for the minors on camera.** Four participant video clips
   are on the homepage. Written consent per clip had not been provided as of
   9 September. If it never arrives the clips come down. Do not design a feature
   that assumes they stay.

2. **Privacy policy and terms.** The text had not been supplied. `/privacy`
   ships with `[ bracketed ]` placeholders. The forms link to it for consent, so
   this is a legal dependency, not a content one. `PRIVACY-INVENTORY.md` in the
   original repo enumerates every field the site collects, written for their
   lawyer.
