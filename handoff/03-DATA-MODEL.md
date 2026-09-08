# Data model — ten content types, ready for Postgres

Source of truth: `reference/content.config.ts`. Every field below is taken from
that file, which validates the real content in `reference/content/`. Sample data
for each type is in that folder, so you can seed from it directly.

`locale` is `'nl' | 'en'`, default `'nl'`, on the two types that carry prose.

---

## events — the important one

Four real records in `reference/content/events/`.

| Field | Type | Notes |
|---|---|---|
| `title` | text | |
| `format` | ref → formats | |
| `editionYear` | int | |
| `dateText` | text | Human string: "Juli 2027" or "Datum volgt". **Kept separate from the real dates on purpose** — an edition often has no confirmed date yet, and the page still has to say something honest |
| `dateStart`, `dateEnd` | date, optional | |
| `location` | text | |
| `ageMin`, `ageMax` | int | Sent with the waitlist form and re-checked server-side |
| `price` | text, optional | Text, not a number — real values include "Volgt bij bevestiging" |
| `capacity` | int, optional | |
| `status` | enum | `waitlist` \| `open` \| `full` \| `past`. The page branches on this |
| `standfirst` | text | One-paragraph lead |
| `intro` | text | |
| `heroImage` | text path | |
| `heroVideo` | text path, optional | |
| `gallery` | array of `{src, alt}` | |
| `programmeDays` | array of `{day, title, body}` | |
| `foundations` | array of refs → foundations | |
| `experts` | array of refs → experts | |
| `partners` | array of refs → partners | |
| `faq` | array of `{q, a}` | |
| `practical` | array of `{k, v}` | Key/value rows in the sidebar |
| `seo` | `{title, description}` | |

**`status` drives behaviour, not just display.** `waitlist` shows the waitlist
form; `open` should show a purchase route; `full` and `past` neither. The
"registration opened" email is meant to fire when this flips to `open`.

## formats
`name`, `bracketName`, `description`, `meta`, `order` int, `isHosted` bool,
`body?`, `image?`, `ticks[]`

## foundations
The six pillars. `number`, `name`, `enOneLiner`, `nlBody`, `workOn[]`, `image`, `alt`

## ageGroups
`label`, `tagline`, `body`, `formats[]`, `image`, `alt`

## experts
`name`, `org`, `bio?`, `foundations[]`, `portrait?`, **`confirmed` bool — nothing
publishes until the client confirms the person may be named**

## partners
`name`, `logo`, `url`, `tier?`, `isHost` bool

## tiers
Partnership levels. `name`, `investmentFrom`, `order`, `benefits[]`

## figures
`value` number, `display` text, `suffix?`, `label`, `explanation?`, `period`,
`group` enum `forAll | reach`, **`confirmed` bool**

## journal
Markdown, four real posts. `category` enum
(`past-event | story | insight | social | partner | news`), `title`, `image`,
`alt`, `meta`, `publishedAt` date, `relatedEvent?` ref → events, `locale`

## testimonials
`quote`, `attribution`, `edition`, **`consentOnFile` bool — nothing renders
without it true.** The file is currently `[]` because no consent is held.

---

## Three patterns to carry into the schema

**`confirmed` / `consentOnFile` booleans are not soft-delete flags.** They mean
"a human has verified we are allowed to publish this". Experts are real named
people; testimonials quote parents; figures are claims about outcomes. Default
them to `false` and make the CMS require an explicit tick, because the cost of a
wrong `true` is a person's name published without permission.

**Free text where a type would be neater.** `price` and `dateText` are strings
because reality is "Volgt bij bevestiging". Resist normalising them into
`numeric` and `date` unless you keep a display field alongside.

**References, not embedding.** Events point at foundations, experts and partners
by id. Those are shared across events and edited independently — foreign keys,
join tables for the arrays.

---

## What is *not* in this model, and must not be added to it

**Registrations, orders, tickets, payments and participants.** They live in
Ticket Tailor. It holds the money, the PCI scope, refunds, VAT invoices, the
attendee list and door scanning. Modelling them again gives you two systems that
both believe they own an order.

The one thing worth building later is a **read-only joined view** — signups from
Brevo, orders from Ticket Tailor, attribution from your own data, in one screen.
That is genuinely missing and no off-the-shelf tool provides it. It is a
reporting problem, not an ownership one.

---

## Suggested table sketch

```sql
create table events (
  id            text primary key,          -- slug, e.g. camp-basketball-edition-2027
  title         text not null,
  format_id     text references formats(id),
  edition_year  int  not null,
  date_text     text not null,
  date_start    date, date_end date,
  location      text not null,
  age_min       int  not null, age_max int not null,
  price         text, capacity int,
  status        text not null check (status in ('waitlist','open','full','past')),
  standfirst    text not null, intro text not null,
  hero_image    text not null, hero_video text,
  gallery       jsonb not null default '[]',
  programme_days jsonb not null default '[]',
  faq           jsonb not null default '[]',
  practical     jsonb not null default '[]',
  seo           jsonb not null,
  locale        text not null default 'nl',
  updated_at    timestamptz not null default now()
);
-- events_foundations, events_experts, events_partners as join tables
```

`jsonb` for the ordered arrays of small objects is a deliberate simplification:
they are always read and written whole, always belong to exactly one event, and
have no independent identity. Separate tables would buy nothing and cost joins.
The three cross-type relationships are real foreign keys because those records
are shared and edited on their own.
