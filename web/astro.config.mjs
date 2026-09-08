// @ts-check
import { defineConfig } from 'astro/config';
import netlify from '@astrojs/netlify';

// `astro dev` runs plain Vite; the Netlify adapter is only attached for builds,
// because its local edge-function bridge needs the Netlify CLI and breaks
// `npm run dev` without it. API routes still work in dev via Astro's own server.
const isDev = process.argv.includes('dev');

export default defineConfig({
  site: 'https://www.wemakeimpact.be',
  ...(isDev ? {} : { adapter: netlify({ imageCDN: false }) }),
  // Pages are static; only the form endpoints run on demand (prerender = false).
  output: 'static',
  i18n: {
    defaultLocale: 'nl',
    locales: ['nl', 'en'],
    routing: { prefixDefaultLocale: false, redirectToDefaultLocale: true },
  },
  image: { responsiveStyles: true },
  build: { inlineStylesheets: 'auto' },
});
