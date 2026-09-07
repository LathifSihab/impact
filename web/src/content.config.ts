import { defineCollection, reference, z } from 'astro:content';
import { glob, file } from 'astro/loaders';

/* The shapes here mirror the Payload models in brief/docs/04-ARCHITECTURE.md §2.
   When Payload goes live the loaders swap to its REST API and the schemas —
   and therefore every component — stay exactly as they are. */

const localised = { locale: z.enum(['nl', 'en']).default('nl') };

const events = defineCollection({
  loader: glob({ pattern: '**/*.json', base: './src/content/events' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      format: reference('formats'),
      editionYear: z.number(),
      dateText: z.string(),                       // "Juli 2027" or "Datum volgt"
      dateStart: z.coerce.date().optional(),
      dateEnd: z.coerce.date().optional(),
      location: z.string(),
      ageMin: z.number(),
      ageMax: z.number(),
      price: z.string().optional(),
      capacity: z.number().optional(),
      status: z.enum(['waitlist', 'open', 'full', 'past']),
      standfirst: z.string(),
      intro: z.string(),
      heroImage: z.string(),
      heroVideo: z.string().optional(),
      gallery: z.array(z.object({ src: z.string(), alt: z.string() })).default([]),
      programmeDays: z.array(z.object({ day: z.string(), title: z.string(), body: z.string() })).default([]),
      foundations: z.array(reference('foundations')).default([]),
      experts: z.array(reference('experts')).default([]),
      partners: z.array(reference('partners')).default([]),
      faq: z.array(z.object({ q: z.string(), a: z.string() })).default([]),
      practical: z.array(z.object({ k: z.string(), v: z.string() })).default([]),
      seo: z.object({ title: z.string(), description: z.string() }),
      ...localised,
    }),
});

const formats = defineCollection({
  loader: file('./src/content/formats.json'),
  schema: z.object({
    name: z.string(),
    bracketName: z.string(),
    description: z.string(),
    meta: z.string(),
    order: z.number(),
    isHosted: z.boolean().default(false),
    body: z.string().optional(),
    image: z.string().optional(),
    ticks: z.array(z.string()).default([]),
  }),
});

const foundations = defineCollection({
  loader: file('./src/content/foundations.json'),
  schema: z.object({
    number: z.string(),
    name: z.string(),
    enOneLiner: z.string(),
    nlBody: z.string(),
    workOn: z.array(z.string()).default([]),
    image: z.string(),
    alt: z.string(),
  }),
});

const ageGroups = defineCollection({
  loader: file('./src/content/age-groups.json'),
  schema: z.object({
    label: z.string(),
    tagline: z.string(),
    body: z.string(),
    formats: z.array(z.string()).default([]),
    image: z.string(),
    alt: z.string(),
  }),
});

const experts = defineCollection({
  loader: file('./src/content/experts.json'),
  schema: z.object({
    name: z.string(),
    org: z.string(),
    bio: z.string().optional(),
    foundations: z.array(z.string()).default([]),
    portrait: z.string().optional(),
    confirmed: z.boolean().default(false),   // published only once IMPACT confirms
  }),
});

const partners = defineCollection({
  loader: file('./src/content/partners.json'),
  schema: z.object({
    name: z.string(),
    logo: z.string(),
    url: z.string().url(),
    tier: z.string().optional(),
    isHost: z.boolean().default(false),
  }),
});

const tiers = defineCollection({
  loader: file('./src/content/tiers.json'),
  schema: z.object({
    name: z.string(),
    investmentFrom: z.string(),
    order: z.number(),
    benefits: z.array(z.string()).default([]),
  }),
});

const figures = defineCollection({
  loader: file('./src/content/figures.json'),
  schema: z.object({
    value: z.number(),
    display: z.string(),
    suffix: z.string().optional(),
    label: z.string(),
    explanation: z.string().optional(),
    period: z.string(),
    group: z.enum(['forAll', 'reach']),
    confirmed: z.boolean().default(false),
  }),
});

const journal = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/journal' }),
  schema: z.object({
    category: z.enum(['past-event', 'story', 'insight', 'social', 'partner', 'news']),
    title: z.string(),
    image: z.string(),
    alt: z.string(),
    meta: z.string(),
    publishedAt: z.coerce.date(),
    relatedEvent: reference('events').optional(),
    ...localised,
  }),
});

const testimonials = defineCollection({
  loader: file('./src/content/testimonials.json'),
  schema: z.object({
    quote: z.string(),
    attribution: z.string(),
    edition: z.string(),
    consentOnFile: z.boolean(),      // nothing renders without this true
  }),
});

export const collections = {
  events, formats, foundations, ageGroups, experts, partners, tiers, figures, journal, testimonials,
};
