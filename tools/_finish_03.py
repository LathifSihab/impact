"""Close the remaining doc 03 reworks in site/.

1. event-row becomes two separate links, as the hi-fi specified: the row goes to
   the event, the waitlist pill is its own target at the form anchor.
2. Middle-dot meta strings become separate meta cells (01 stop list).
"""
import pathlib
import re

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

ROW = re.compile(r'<a class="event-row" href="([^"]+)">(.*?)\n    </a>', re.S)


def restructure(html: str) -> tuple[str, int]:
    count = 0

    def one(m: re.Match) -> str:
        nonlocal count
        count += 1
        href, inner = m.group(1), m.group(2)

        # lift the CTA out of the row's anchor and make it a real link
        cta = re.search(r'<div class="cta">(.*?)</div>', inner, re.S)
        cta_html = ''
        if cta:
            body = cta.group(1)
            label = re.search(r'<span class="pill[^"]*">([^<]+)</span>', body)
            status = re.search(r'<span class="status">([^<]+)</span>', body)
            target = f'{href}#wachtlijst' if href.endswith('event.html') else href
            cta_html = (
                '\n      <div class="cta">'
                f'\n        <a class="pill pill--secondary pill--sm" href="{target}">'
                f'{label.group(1) if label else "Bekijk"}</a>'
                + (f'\n        <span class="status">{status.group(1)}</span>' if status else '')
                + '\n      </div>'
            )
            inner = inner.replace(cta.group(0), '').rstrip()

        # "Camp · 5 dagen" is two facts, not one string
        def split_tag(t: re.Match) -> str:
            parts = [p.strip() for p in t.group(1).split('·')]
            if len(parts) == 1:
                return t.group(0)
            return ('<span class="tag">%s</span><span class="tag tag--dim">%s</span>'
                    % (parts[0], ' '.join(parts[1:])))
        inner = re.sub(r'<span class="tag">([^<]+)</span>', split_tag, inner)

        return (f'<div class="event-row">\n      '
                f'<a class="event-row-main" href="{href}">{inner}\n      </a>'
                f'{cta_html}\n    </div>')

    return ROW.sub(one, html), count


for name in ('index.html', 'events.html'):
    p = SITE / name
    html = p.read_text(encoding='utf8')
    out, n = restructure(html)
    p.write_text(out, encoding='utf8')
    print(f'  {name}: {n} rows restructured')

# the event page meta bar carried the same joined string
p = SITE / 'event.html'
t = p.read_text(encoding='utf8')
t = t.replace('<div><div class="k">Format</div><div class="v">Camp · 5 dagen</div></div>',
              '<div><div class="k">Format</div><div class="v">Camp</div></div>\n'
              '      <div><div class="k">Duur</div><div class="v">5 dagen</div></div>')
t = t.replace('<div class="row"><span>Format</span><span>Camp · 5 dagen</span></div>',
              '<div class="row"><span>Format</span><span>Camp</span></div>\n'
              '        <div class="row"><span>Duur</span><span>5 dagen</span></div>')
p.write_text(t, encoding='utf8')
print('  event.html: meta bar split')

# any leftovers in the overview table and format meta
for name in ('events.html', 'index.html', 'journal.html'):
    p = SITE / name
    t = p.read_text(encoding='utf8')
    t = t.replace('<span class="tag">Day · scholen</span>',
                  '<span class="tag">Day</span><span class="tag tag--dim">Scholen</span>')
    t = t.replace('Recap · aftermovie', 'Recap, met aftermovie')
    t = t.replace('Expert content · fundament 03', 'Expert content, fundament 03')
    t = t.replace('Hosted Experience</p>', 'Hosted Experience</p>')
    p.write_text(t, encoding='utf8')

css = SITE / 'assets/css/style.css'
s = css.read_text(encoding='utf8')

s = s.replace(
    """.event-row{display:grid;grid-template-columns:200px 1fr 220px 150px 230px;gap:32px;align-items:center;
  padding:30px 0;border-top:1px solid var(--border);transition:background var(--dur-fast) var(--ease)}""",
    """/* Two targets, not a nested anchor: the row is one link, the waitlist pill is
   another. Same visual grid as before, split across two elements. */
.event-row{display:grid;grid-template-columns:1fr 230px;gap:32px;align-items:center;
  padding:30px 0;border-top:1px solid var(--border);transition:background var(--dur-fast) var(--ease)}
.event-row-main{display:grid;grid-template-columns:200px 1fr 220px 150px;gap:32px;align-items:center}
.tag--dim{color:var(--grey-warm);margin-left:12px}""")

s = s.replace("""  .event-row{grid-template-columns:160px 1fr 180px}
  .event-row .age{display:none}
  .event-row .cta{grid-column:1/-1;text-align:left}""",
              """  .event-row{grid-template-columns:1fr}
  .event-row-main{grid-template-columns:160px 1fr 180px}
  .event-row .age{display:none}
  .event-row .cta{text-align:left}""")

s = s.replace("""  .event-row{grid-template-columns:1fr;gap:14px}
  .event-row .cta .pill{width:100%}""",
              """  .event-row,.event-row-main{grid-template-columns:1fr;gap:14px}
  .event-row .cta .pill{width:100%}""")
css.write_text(s, encoding='utf8')
print('  css: event-row split into row + cta')
