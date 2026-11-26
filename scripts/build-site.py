#!/usr/bin/env python3
"""Build the Aikhoje Studios wedding site (Evergreen design, v2).

Generates, from the data in this folder:
  index.html                     homepage
  gallery/index.html             full gallery with filters
  <area>-wedding-photographer/   six location pages
  404.html, sitemap.xml, and the engagements/ and family/ redirects

Shared look and behaviour live in /css/evergreen.css and /js/site.js.
Data: scripts/photos.json (every gallery photo: alt text, size, categories),
scripts/business.json (structured data), scripts/faq.json (questions + answers),
and AREAS below (location page copy).

Edit the data or templates here, then run:

    python3 scripts/build-site.py

and commit everything it writes. /real-estate/ and /studio/ are separate and not touched.
"""
import html
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
SITE = "https://aikhojestudios.com"
TODAY = "2026-11-24"
YEAR = "2026"
EMAIL = "aikhojestudios@gmail.com"
# Google Apps Script web app that emails inquiries from the studio Gmail and logs them to a Sheet
# (see scripts/inquiry-apps-script.gs). Every site form posts here; it runs the spam filter and sends the auto-reply.
FORM_ENDPOINT = "https://script.google.com/macros/s/AKfycbzXs5tRDZtOgf0inEaoASbIggt1pdCpdmecaGwiDWfbaV5UC27YLhSe--WmG1gX-Ac39w/exec"
PHONE = "+15087628168"
PHONE_SHOWN = "(508) 762-8168"

PHOTOS = json.loads((HERE / "photos.json").read_text())
BUSINESS = json.loads((HERE / "business.json").read_text())
FAQ = json.loads((HERE / "faq.json").read_text())

# Title-page covers: one is chosen at random on each visit (js below). The first is the no-JS fallback.
COVERS = [
    ("cover-01", "A couple in autumn woods, seen through the leaves"),
    ("cover-02", "A bride and groom looking into a gilded mirror at night"),
    ("cover-03", "A bride in lace and a long veil by a tall window and gilt mirror"),
    ("cover-04", "A bride with an orchid bouquet on church steps, in black and white"),
    ("cover-05", "A couple kissing in a sunlit vineyard, on film"),
    ("cover-06", "A smiling bride holding her bouquet on a tree-lined path"),
    ("cover-07", "A couple embracing forehead to forehead in a forest"),
    ("cover-08", "A bride seen from behind, veil and bouquet, beneath old trees"),
    ("cover-09", "A couple at golden hour above autumn hills"),
]

REVIEWS = [
    {
        "img": "review-martin", "alt": "Newlyweds embracing under a leafy tree after their intimate wedding",
        "quote": "When my wife and I needed a wedding photographer for our small intimate ceremony, we reached out to Aikhoje Studios and couldn’t have been happier. They were incredibly professional from the very first conversation. Communication was clear and responsive, they were organized and on time, and they made the whole process easy. On the day, they were calm and respectful, and they knew exactly how to work in an intimate setting without taking over. It’s rare to find someone this skilled who is also this great to work with. Highly recommend!",
        "who": "Martin G.", "what": "Intimate wedding",
    },
    {
        "img": "review-ohenewaa-bts", "alt": "Behind the scenes: bride and groom posing in a hotel lounge under a studio light",
        "quote": "Beyond pleased with the photography services provided for my wedding! So professional, timely and my pictures were stunning.",
        "who": "Ohenewaa", "what": "Wedding",
    },
    {
        "img": "review-newf-booth", "alt": "Bride in a lace veil stepping out of a pink telephone booth",
        "quote": "We’ve worked with them several times for both photo and video shoots, and every time has been a great experience. They’re professional, easy to coordinate with, and the results are always top-notch. Highly recommend!",
        "who": "New England Wedding Film", "what": "Fellow wedding vendor",
    },
]

FILTERS = [
    ("all", "All"),
    ("ready", "Getting ready"),
    ("portraits", "Portraits"),
    ("ceremony", "Ceremony & celebration"),
    ("details", "Details"),
    ("bw", "Black & white"),
    ("film", "Shot on film"),
]

# Order of the full gallery (every photo in photos.json appears once).
GALLERY_ORDER = [
    "window-bride-veil", "196", "dscf0309", "flower-girls-yellow-roses", "film-beach-kiss-bw", "untitled-23", "vineyard-kiss-closeup",
    "dscf0031", "dscf0552-2", "trix400_2017-08-22-0020", "mirror-steps", "film-hands-color", "7",
    "petals-getting-ready", "altar-portrait", "dscf0604", "untitled-31", "film-couple-mountains", "dscf0500",
    "dscf0048", "church-steps-bw", "pink-phone-booth", "wedding-380", "untitled-84-2", "aw-197",
    "0-104", "film-bride-bouquet", "20191019-dscf0491", "film-under-veil", "vintage-car", "petals-celebration",
    "night-veil-bw", "dscf0486", "signal-2022-10-03-162349_002", "phone-booth-bw", "dscf0559", "8",
    "untitled-32", "film-beach-couple", "dscf0614-2", "aw-190", "36", "0-1", "dscf0084", "20191019-dscf0340",
    "film-mountain-overlook", "4", "118", "dscf0427", "9344835903_50e22f1f0e_o", "film-couple-steps",
    "dscf0497-2", "aw-146", "311", "dscf0599",
]

AREAS = [
    {
        "slug": "outer-banks-wedding-photographer",
        "name": "Outer Banks",
        "region": "Outer Banks, North Carolina",
        "title": "Outer Banks Wedding Photographer & Film | Aikhoje Studios",
        "desc": "Outer Banks wedding photography and film by Aikhoje Studios. Beach ceremonies, soundside elopements and celebrations from Corolla to Hatteras. Editorial, documentary, since 2015.",
        "hero": "film-beach-couple",
        "hero_sub": "Beach ceremonies, soundside elopements, and barefoot receptions, from Corolla to Hatteras.",
        "intro_h": "Wind, salt,<br>and golden light.",
        "intro": [
            "The Outer Banks are made for weddings that feel free. Ceremonies on the sand in Duck or Nags Head, intimate vows on a soundside dock in Corolla, big beach-house weekends where the whole family stays under one roof. I photograph and film them the way they actually feel: windswept, sun-drenched, and a little bit wild.",
            "My approach is editorial and documentary. I guide portraits when you want direction, then step back and let the day unfold, so your gallery holds the real moments as much as the posed ones.",
        ],
        "intro_img": "dscf0559",
        "notes_h": "Planning an Outer Banks wedding.",
        "notes_copy": "A few things I talk through with every Outer Banks couple.",
        "notes": [
            ("Sound side vs. ocean side", "The ocean faces east, so sunset light is softest on the sound side. Many couples hold the ceremony on the beach and take portraits by the sound at golden hour."),
            ("Plan for the wind", "There is almost always a breeze off the water. Veils, hair, and florals look beautiful in it when you plan for it, and I build time into the day for it."),
            ("Beach ceremony permits", "Each Outer Banks town sets its own rules for beach weddings. Check with your town, rental company, or planner early; I am happy to help you think through timing."),
            ("Beach-house weddings", "Rental-home celebrations are an Outer Banks tradition. I photograph getting ready, the ceremony, and the reception all in one place, which leaves more time for portraits."),
        ],
        "gallery": ["film-beach-couple", "film-beach-kiss-bw", "dscf0559", "untitled-84-2", "dscf0497-2", "118", "dscf0486", "aw-190", "dscf0604", "film-hands-color", "8", "dscf0614-2"],
    },
    {
        "slug": "virginia-beach-wedding-photographer",
        "name": "Virginia Beach & Hampton Roads",
        "region": "Virginia Beach and Hampton Roads, Virginia",
        "title": "Virginia Beach Wedding Photographer & Film | Aikhoje Studios",
        "desc": "Virginia Beach and Hampton Roads wedding photography and film by Aikhoje Studios. Oceanfront, Chesapeake Bay, Norfolk and military weddings. Editorial and documentary, since 2015.",
        "hero": "film-beach-kiss-bw",
        "hero_sub": "Oceanfront ceremonies, Chesapeake Bay sunsets, and city celebrations across Hampton Roads.",
        "intro_h": "Ocean, bay,<br>and city.",
        "intro": [
            "Hampton Roads gives couples every kind of backdrop within a short drive: the Virginia Beach oceanfront, quieter sand at Sandbridge, Chesapeake Bay beaches where the sun sets over the water, and the historic streets and gardens of Norfolk.",
            "I photograph and film weddings across Virginia Beach, Norfolk, Chesapeake, Suffolk, and Hampton with an editorial eye and a documentary heart. Many couples here are military families, and I plan around tight schedules, deployments, and dress uniforms with care.",
        ],
        "intro_img": "36",
        "notes_h": "Planning a Hampton Roads wedding.",
        "notes_copy": "A few things I talk through with couples marrying in Virginia Beach and the surrounding cities.",
        "notes": [
            ("Bay-side sunsets", "The oceanfront faces east, but Chesapeake Bay beaches face north and west, so sunset portraits there can glow over the water."),
            ("Military weddings", "Saber arches, dress uniforms, and families flying in on short notice. I keep the timeline flexible and make sure the traditions are covered."),
            ("City and coast in one day", "Getting ready downtown and portraits on the sand are an easy pairing here. I plan travel time between locations into your timeline."),
            ("Peak season", "Summer weekends at the oceanfront are busy. Early-morning or weekday sessions give you open beaches and soft light."),
        ],
        "gallery": ["film-beach-kiss-bw", "36", "film-beach-couple", "dscf0604", "wedding-380", "118", "aw-197", "dscf0614-2", "8", "311", "dscf0048", "196"],
    },
    {
        "slug": "williamsburg-wedding-photographer",
        "name": "Williamsburg",
        "region": "Williamsburg, Virginia",
        "title": "Williamsburg Wedding Photographer & Film | Aikhoje Studios",
        "desc": "Williamsburg, Virginia wedding photography and film by Aikhoje Studios. Colonial streets, historic estates, wineries and the James River. Editorial and documentary, since 2015.",
        "hero": "film-couple-steps",
        "hero_sub": "Colonial streets, historic estates, vineyards, and the James River.",
        "intro_h": "History<br>with a heartbeat.",
        "intro": [
            "Williamsburg weddings carry a sense of place you can feel in every frame: brick paths and colonial architecture, old estates along the James River, and vineyards that glow at the end of the day.",
            "I photograph and film Williamsburg weddings with a timeless, editorial approach that suits the setting, while keeping the documentary moments that make the day yours: the laughter, the nerves, the hands held a little tighter.",
        ],
        "intro_img": "36",
        "notes_h": "Planning a Williamsburg wedding.",
        "notes_copy": "A few things I talk through with Williamsburg couples.",
        "notes": [
            ("Historic-area portraits", "Colonial Williamsburg and the surrounding historic sites make beautiful backdrops, and some have their own photography rules. Check with your venue or the site ahead of time."),
            ("Fall is the season", "October and early November bring warm color and mild evenings, and dates book early. Spring is a close second."),
            ("Vineyard and estate light", "Open lawns and long views mean golden hour does a lot of the work. I plan portrait time around sunset for your date."),
            ("Weekend celebrations", "Many Williamsburg weddings are destination weekends. I can cover welcome dinners and farewell brunches as well as the wedding day."),
        ],
        "gallery": ["film-couple-steps", "36", "dscf0309", "film-couple-mountains", "aw-197", "dscf0031", "dscf0084", "wedding-380", "film-bride-bouquet", "untitled-32", "dscf0427", "0-104"],
    },
    {
        "slug": "richmond-wedding-photographer",
        "name": "Richmond",
        "region": "Richmond, Virginia",
        "title": "Richmond Wedding Photographer & Film | Aikhoje Studios",
        "desc": "Richmond, Virginia wedding photography and film by Aikhoje Studios. Historic hotels, gardens, warehouse venues and the James River. Editorial and documentary, since 2015.",
        "hero": "dscf0604",
        "hero_sub": "Grand hotels, garden estates, warehouse venues, and the James River.",
        "intro_h": "Classic, creative,<br>and all your own.",
        "intro": [
            "Richmond weddings run from black-tie ballrooms to industrial warehouse parties, garden ceremonies, and riverside celebrations. It is a city with real character, and I love a wedding that leans into it.",
            "I photograph and film Richmond weddings with an editorial eye for the architecture and a documentary heart for the people, so the gallery feels like your day in your city, not a template.",
        ],
        "intro_img": "vineyard-kiss-closeup",
        "notes_h": "Planning a Richmond wedding.",
        "notes_copy": "A few things I talk through with Richmond couples.",
        "notes": [
            ("Gardens and grounds", "Richmond's public gardens and historic estates are popular for ceremonies and portraits, and many require a permit or booking for photography. Ask early."),
            ("City portraits", "Brick streets, murals, and old warehouses make strong editorial backdrops. A short portrait walk between ceremony and reception goes a long way."),
            ("Summer heat", "July and August can be hot and humid. I plan shaded portrait spots and lean on evening light so everyone stays comfortable."),
            ("Every tradition", "Richmond weddings often blend cultures and traditions. I have photographed ceremonies of many faiths and backgrounds and plan coverage around each one."),
        ],
        "gallery": ["dscf0604", "vineyard-kiss-closeup", "untitled-31", "signal-2022-10-03-162349_002", "dscf0614-2", "7", "196", "untitled-23", "0-1", "dscf0427", "9344835903_50e22f1f0e_o", "aw-146"],
    },
    {
        "slug": "raleigh-durham-wedding-photographer",
        "name": "Raleigh-Durham",
        "region": "Raleigh, Durham and Chapel Hill, North Carolina",
        "title": "Raleigh-Durham Wedding Photographer & Film | Aikhoje Studios",
        "desc": "Raleigh, Durham and Chapel Hill wedding photography and film by Aikhoje Studios. Gardens, chapels, tobacco warehouses and farm venues. Editorial and documentary, since 2015.",
        "hero": "dscf0309",
        "hero_sub": "Gardens, chapels, tobacco warehouses, and farm venues across the Triangle.",
        "intro_h": "The Triangle,<br>told well.",
        "intro": [
            "Raleigh, Durham, and Chapel Hill offer some of the most varied wedding settings in North Carolina: university chapels and gardens, restored tobacco warehouses, modern downtown spaces, and rolling farm venues just outside the city.",
            "I photograph and film weddings across the Triangle with an editorial, documentary approach: honest moments, natural color, and portraits that feel like you.",
        ],
        "intro_img": "20191019-dscf0340",
        "notes_h": "Planning a Triangle wedding.",
        "notes_copy": "A few things I talk through with Raleigh-Durham couples.",
        "notes": [
            ("Gardens and campuses", "The Triangle's gardens and campus landmarks are favorite portrait spots, and several require reservations or permits for wedding photography. Book them with your venue early."),
            ("Farm and barn venues", "Open fields and tree lines give soft, even light. I plan portraits for the last hour before sunset."),
            ("Warehouse and downtown venues", "Brick, steel, and big windows suit an editorial look. I bring lighting for receptions so evening coverage stays clean and true to color."),
            ("Spring and fall", "April, May, October, and November are the busiest months in the Triangle. Pollen season in early spring is worth knowing about for outdoor ceremonies."),
        ],
        "gallery": ["dscf0309", "vineyard-kiss-closeup", "20191019-dscf0340", "20191019-dscf0491", "film-couple-steps", "dscf0084", "dscf0031", "untitled-23", "7", "4", "trix400_2017-08-22-0020", "dscf0599"],
    },
    {
        "slug": "wilmington-wedding-photographer",
        "name": "Wilmington",
        "region": "Wilmington, North Carolina",
        "title": "Wilmington Wedding Photographer & Film | Aikhoje Studios",
        "desc": "Wilmington, NC wedding photography and film by Aikhoje Studios. Riverfront downtown, live oak gardens, and Wrightsville, Carolina and Kure beaches. Editorial and documentary, since 2015.",
        "hero": "dscf0497-2",
        "hero_sub": "The riverfront, live oak gardens, and Wrightsville, Carolina, and Kure beaches.",
        "intro_h": "River, oaks,<br>and open ocean.",
        "intro": [
            "Wilmington pairs a historic riverfront downtown with live oaks draped in Spanish moss and some of the prettiest beaches on the Carolina coast. Couples can marry in a garden, celebrate downtown, and take portraits on the sand, all in one day.",
            "I photograph and film Wilmington weddings with an editorial eye and a documentary heart, so your gallery holds both the beauty of the place and the honest moments between the people in it.",
        ],
        "intro_img": "film-beach-couple",
        "notes_h": "Planning a Wilmington wedding.",
        "notes_copy": "A few things I talk through with Wilmington couples.",
        "notes": [
            ("Garden ceremonies", "Wilmington's gardens and historic homes are popular for ceremonies and portraits, and many book up early in spring when the azaleas bloom."),
            ("Beach portraits", "Wrightsville, Carolina, and Kure beaches are all close to town. Each beach town has its own rules for ceremonies, so check before you plan one on the sand."),
            ("Riverfront evenings", "Downtown along the Cape Fear River is lovely after dark. A few evening portraits with the lights on the water make a great close to the day."),
            ("Hurricane season", "Late summer and early fall carry some storm risk on the coast. I always talk through a backup plan for outdoor ceremonies."),
        ],
        "gallery": ["dscf0497-2", "film-beach-couple", "film-beach-kiss-bw", "dscf0559", "aw-197", "film-bride-bouquet", "untitled-84-2", "118", "dscf0486", "aw-190", "311", "film-hands-color"],
    },
]

AREA_NAV_NAME = {
    "outer-banks-wedding-photographer": "Outer Banks",
    "virginia-beach-wedding-photographer": "Virginia Beach & Hampton Roads",
    "wilmington-wedding-photographer": "Wilmington",
    "williamsburg-wedding-photographer": "Williamsburg",
    "richmond-wedding-photographer": "Richmond",
    "raleigh-durham-wedding-photographer": "Raleigh-Durham",
}


def esc(s):
    return html.escape(s, quote=True)


def photo(key):
    p = PHOTOS[key]
    return p


def large(key):
    """URL of the 1200px (or largest) WebP for a photo."""
    return PHOTOS[key]["srcset"].split(", ")[-1].split(" ")[0]


def img(key, sizes, cls="", lazy=True, alt=None):
    p = PHOTOS[key]
    a = esc(alt if alt is not None else p["alt"])
    c = f' class="{cls}"' if cls else ""
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    return (f'<img{c} src="{large(key)}" srcset="{p["srcset"]}" sizes="{sizes}" '
            f'width="{p["width"]}" height="{p["height"]}" alt="{a}"{load} decoding="async">')


def em_title(text_with_br):
    """'Wind, salt,<br>and golden light.' -> 'Wind, salt, <em>and golden light.</em>'"""
    if "<br>" in text_with_br:
        a, b = text_with_br.split("<br>", 1)
        return f"{esc(a)} <em>{esc(b)}</em>"
    return esc(text_with_br)


# ---------------------------------------------------------------------------------------------
# Shared page parts
# ---------------------------------------------------------------------------------------------

VERIFICATION = """<meta name="google-site-verification" content="oZkggRjuqXnjA4Z2QU2YsTbLi1PQHYLp-wU5txYEppo" />
<meta name="p:domain_verify" content="dbae2caff80e14e75b3591723e6bc5b6"/>"""


def head(title, desc, path, schema, og_image="/images/og-autumn-couple.jpg", og_alt="Groom in a white tuxedo and bride in a lace gown holding hands under autumn trees, photographed by Aikhoje Studios", extra="", robots="index, follow"):
    url = SITE + path
    blocks = "\n".join(
        f'<script type="application/ld+json">\n{json.dumps(s, indent=2, ensure_ascii=False)}\n</script>' for s in schema
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{"" if robots.startswith("noindex") else f'<link rel="canonical" href="{url}">'}
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#1e291b">
<meta name="geo.region" content="US-NC">
{VERIFICATION}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Aikhoje Studios">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(og_alt)}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE}{og_image}">
<meta name="twitter:image:alt" content="{esc(og_alt)}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/fonts/libre-caslon-display-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/newsreader-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/evergreen.css?v={TODAY}">
{extra}<!-- Generated by scripts/build-site.py. Edit the script or its data files, not this file. -->
{blocks}
</head>
"""


def header(current=""):
    def item(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<li><a href="{href}"{cur}>{label}</a></li>'
    return f"""<body>
<a class="skip-link" href="#content">Skip to content</a>

<header class="site-head" id="site-head">
  <div class="site-head-in">
    <a href="/" class="wordmark" aria-label="Aikhoje Studios, home">AIKHOJE STUDIOS</a>
    <button type="button" class="nav-toggle" id="nav-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav aria-label="Primary">
      <ul class="nav-links" id="site-nav">
        {item("/gallery/", "Gallery", "gallery")}
        {item("/#film", "Film", "film")}
        {item("/#about", "About", "about")}
        {item("/#places", "Places", "places")}
        {item("/#questions", "Questions", "questions")}
      </ul>
    </nav>
    <a class="btn btn-sand head-cta" href="#contact">Inquire</a>
  </div>
</header>
"""


def inquiry(chapter_label, page_name=None):
    subject = "New wedding inquiry from your website" + (f" ({page_name} page)" if page_name else "")
    page_field = f'\n      <input type="hidden" name="Inquiry Page" value="{esc(page_name)}">' if page_name else ""
    return f"""
<section class="sec bg-moss" id="contact" aria-labelledby="contact-title">
  <div class="wrap" style="max-width: 720px; display: flex; flex-direction: column; gap: 3rem">
    <div class="sec-head">
      <p class="label">{chapter_label}</p>
      <h2 id="contact-title" class="title">Let’s tell <em>your story.</em></h2>
      <p class="body" style="max-width: 32rem">Tell me a little about your day. I reply to every inquiry within 24 hours.</p>
    </div>
    <form id="inquiry-form" class="inquiry-form" data-endpoint="{FORM_ENDPOINT}">
      <input type="hidden" name="_subject" value="{esc(subject)}">{page_field}
      <input type="hidden" name="_autoresponse" value="Thank you for reaching out to Aikhoje Studios! I’ve received your inquiry and will get back to you within 24 hours. In the meantime, feel free to reply to this email with anything else you’d like me to know about your day. — Aigbokhai, Aikhoje Studios">
      <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">
      <div style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden" aria-hidden="true"><label>Website <input type="text" name="_website" tabindex="-1" autocomplete="off"></label></div>
      <div class="form-row">
        <div class="field"><label for="inquiry-name">Your name</label><input id="inquiry-name" name="Name" type="text" autocomplete="name" required maxlength="120"></div>
        <div class="field"><label for="inquiry-email">Email</label><input id="inquiry-email" name="email" type="email" autocomplete="email" required maxlength="160"></div>
      </div>
      <div class="form-row">
        <div class="field"><label for="inquiry-date">Wedding date <span class="optional">(optional)</span></label><input id="inquiry-date" name="Wedding Date" type="date"></div>
        <div class="field"><label for="inquiry-place">Ceremony location <span class="optional">(optional)</span></label><input id="inquiry-place" name="Ceremony Location" type="text" maxlength="160"></div>
      </div>
      <div class="form-row">
        <div class="field"><label for="inquiry-phone">Phone <span class="optional">(optional)</span></label><input id="inquiry-phone" name="Phone" type="tel" autocomplete="tel" maxlength="40"></div>
        <div class="field"><label for="inquiry-contact">Best way to reach you</label>
          <select id="inquiry-contact" name="Preferred Contact"><option>Email</option><option>Phone call</option><option>Text</option></select></div>
      </div>
      <div class="form-row">
        <div class="field"><label for="inquiry-size">Wedding size</label>
          <select id="inquiry-size" name="Wedding Size" required><option value="" disabled selected>Choose one</option><option>Elopement (just us)</option><option>Under 50 guests</option><option>50–150 guests</option><option>150+ guests</option><option>Not sure yet</option></select></div>
        <div class="field"><label for="inquiry-source">How did you hear about me?</label>
          <select id="inquiry-source" name="Heard About Me Via" required><option value="" disabled selected>Choose one</option><option>Instagram</option><option>Google search</option><option>My venue</option><option>My wedding planner</option><option>A friend or past couple</option><option>Other</option></select></div>
      </div>
      <div class="field"><label for="inquiry-note">About your day</label><textarea id="inquiry-note" name="About Their Day" required maxlength="4000"></textarea></div>
      <div class="form-actions">
        <button type="submit" class="btn btn-sand">Send inquiry</button>
        <p class="body" style="font-size: .9375rem">Prefer to talk? Call or text <a href="tel:{PHONE}">{PHONE_SHOWN}</a>, or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
      </div>
      <p id="form-status" class="form-status" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>
"""


def footer():
    return f"""</main>

<footer class="site-foot">
  <div class="wrap">
    <p class="wordmark" style="margin: 0; font-size: 1.15rem">AIKHOJE STUDIOS</p>
    <p class="foot-tag">Love written in light.</p>
    <hr class="rule">
    <nav aria-label="Footer" class="foot-links">
      <a href="/gallery/">Gallery</a>
      <a href="/#film">Film</a>
      <a href="/#contact">Inquire</a>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
      <a href="tel:{PHONE}">{PHONE_SHOWN}</a>
      <a href="https://www.instagram.com/aikhojestudios/" rel="noopener" target="_blank">Instagram</a>
      <a href="https://www.facebook.com/AikhojeStudios/" rel="noopener" target="_blank">Facebook</a>
      <a href="https://maps.google.com/?cid=2370023642542401137" rel="noopener" target="_blank">Google Reviews</a>
      <a href="/real-estate/">Real Estate Photography</a>
    </nav>
    <nav aria-label="Places" class="foot-links">
      {" ".join(f'<a href="/{a["slug"]}/">{esc(AREA_NAV_NAME[a["slug"]])}</a>' for a in AREAS)}
    </nav>
    <p class="label colophon">Colophon · Set in Newsreader, Instrument Sans &amp; Libre Caslon Display · Photographed on film and digital since 2015 · Coastal North Carolina, available worldwide</p>
    <p class="foot-small">© {YEAR} Aikhoje Studios · Wedding &amp; portrait photography and film</p>
  </div>
</footer>

<a class="mobile-inquire" id="mobile-inquire" href="#contact" hidden>Inquire about your date</a>

<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Photo viewer" hidden>
  <p id="lb-status" class="visually-hidden" aria-live="polite"></p>
  <button type="button" class="lb-btn lb-close" aria-label="Close viewer"><svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M2 2 L14 14 M14 2 L2 14" stroke="currentColor" stroke-width="1.4" fill="none"/></svg></button>
  <div class="lb-stage">
    <button type="button" class="lb-btn lb-prev" aria-label="Previous photograph"><svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M10 2 L4 8 L10 14" stroke="currentColor" stroke-width="1.4" fill="none"/></svg></button>
    <img class="lb-img" alt="">
    <button type="button" class="lb-btn lb-next" aria-label="Next photograph"><svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M6 2 L12 8 L6 14" stroke="currentColor" stroke-width="1.4" fill="none"/></svg></button>
  </div>
  <p class="lb-count"></p>
</div>

<script src="/js/site.js?v={TODAY}" defer></script>
<script data-goatcounter="https://aikhojestudios.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</body>
</html>
"""


def sheet(keys, sizes="(max-width: 560px) 100vw, (max-width: 900px) 50vw, 25vw"):
    out = []
    for k in keys:
        p = PHOTOS[k]
        ratio = p["width"] / p["height"]
        cls = "tall" if ratio < .9 else ("pano" if ratio > 1.6 else "wide")
        if cls == "pano":
            cls = "wide pano"
        out.append(f'<li class="{cls}"><button type="button" data-full="/images/{k}.jpg" aria-label="Open photograph: {esc(p["alt"])}">{img(k, sizes)}</button></li>')
    return '<ul class="sheet">\n      ' + "\n      ".join(out) + "\n    </ul>"


def reviews_section(label):
    cards = []
    for r in REVIEWS:
        cards.append(f"""      <li class="review">
        <figure style="margin: 0; display: flex; flex-direction: column; height: 100%">
          <img src="/images/opt/{r['img']}-1200.webp" srcset="/images/opt/{r['img']}-640.webp 640w, /images/opt/{r['img']}-1200.webp 1200w" sizes="(max-width: 900px) 100vw, 33vw" width="1200" height="800" alt="{esc(r['alt'])}" loading="lazy" decoding="async">
          <div class="review-body">
            <span class="stars" role="img" aria-label="5 out of 5 stars">★★★★★</span>
            <blockquote><p>“{esc(r['quote'])}”</p></blockquote>
            <figcaption><span class="label who">{esc(r['who'])}</span><span class="what">{esc(r['what'])}</span></figcaption>
          </div>
        </figure>
      </li>""")
    return f"""
<section class="sec" id="reviews" aria-labelledby="reviews-title">
  <div class="wrap" style="display: flex; flex-direction: column; gap: 4rem">
    <div class="sec-head">
      <p class="label">{label}</p>
      <h2 id="reviews-title" class="title">From couples <em>&amp; colleagues.</em></h2>
      <p class="ui" style="margin: 0; font-size: .8125rem; color: var(--lichen); letter-spacing: .04em"><span class="stars">★★★★★</span> 5.0 on <a href="https://maps.google.com/?cid=2370023642542401137" rel="noopener" target="_blank">Google</a></p>
    </div>
    <ul class="reviews">
{chr(10).join(cards)}
    </ul>
  </div>
</section>
"""


def provider_ref():
    b = BUSINESS["@graph"][0]
    return {
        "@type": ["Photographer", "LocalBusiness"], "@id": f"{SITE}/#business", "name": b["name"], "url": b["url"],
        "image": b["image"], "email": b["email"], "telephone": b["telephone"], "address": b["address"], "sameAs": b.get("sameAs", []),
    }


def write(rel, text):
    out = ROOT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    print("wrote", rel)


# ---------------------------------------------------------------------------------------------
# Homepage
# ---------------------------------------------------------------------------------------------

def homepage():
    title = "Aikhoje Studios — Love written in light | Wedding Photographer & Film, Coastal NC"
    desc = ("Aikhoje Studios — editorial and documentary wedding photography and film on the East Coast and worldwide, "
            "from coastal North Carolina to Hampton Roads and beyond. In business since 2015.")
    faq_schema = {
        "@context": "https://schema.org", "@type": "FAQPage", "@id": f"{SITE}/#faq",
        "mainEntity": [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in FAQ],
    }
    business = json.loads(json.dumps(BUSINESS))
    for node in business["@graph"]:
        if node.get("@type") == "WebPage":
            node["name"] = title
            node["description"] = desc
    cover_list = json.dumps([[f"/images/cover/{c}-1000.webp", f"/images/cover/{c}-640.webp", alt] for c, alt in COVERS], ensure_ascii=False)
    first, first_alt = COVERS[0]
    extra = (f'<link rel="preload" as="image" href="/images/cover/{first}-1000.webp" '
             f'imagesrcset="/images/cover/{first}-640.webp 640w, /images/cover/{first}-1000.webp 1000w" imagesizes="(max-width: 520px) 80vw, 384px" type="image/webp">\n')

    places = []
    for i, a in enumerate(AREAS, 1):
        places.append(f'<li><span class="num">{i:02d}</span><div><h3><a href="/{a["slug"]}/">{esc(a["region"] if a["slug"] != "virginia-beach-wedding-photographer" else "Virginia Beach & Hampton Roads")}</a></h3><p>{esc(a["hero_sub"])}</p></div></li>')
    places.append(f'<li><span class="num">{len(AREAS) + 1:02d}</span><div><h3>Worldwide</h3><p>Available wherever your day takes you.</p></div></li>')

    faq_items = []
    for i, f in enumerate(FAQ):
        opened = " open" if i == 0 else ""
        faq_items.append(f'<details{opened}><summary>{esc(f["q"])}</summary><p>{esc(f["a"])}</p></details>')

    contents = [("I", "The Approach", "#approach", 3), ("II", "The Gallery", "#gallery", 9), ("III", "The Film", "#film", 21),
                ("IV", "Kind Words", "#reviews", 25), ("V", "The Author", "#about", 29), ("VI", "Places", "#places", 35),
                ("App.", "Questions Couples Ask", "#questions", 39), ("VII", "Your Story", "#contact", 43)]
    contents_html = "\n        ".join(
        f'<li><a href="{h}"><span class="label c-num">{n}</span><span class="c-name">{esc(t)}</span><span class="c-page" aria-hidden="true">{p}</span></a></li>'
        for n, t, h, p in contents)

    body = f"""{head(title, desc, "/", [business, faq_schema], extra=extra)}{header()}
<main id="content">

<section class="title-page" id="title" aria-labelledby="page-title">
  <p class="label">Wedding Photography &amp; Film · Since 2015</p>
  <figure class="mat">
    <div class="mat-in"><img id="cover-img" class="cover-img" src="/images/cover/{first}-1000.webp" srcset="/images/cover/{first}-640.webp 640w, /images/cover/{first}-1000.webp 1000w" sizes="(max-width: 520px) 80vw, 384px" width="1000" height="1500" alt="{esc(first_alt)}" fetchpriority="high" decoding="async"></div>
  </figure>
  <script>(function(){{var c={cover_list};var p=c[Math.floor(Math.random()*c.length)];var i=document.getElementById("cover-img");i.src=p[0];i.srcset=p[1]+" 640w, "+p[0]+" 1000w";i.alt=p[2];}})();</script>
  <div class="title-copy">
    <h1 id="page-title">Love written <em>in light.</em></h1>
    <p class="body" style="max-width: 34rem">Intimate, editorial wedding photography and film for couples who want their day remembered as it felt — not just as it looked. Outer Banks, Hampton Roads &amp; coastal North Carolina, available worldwide.</p>
    <div class="btn-row">
      <a class="btn btn-sand" href="#contact">Inquire about your date</a>
      <a class="btn btn-line" href="/gallery/">View the gallery</a>
    </div>
  </div>
  <p class="label triplet"><span>Every couple.</span><span>Every culture.</span><span>Every moment.</span></p>
</section>

<section class="sec bg-deep" id="contents" aria-labelledby="contents-title" style="padding-top: 7rem; padding-bottom: 7rem">
  <div class="wrap" style="max-width: 760px; display: flex; flex-direction: column; gap: 2.5rem">
    <div class="sec-head">
      <p class="label">Contents</p>
      <h2 id="contents-title" class="title">A wedding, <em>told in chapters.</em></h2>
    </div>
    <nav aria-label="Contents">
      <ol class="contents">
        {contents_html}
      </ol>
    </nav>
  </div>
</section>

<section class="sec" id="approach" aria-labelledby="approach-title">
  <div class="wrap split">
    <div class="chapter-text">
      <p class="label"><b>Chapter I</b> · The Approach</p>
      <h2 id="approach-title" class="title">Every couple. Every culture. <em>Every moment.</em></h2>
      <hr class="rule">
      <p class="lead dropcap">With over a decade behind the lens, I bring an editorial eye and a documentary heart to every wedding.</p>
      <p class="body" style="max-width: 34rem">From South Asian ceremonies to intimate elopements, vineyard celebrations to golden-hour hilltop vows — I’m here to tell the story the way it actually unfolded. I’m based in coastal North Carolina and available worldwide.</p>
    </div>
    <figure class="mat chapter-figure"><div class="mat-in">{img("church-steps-bw", "(max-width: 900px) 90vw, 380px")}</div></figure>
  </div>
</section>

<section class="sec bg-moss" id="gallery" aria-labelledby="gallery-title">
  <div class="wrap-wide" style="display: flex; flex-direction: column; gap: 3.5rem">
    <div class="sec-head">
      <p class="label"><b>Chapter II</b> · The Gallery</p>
      <h2 id="gallery-title" class="title">Selected work, <em>as a contact sheet.</em></h2>
      <p class="body" style="max-width: 32rem">Weddings, elopements, and love stories across cultures.</p>
    </div>
    {sheet(["vineyard-kiss-closeup", "petals-celebration", "mirror-steps", "film-couple-mountains", "altar-portrait", "night-veil-bw"])}
    <div style="text-align: center"><a class="btn btn-line" href="/gallery/">See the full gallery</a></div>
  </div>
</section>

<section class="sec bg-deep" id="film" aria-labelledby="film-title">
  <div class="wrap" style="max-width: 1040px; display: flex; flex-direction: column; gap: 3rem; align-items: center; text-align: center">
    <div class="sec-head">
      <p class="label"><b>Chapter III</b> · The Film</p>
      <h2 id="film-title" class="title">The Reel, <em>in motion.</em></h2>
      <p class="body">A glimpse into how I see your day.</p>
    </div>
    <div class="film-stack">
      <div class="film-item">
        <!-- OWNER TODO: add an English captions file and a <track kind="captions"> for video/reel.mp4 -->
        <div class="video-frame"><video controls playsinline preload="none" poster="/images/opt/dscf0599-1200.webp" width="1280" height="720" aria-label="Wedding film reel"><source src="/video/reel.mp4" type="video/mp4"></video></div>
      </div>
      <div class="film-item">
        <h3 class="label" style="color: var(--ivory)">Behind the moments · Wedding day film</h3>
        <!-- OWNER TODO: add an English captions file and a <track kind="captions"> for video/wedding.mp4 -->
        <div class="video-frame"><video controls playsinline preload="none" poster="/images/opt/dscf0604-1200.webp" width="1280" height="720" aria-label="Wedding day film"><source src="/video/wedding.mp4" type="video/mp4"></video></div>
      </div>
    </div>
  </div>
</section>
{reviews_section("<b>Chapter IV</b> · Kind Words")}
<section class="sec bg-moss" id="about" aria-labelledby="about-title">
  <div class="wrap split">
    <figure class="mat chapter-figure"><div class="mat-in"><img src="/images/opt/meet-fu-800.webp" srcset="/images/opt/meet-fu-640.webp 640w, /images/opt/meet-fu-800.webp 800w" sizes="(max-width: 900px) 90vw, 380px" width="800" height="1200" alt="Aigbokhai Aikhoje, wedding photographer, smiling outdoors with his children" loading="lazy" decoding="async"></div></figure>
    <div class="chapter-text" style="gap: 1.4rem">
      <p class="label"><b>Chapter V</b> · The Author</p>
      <h2 id="about-title" class="title">Hi, I’m <em>Aigbokhai.</em></h2>
      <hr class="rule">
      <p class="lead dropcap" style="font-size: 1.25rem">I’ve always wanted a way to capture the world as it changes. It started with a Canon AE-1 Program and photos of my friends and family, documenting the real love shared between people. That is still what I’m chasing.</p>
      <p class="body">I love people and make friends easily, so when a friend asked me to second shoot his wedding, it felt completely natural. I was already documenting real relationships; now I got to document people on the happiest day of their lives. More than eleven years later, I still can’t believe I get to do this, and I feel incredibly lucky.</p>
      <p class="body">Every wedding day is special. On the day I’m calm, joyful and organized. I pay attention to the setting and bring whichever of my skills the day needs. Couples almost always mention how calm I am — that’s simply who I am.</p>
      <p class="body">I also shoot real film and develop it in my own lab. Its character can’t be replicated, it tells a story beautifully, and the slower process has made me a better artist.</p>
      <p class="body">Off the clock, you’ll find me in the yard working on one of a thousand projects. The truck or the yard? Depends on my mood.</p>
      <p style="margin: .4rem 0 0; font-size: 1.75rem; font-style: italic; font-weight: 300; color: var(--sand)">— Aigbokhai</p>
    </div>
  </div>
</section>

<section class="sec" id="places" aria-labelledby="places-title">
  <div class="wrap split top">
    <div class="places-intro">
      <p class="label"><b>Chapter VI</b> · Places</p>
      <h2 id="places-title" class="title">The Outer Banks, Hampton Roads, <em>and worldwide.</em></h2>
      <p class="body" style="max-width: 30rem">Aikhoje Studios has photographed and filmed weddings since 2015. I am booking weddings, elopements, and engagement sessions along the Carolina and Virginia coast, and I am available worldwide.</p>
    </div>
    <ol class="places">
      {chr(10).join("      " + p for p in places).strip()}
    </ol>
  </div>
</section>

<section class="sec paper" id="questions" aria-labelledby="faq-title">
  <div class="wrap" style="max-width: 760px; display: flex; flex-direction: column; gap: 2.5rem">
    <div class="sec-head">
      <p class="label"><b>Appendix</b> · Good to know</p>
      <h2 id="faq-title" class="title">Questions <em>couples ask.</em></h2>
    </div>
    <div class="faq">
      {chr(10).join("      " + f for f in faq_items).strip()}
    </div>
    <p class="footnote">Still wondering about something? <a href="#contact">Ask me directly</a> — I reply to every inquiry within 24 hours.</p>
  </div>
</section>
{inquiry("<b>Chapter VII</b> · Your Story")}
{footer()}"""
    write("index.html", body)


# ---------------------------------------------------------------------------------------------
# Gallery page
# ---------------------------------------------------------------------------------------------

def gallery_page():
    missing = set(PHOTOS) - set(GALLERY_ORDER)
    assert not missing, f"photos.json entries missing from GALLERY_ORDER: {missing}"
    title = "Wedding Photography Gallery | Aikhoje Studios"
    desc = ("Wedding photography by Aikhoje Studios: getting ready, portraits, ceremonies and celebrations, "
            "details, black and white, and real film. Coastal North Carolina, Hampton Roads and worldwide.")
    url = f"{SITE}/gallery/"
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "CollectionPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc,
             "isPartOf": {"@id": f"{SITE}/#website"}, "about": {"@id": f"{SITE}/#business"},
             "breadcrumb": {"@id": url + "#breadcrumb"}, "inLanguage": "en-US",
             "primaryImageOfPage": {"@type": "ImageObject", "contentUrl": f"{SITE}{large(GALLERY_ORDER[0])}"}},
            {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Aikhoje Studios", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "Gallery", "item": url}]},
        ],
    }
    counts = {k: (len(PHOTOS) if k == "all" else sum(k in p["tags"] for p in PHOTOS.values())) for k, _ in FILTERS}
    chips = "\n      ".join(
        f'<button type="button" class="chip" data-filter="{k}" data-label="{esc(l)}" aria-pressed="{"true" if k == "all" else "false"}">{esc(l)} <span>{counts[k]}</span></button>'
        for k, l in FILTERS)
    tiles = "\n      ".join(
        f'<li class="tile" data-tags="{" ".join(PHOTOS[k]["tags"])}"><button type="button" data-full="/images/{k}.jpg" aria-label="Open photograph: {esc(PHOTOS[k]["alt"])}">{img(k, "(max-width: 560px) 100vw, (max-width: 900px) 50vw, 33vw", lazy=i > 5)}</button></li>'
        for i, k in enumerate(GALLERY_ORDER))
    body = f"""{head(title, desc, "/gallery/", [schema])}{header("gallery")}
<main id="content">

<section class="sec" style="padding-bottom: 3rem" aria-labelledby="page-title">
  <div class="wrap-wide" style="display: flex; flex-direction: column; gap: 2.5rem">
    <div class="sec-head">
      <p class="label"><b>Chapter II</b> · The Gallery</p>
      <h1 id="page-title" class="title" style="font-size: clamp(2.4rem, 5vw, 4rem); line-height: 1.05">Weddings, elopements, <em>and love stories.</em></h1>
      <p class="body" style="max-width: 34rem">Real days, photographed as they unfolded, on digital and on film. Choose a part of the day, or see everything.</p>
    </div>
    <div class="chips" id="gallery-filters" role="group" aria-label="Filter the gallery">
      {chips}
    </div>
  </div>
</section>

<section class="sec" style="padding-top: 0" aria-label="Photographs">
  <div class="wrap-wide" style="display: flex; flex-direction: column; gap: 1.5rem">
    <p class="count" id="gallery-count" aria-live="polite">{len(PHOTOS)} photographs</p>
    <ul class="wall">
      {tiles}
    </ul>
  </div>
</section>
{reviews_section("Kind Words")}
{inquiry("<b>Chapter VII</b> · Your Story", "Gallery")}
{footer()}"""
    write("gallery/index.html", body)


# ---------------------------------------------------------------------------------------------
# Location pages
# ---------------------------------------------------------------------------------------------

def area_page(a):
    url = f"{SITE}/{a['slug']}/"
    others = [o for o in AREAS if o["slug"] != a["slug"]]
    other_links = ", ".join(f'<a href="/{o["slug"]}/">{esc(AREA_NAV_NAME[o["slug"]])}</a>' for o in others)
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": a["title"], "description": a["desc"],
             "isPartOf": {"@id": f"{SITE}/#website"}, "about": {"@id": url + "#service"},
             "breadcrumb": {"@id": url + "#breadcrumb"}, "inLanguage": "en-US",
             "primaryImageOfPage": {"@type": "ImageObject", "contentUrl": f"{SITE}{large(a['hero'])}"}},
            {"@type": "Service", "@id": url + "#service", "name": f"{a['name']} wedding photography and film",
             "serviceType": "Wedding photography and videography", "areaServed": {"@type": "Place", "name": a["region"]},
             "provider": provider_ref()},
            {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Aikhoje Studios", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": f"{a['name']} Wedding Photographer", "item": url}]},
        ],
    }
    notes = "\n      ".join(
        f'<li><span class="num">{i:02d}</span><div><h3>{esc(h)}</h3><p>{esc(p)}</p></div></li>'
        for i, (h, p) in enumerate(a["notes"], 1))
    intro_ps = "\n      ".join(
        (f'<p class="lead dropcap">{esc(p)}</p>' if i == 0 else f'<p class="body">{esc(p)}</p>')
        for i, p in enumerate(a["intro"]))
    hero = PHOTOS[a["hero"]]
    hero_tall = hero["width"] / hero["height"] < 1
    hero_width = "min(440px, 100%)" if hero_tall else "min(760px, 100%)"
    body = f"""{head(a["title"], a["desc"], "/" + a["slug"] + "/", [schema], og_image=large(a["hero"]) if False else "/images/og-autumn-couple.jpg")}{header("places")}
<main id="content">

<section class="title-page area" aria-labelledby="page-title">
  <p class="label">Aikhoje Studios · {esc(a['name'])}</p>
  <figure class="mat" style="width: {hero_width}"><div class="mat-in">{img(a["hero"], "(max-width: 900px) 90vw, 700px", lazy=False)}</div></figure>
  <div class="title-copy">
    <h1 id="page-title">{esc(a['name'])} Wedding <em>Photographer &amp; Film</em></h1>
    <p class="body" style="max-width: 34rem">{esc(a['hero_sub'])}</p>
    <div class="btn-row">
      <a class="btn btn-sand" href="#contact">Inquire about your date</a>
      <a class="btn btn-line" href="#gallery">View the work</a>
    </div>
  </div>
  <p class="label triplet"><span>Editorial &amp; documentary.</span><span>Since 2015.</span><span>Available worldwide.</span></p>
</section>

<section class="sec bg-deep" id="approach" aria-labelledby="approach-title">
  <div class="wrap split">
    <div class="chapter-text">
      <p class="label"><b>Chapter I</b> · {esc(a['name'])} Weddings</p>
      <h2 id="approach-title" class="title">{em_title(a['intro_h'])}</h2>
      <hr class="rule">
      {intro_ps}
    </div>
    <figure class="mat chapter-figure"><div class="mat-in">{img(a["intro_img"], "(max-width: 900px) 90vw, 380px")}</div></figure>
  </div>
</section>

<section class="sec" id="notes" aria-labelledby="notes-title">
  <div class="wrap split top">
    <div class="places-intro">
      <p class="label"><b>Chapter II</b> · Good to Know</p>
      <h2 id="notes-title" class="title">{esc(a['notes_h'])}</h2>
      <p class="body" style="max-width: 30rem">{esc(a['notes_copy'])} I also photograph weddings in {other_links}, and anywhere your day takes you.</p>
    </div>
    <ol class="places">
      {notes}
    </ol>
  </div>
</section>

<section class="sec bg-moss" id="gallery" aria-labelledby="gallery-title">
  <div class="wrap-wide" style="display: flex; flex-direction: column; gap: 3.5rem">
    <div class="sec-head">
      <p class="label"><b>Chapter III</b> · Selected Work</p>
      <h2 id="gallery-title" class="title">A selection of <em>love stories.</em></h2>
      <p class="body" style="max-width: 32rem">Weddings, elopements, and celebrations, photographed on digital and on film.</p>
    </div>
    {sheet(a["gallery"])}
    <div style="text-align: center"><a class="btn btn-line" href="/gallery/">See the full gallery</a></div>
  </div>
</section>
{reviews_section("<b>Chapter IV</b> · Kind Words")}
{inquiry("<b>Chapter V</b> · Your Story", a["name"])}
{footer()}"""
    write(f"{a['slug']}/index.html", body)


# ---------------------------------------------------------------------------------------------
# 404, redirects, sitemap
# ---------------------------------------------------------------------------------------------

def not_found():
    body = f"""{head("Page not found — Aikhoje Studios", "This page isn’t here, but the rest of the story is.", "/404.html", [], robots="noindex")}{header()}
<main id="content">
<section class="title-page" aria-labelledby="page-title" style="min-height: 70vh; justify-content: center">
  <p class="label">Aikhoje Studios — Love written in light</p>
  <div class="title-copy">
    <h1 id="page-title" style="font-size: clamp(2.4rem, 6vw, 4.5rem)">This page <em>wandered off.</em></h1>
    <p class="body" style="max-width: 30rem">The page you’re looking for isn’t here, but the rest of the story is.</p>
    <div class="btn-row"><a class="btn btn-sand" href="/">Back to the beginning</a><a class="btn btn-line" href="/gallery/">View the gallery</a></div>
  </div>
</section>
{footer()}"""
    write("404.html", body.replace('href="#contact"', 'href="/#contact"'))


def redirect(rel, target):
    write(rel, f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Aikhoje Studios — Love written in light</title>
<link rel="canonical" href="{SITE}{target.split('#')[0]}">
<meta name="robots" content="noindex, follow">
<meta http-equiv="refresh" content="0; url={target}">
<script>location.replace("{target}");</script>
</head>
<body>
<p>This page has moved. <a href="{target}">Continue to Aikhoje Studios</a>.</p>
</body>
</html>
""")


def sitemap():
    urls = [(f"{SITE}/", "1.0"), (f"{SITE}/gallery/", "0.9")] + [(f"{SITE}/{a['slug']}/", "0.8") for a in AREAS]
    urls += [(f"{SITE}/real-estate/", "0.5")]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, pri in urls:
        lines += ["  <url>", f"    <loc>{loc}</loc>", f"    <lastmod>{TODAY}</lastmod>",
                  "    <changefreq>monthly</changefreq>", f"    <priority>{pri}</priority>", "  </url>"]
    lines.append("</urlset>")
    write("sitemap.xml", "\n".join(lines) + "\n")


if __name__ == "__main__":
    for a in AREAS:
        for k in a["gallery"] + [a["hero"], a["intro_img"]]:
            assert k in PHOTOS, f"{a['slug']}: unknown photo {k}"
    homepage()
    gallery_page()
    for a in AREAS:
        area_page(a)
    not_found()
    redirect("engagements/index.html", "/gallery/")
    redirect("family/index.html", "/gallery/")
    sitemap()
