"""Injects the shared utility bar + nav + mobile menu and the footer into every page
in site/, between the <!--NAV--> / <!--/NAV--> and <!--FOOTER--> / <!--/FOOTER--> markers.

Run after editing the templates below:  python tools/inject.py
Every page reads `<body data-nav="...">` to mark the active main-nav item.
"""
import pathlib
import re

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

NAV = """
<!-- utility bar -->
<div class="util">
  <div class="wrap">
    <ul>
      <li><a href="assets/impact-brochure.pdf" target="_blank" rel="noopener">Brochure</a></li>
      <li><a href="media.html"{a_media}>Media</a></li>
      <li><a href="journal.html"{a_journal}>Journal</a></li>
      <li><a href="contact.html"{a_contact}>Contact</a></li>
    </ul>
    <div class="right">
      <a href="#">IG</a><a href="#">LI</a><a href="#">TT</a>
      <span class="divider"></span>
      <a href="#" class="is-active">NL</a><a href="#">EN</a>
    </div>
  </div>
</div>

<!-- main nav -->
<nav class="nav">
  <div class="wrap">
    <a href="index.html" class="logo" aria-label="IMPACT — home">
      <img src="assets/brand/impact-logo.png" alt="IMPACT" width="647" height="145">
    </a>
    <ul class="nav-main">
      <li{c_over}><a href="over.html" class="top">Over</a>
        <div class="dropdown">
          <a href="over.html#founders">Founders</a>
          <a href="over.html#fundamenten">Onze fundamenten</a>
          <a href="over.html#voor-wie">Voor wie</a>
          <a href="over.html#team">Team &amp; experts</a>
        </div>
      </li>
      <li{c_events}><a href="events.html" class="top">Events</a>
        <div class="dropdown">
          <a href="events.html#upcoming">Upcoming Events</a>
          <a href="events.html#camps">Camps</a>
          <a href="events.html#days">Days</a>
          <a href="events.html#retreats">Retreats</a>
          <a href="hosted-experiences.html">Hosted Experiences</a>
          <a href="events.html#alle">Alle events</a>
        </div>
      </li>
      <li{c_samenwerken}><a href="samenwerken.html" class="top">Samenwerken</a>
        <div class="dropdown">
          <a href="samenwerken.html#partner-worden">Partner worden</a>
          <a href="hosted-experiences.html">Hosted Experiences</a>
          <a href="samenwerken.html#experts">Experts &amp; coaches</a>
          <a href="samenwerken.html#bedrijven">Voor bedrijven</a>
          <a href="samenwerken.html#partners">Onze partners</a>
        </div>
      </li>
      <li{c_social}><a href="social-impact.html" class="top">Social Impact</a>
        <div class="dropdown">
          <a href="social-impact.html">IMPACT FOR ALL</a>
          <a href="social-impact.html#aanpak">Onze aanpak</a>
          <a href="social-impact.html#impact">Onze impact</a>
          <a href="social-impact.html#draag-bij">Steun onze missie</a>
        </div>
      </li>
    </ul>
    <a href="events.html#upcoming" class="pill pill--primary pill--sm">UPCOMING EVENTS</a>
    <button class="burger" aria-label="Menu openen"><span></span></button>
  </div>
</nav>

<div class="mobile-menu" id="mobile-menu">
  <div class="mm-top">
    <a href="index.html" class="logo logo--invert">
      <img src="assets/brand/impact-logo.png" alt="IMPACT" width="647" height="145">
    </a>
    <button class="close" aria-label="Menu sluiten">&times;</button>
  </div>
  <a class="mm-item" href="over.html">Over</a>
  <div class="mm-sub">
    <a href="over.html#founders">Founders</a><a href="over.html#fundamenten">Onze fundamenten</a>
    <a href="over.html#voor-wie">Voor wie</a><a href="over.html#team">Team &amp; experts</a>
  </div>
  <a class="mm-item" href="events.html">Events</a>
  <div class="mm-sub">
    <a href="events.html#upcoming">Upcoming Events</a><a href="events.html#camps">Camps</a>
    <a href="events.html#days">Days</a><a href="events.html#retreats">Retreats</a>
    <a href="hosted-experiences.html">Hosted Experiences</a><a href="events.html#alle">Alle events</a>
  </div>
  <a class="mm-item" href="samenwerken.html">Samenwerken</a>
  <div class="mm-sub">
    <a href="samenwerken.html#partner-worden">Partner worden</a><a href="hosted-experiences.html">Hosted Experiences</a>
    <a href="samenwerken.html#experts">Experts &amp; coaches</a><a href="samenwerken.html#bedrijven">Voor bedrijven</a>
    <a href="samenwerken.html#partners">Onze partners</a>
  </div>
  <a class="mm-item" href="social-impact.html">Social Impact</a>
  <div class="mm-sub">
    <a href="social-impact.html#aanpak">Onze aanpak</a><a href="social-impact.html#impact">Onze impact</a>
    <a href="social-impact.html#draag-bij">Steun onze missie</a>
  </div>
  <div class="mm-foot">
    <a href="assets/impact-brochure.pdf" target="_blank" rel="noopener">Brochure</a>
    <a href="media.html">Media</a><a href="journal.html">Journal</a><a href="contact.html">Contact</a>
    <a href="#">IG</a><a href="#">LI</a><a href="#">TT</a>
  </div>
</div>
"""

FOOTER = """
<footer class="footer">
  <div class="wrap">
    <div class="grid">
      <div class="brandcol">
        <a href="index.html" class="logo logo--invert">
          <img src="assets/brand/impact-logo.png" alt="IMPACT" width="647" height="145">
        </a>
        <p class="body">Youth development through experiences, connection and growth.</p>
        <div class="socials"><a href="#">Instagram</a><a href="#">LinkedIn</a><a href="#">TikTok</a></div>
      </div>
      <div><h4>IMPACT</h4><ul>
        <li><a href="over.html">Over</a></li>
        <li><a href="over.html#fundamenten">Fundamenten</a></li>
        <li><a href="over.html#team">Team</a></li>
      </ul></div>
      <div><h4>Events</h4><ul>
        <li><a href="events.html#upcoming">Upcoming</a></li>
        <li><a href="events.html#camps">Camps</a></li>
        <li><a href="events.html#days">Days</a></li>
        <li><a href="events.html#retreats">Retreats</a></li>
        <li><a href="hosted-experiences.html">Hosted Experiences</a></li>
      </ul></div>
      <div><h4>Samenwerken</h4><ul>
        <li><a href="samenwerken.html#partner-worden">Partner worden</a></li>
        <li><a href="hosted-experiences.html">Hosted Experiences</a></li>
        <li><a href="samenwerken.html#bedrijven">Voor bedrijven</a></li>
      </ul></div>
      <div><h4>Social impact</h4><ul>
        <li><a href="social-impact.html">IMPACT FOR ALL</a></li>
        <li><a href="social-impact.html#draag-bij">Steun onze missie</a></li>
      </ul></div>
      <div><h4>Info</h4><ul>
        <li><a href="journal.html">Journal</a></li>
        <li><a href="media.html">Media</a></li>
        <li><a href="assets/impact-brochure.pdf" target="_blank" rel="noopener">Brochure</a></li>
        <li><a href="contact.html">Contact</a></li>
      </ul></div>
    </div>
    <div class="bottom">
      <span>hello@wemakeimpact.be · +32 495 37 00 44 · @impact___collective</span>
      <span><a href="#">Privacy</a> · <a href="#">Algemene voorwaarden</a></span>
    </div>
  </div>
</footer>
"""

ACTIVE = ' class="is-active"'


def nav_for(page):
    fields = {k: "" for k in ("c_over", "c_events", "c_samenwerken", "c_social",
                              "a_media", "a_journal", "a_contact")}
    main = {"over": "c_over", "events": "c_events", "samenwerken": "c_samenwerken",
            "social": "c_social"}.get(page)
    if main:
        fields[main] = ' class="is-current"'
    util = {"media": "a_media", "journal": "a_journal", "contact": "a_contact"}.get(page)
    if util:
        fields[util] = ACTIVE
    return NAV.format(**fields)


def inject(path):
    html = path.read_text(encoding="utf8")
    page = re.search(r'<body[^>]*data-nav="([^"]*)"', html)
    page = page.group(1) if page else ""
    out, n = html, 0
    for marker, block in (("NAV", nav_for(page)), ("FOOTER", FOOTER)):
        pattern = re.compile(r"<!--%s-->.*?<!--/%s-->" % (marker, marker), re.S)
        if pattern.search(out):
            out = pattern.sub("<!--%s-->%s<!--/%s-->" % (marker, block, marker), out)
            n += 1
    if out != html:
        path.write_text(out, encoding="utf8")
    return n


if __name__ == "__main__":
    for f in sorted(SITE.glob("*.html")):
        print(f.name, "->", inject(f), "blocks")
