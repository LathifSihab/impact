# reference/ — source files, not documentation

| File | Why it is here |
|---|---|
| `content.config.ts` | **The data model.** Ten Zod schemas with every field and relationship. Start here, not from the HTML |
| `content/` | The real content: 4 events, 4 journal posts, partners, experts, formats, foundations, age groups, tiers, figures. Seed from this |
| `subscribe.mjs` | The live newsletter/waitlist endpoint. Read for the Brevo contract and the validation rules |
| `tt-webhook.mjs` | The live Ticket Tailor webhook, including signature verification and the replay guard |
| `noindex.ts` | Edge function keeping every non-production host out of the search index |
| `i18n-en.json` | 912 Dutch→English strings. This is how the site is bilingual |
| `env.example.txt` | Variable names and what each is for. **No values** |

`testimonials.json` is `[]` on purpose — no parent consent is held. Do not
invent quotes to fill it.
