// @ts-check
import { defineConfig } from 'astro/config';
import netlify from '@astrojs/netlify';

export default defineConfig({
  site: 'https://www.wemakeimpact.be',
  adapter: netlify(),
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
