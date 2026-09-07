/**
 * The head contract, ported from tools/seo.py so the static site and the Astro
 * build emit identical metadata. One place to change titles, descriptions and
 * structured data.
 */
export const SITE_URL = 'https://www.wemakeimpact.be';
export const SITE_NAME = 'IMPACT';
export const LOCALE = 'nl_BE';
export const OG_IMAGE = '/assets/img/court-169.jpg'; // replace with a 1200x630 share image

export const ORGANISATION = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  name: 'IMPACT',
  alternateName: 'IMPACT Collective Antwerp',
  url: SITE_URL + '/',
  logo: SITE_URL + '/assets/brand/impact-logo.png',
  description:
    'Youth development brand voor jongeren van 8 tot 25 jaar. Camps, Days, Retreats, Community en Hosted Experiences rond zes fundamenten.',
  email: 'hello@wemakeimpact.be',
  telephone: '+32495370044',
  areaServed: 'BE',
  address: { '@type': 'PostalAddress', addressCountry: 'BE', addressLocality: 'Antwerpen' },
  sameAs: ['https://www.instagram.com/impact___collective/'],
  founder: [
    { '@type': 'Person', name: 'Mirte Rens' },
    { '@type': 'Person', name: 'Jean-Marc Mwema' },
  ],
};

export const WEBSITE = {
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  name: SITE_NAME,
  url: SITE_URL + '/',
  inLanguage: ['nl-BE', 'en'],
};

export function breadcrumb(name: string, path: string) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home', item: SITE_URL + '/' },
      { '@type': 'ListItem', position: 2, name, item: SITE_URL + path },
    ],
  };
}

type EventInput = {
  title: string;
  standfirst: string;
  dateStart?: Date;
  dateText: string;
  location: string;
  ageMin: number;
  ageMax: number;
  status: 'waitlist' | 'open' | 'full' | 'past';
  heroImage: string;
  price?: string;
  slug: string;
};

/** Event + Offer, driven by the CMS record rather than hand-written per page. */
export function eventLd(e: EventInput) {
  const url = `${SITE_URL}/events/${e.slug}`;
  const availability = {
    waitlist: 'https://schema.org/PreOrder',
    open: 'https://schema.org/InStock',
    full: 'https://schema.org/SoldOut',
    past: 'https://schema.org/SoldOut',
  }[e.status];
  return {
    '@context': 'https://schema.org',
    '@type': 'Event',
    name: e.title,
    description: e.standfirst,
    eventStatus: e.status === 'past'
      ? 'https://schema.org/EventScheduled'
      : 'https://schema.org/EventScheduled',
    eventAttendanceMode: 'https://schema.org/OfflineEventAttendanceMode',
    startDate: e.dateStart ? e.dateStart.toISOString().slice(0, 10) : undefined,
    location: {
      '@type': 'Place',
      name: e.location,
      address: { '@type': 'PostalAddress', addressLocality: e.location, addressCountry: 'BE' },
    },
    organizer: { '@type': 'Organization', name: 'IMPACT', url: SITE_URL + '/' },
    typicalAgeRange: `${e.ageMin}-${e.ageMax}`,
    image: SITE_URL + '/' + e.heroImage.replace(/^\//, ''),
    offers: {
      '@type': 'Offer',
      url: url + '#wachtlijst',
      availability,
      description: e.price ?? 'Prijs volgt bij bevestiging',
    },
  };
}

/** FAQPage, only when the event actually has answered questions. */
export function faqLd(faq: { q: string; a: string }[]) {
  if (!faq?.length) return null;
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faq.map((f) => ({
      '@type': 'Question',
      name: f.q,
      acceptedAnswer: { '@type': 'Answer', text: f.a },
    })),
  };
}
