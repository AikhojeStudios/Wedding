#!/usr/bin/env python3
"""Build the area landing pages (e.g. /outer-banks-wedding-photographer/) from index.html.

Each page reuses the homepage's styles, inquiry form, footer and script, and swaps in
area-specific copy, a curated gallery and its own schema. Edit AREAS below, then run:

    python3 scripts/build-area-pages.py

and commit the generated folders plus sitemap.xml.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://aikhojestudios.com"
TODAY = "2026-11-07"

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

src = (ROOT / "index.html").read_text()

# ---- pieces lifted from the homepage -------------------------------------------------
style = re.search(r"<style>.*?</style>", src, re.S).group(0)
style = style.replace('url("fonts/', 'url("/fonts/')
font_preloads = "\n".join(re.findall(r'<link rel="preload" href="fonts/[^>]+>', src)).replace('href="fonts/', 'href="/fonts/')
verification = "\n".join(re.findall(r'<meta name="(?:google-site-verification|p:domain_verify)"[^>]+>', src))

gallery_items = {}
for li in re.findall(r'<li><button type="button" class="masonry-item".*?</li>', src):
    key = re.search(r'data-full="images/([^"]+)\.jpg"', li).group(1)
    gallery_items[key] = li


def img_attrs(key):
    li = gallery_items[key]
    out = {}
    for attr in ("srcset", "width", "height", "alt"):
        out[attr] = re.search(attr + r'="([^"]*)"', li).group(1)
    return out


cta_to_footer = re.search(r'<section class="cta" id="contact".*?</footer>', src, re.S).group(0)
tail = re.search(r'<a class="mobile-inquire".*?</body>', src, re.S).group(0)
business = json.loads(re.search(r'application/ld\+json">(.*?)</script>', src, re.S).group(1))["@graph"][0]


def absolutize(s):
    s = s.replace('src="images/', 'src="/images/').replace('data-full="images/', 'data-full="/images/')
    s = re.sub(r'(srcset="|, )images/', r'\1/images/', s)
    return s


def esc(s):
    return html.escape(s, quote=True)


def page(a):
    url = f"{SITE}/{a['slug']}/"
    hero = img_attrs(a["hero"])
    intro_img = img_attrs(a["intro_img"])
    others = [o for o in AREAS if o["slug"] != a["slug"]]
    other_links = ", ".join(f'<a href="/{o["slug"]}/">{esc(o["name"])}</a>' for o in others)
    notes = "\n".join(
        f"    <li>\n      <h3>{esc(h)}</h3>\n      <p>{esc(p)}</p>\n    </li>" for h, p in a["notes"]
    )
    gallery = "\n".join("            " + gallery_items[k] for k in a["gallery"])
    intro_ps = "\n    ".join(f"<p>{esc(p)}</p>" for p in a["intro"])

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": url + "#webpage",
                "url": url,
                "name": a["title"],
                "description": a["desc"],
                "isPartOf": {"@id": f"{SITE}/#website"},
                "about": {"@id": url + "#service"},
                "breadcrumb": {"@id": url + "#breadcrumb"},
                "inLanguage": "en-US",
            },
            {
                "@type": "Service",
                "@id": url + "#service",
                "name": f"{a['name']} wedding photography and film",
                "serviceType": "Wedding photography and videography",
                "areaServed": {"@type": "Place", "name": a["region"]},
                "provider": {
                    "@type": ["Photographer", "LocalBusiness"],
                    "@id": f"{SITE}/#business",
                    "name": business["name"],
                    "url": business["url"],
                    "image": business["image"],
                    "email": business["email"],
                    "address": business["address"],
                    "sameAs": business.get("sameAs", []),
                },
            },
            {
                "@type": "BreadcrumbList",
                "@id": url + "#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Aikhoje Studios", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": f"{a['name']} Wedding Photographer", "item": url},
                ],
            },
        ],
    }

    cta = cta_to_footer.replace(
        '<input type="hidden" name="_subject" value="New wedding inquiry from your website">',
        f'<input type="hidden" name="_subject" value="New wedding inquiry from your website ({esc(a["name"])} page)">\n'
        f'    <input type="hidden" name="Inquiry Page" value="{esc(a["name"])}">',
    )
    cta = absolutize(cta)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(a['title'])}</title>
<meta name="description" content="{esc(a['desc'])}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#111010">
{verification}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Aikhoje Studios">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(a['title'])}">
<meta property="og:description" content="{esc(a['desc'])}">
<meta property="og:image" content="{SITE}/images/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(a['title'])}">
<meta name="twitter:description" content="{esc(a['desc'])}">
<meta name="twitter:image" content="{SITE}/images/og.jpg">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<script>document.documentElement.classList.add("js");</script>
{font_preloads}
<!-- Generated by scripts/build-area-pages.py from index.html. Edit the script, not this file. -->
<script type="application/ld+json">
{json.dumps(schema, indent=2, ensure_ascii=False)}
</script>
{style}
</head>
<body>

<a class="skip-link" href="#content">Skip to content</a>

<nav id="nav" aria-label="Primary">
  <a href="/" class="logo">Aikhoje Studios</a>
  <button type="button" class="nav-toggle" id="nav-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
  <ul class="nav-links" id="site-nav">
    <li><a href="#gallery">Gallery</a></li>
    <li><a href="/#film">Film</a></li>
    <li><a href="#contact">Inquire</a></li>
  </ul>
</nav>

<main id="content">
<section class="hero">
  <div class="hero-media">
    <img
      src="/images/{a['hero']}.jpg"
      srcset="{absolutize('srcset="' + hero['srcset'] + '"')[8:-1]}"
      sizes="100vw"
      width="{hero['width']}"
      height="{hero['height']}"
      alt="{esc(hero['alt'])}"
      fetchpriority="high"
      decoding="async">
  </div>
  <div class="hero-overlay"></div>
  <div class="hero-content">
    <p class="hero-eyebrow">Aikhoje Studios &middot; {esc(a['name'])}</p>
    <h1 class="hero-title">{esc(a['name'])} Wedding<br><em>Photographer &amp; Film</em></h1>
    <p class="hero-sub">{esc(a['hero_sub'])}</p>
    <p class="hero-place">Editorial &amp; documentary &middot; since 2015 &middot; available worldwide</p>
    <div class="hero-actions">
      <a href="#contact" class="hero-btn hero-btn-fill">Inquire About Your Date</a>
      <a href="#gallery" class="hero-btn">View the Work</a>
    </div>
  </div>
</section>

<section class="intro" aria-labelledby="approach-title">
  <div class="intro-text">
    <p class="eyebrow">{esc(a['name'])} Weddings</p>
    <h2 id="approach-title" class="section-title">{a['intro_h']}</h2>
    {intro_ps}
  </div>
  <div class="intro-img">
    <img
      src="/images/{a['intro_img']}.jpg"
      srcset="{absolutize('srcset="' + intro_img['srcset'] + '"')[8:-1]}"
      sizes="(max-width: 900px) 100vw, 50vw"
      width="{intro_img['width']}"
      height="{intro_img['height']}"
      alt="{esc(intro_img['alt'])}"
      loading="lazy"
      decoding="async">
  </div>
</section>

<section class="areas" id="areas" aria-labelledby="areas-title">
  <div>
    <p class="eyebrow">Good to Know</p>
    <h2 id="areas-title" class="section-title">{esc(a['notes_h'])}</h2>
    <p class="areas-copy">{esc(a['notes_copy'])} I also photograph weddings in {other_links}, and anywhere your day takes you. <a href="/">See the full portfolio</a>.</p>
  </div>
  <ul class="area-list">
{notes}
  </ul>
</section>

<section class="gallery" id="gallery" aria-labelledby="gallery-title">
  <div class="gallery-header">
    <p class="eyebrow">Selected Work</p>
    <h2 id="gallery-title" class="section-title">The Gallery</h2>
    <p class="gallery-sub">A selection of weddings, elopements, and love stories.</p>
  </div>
  <ul class="masonry" id="masonry">
{absolutize(gallery)}
  </ul>
</section>
{cta}
{tail}
</html>
"""


# Sanity check: the gallery wrapper markup on the homepage must match what we emit.
assert '<ul class="masonry" id="masonry">' in src, "homepage gallery markup changed; update the template"

for a in AREAS:
    for k in a["gallery"] + [a["hero"], a["intro_img"]]:
        assert k in gallery_items, f"{a['slug']}: unknown image {k}"
    out = ROOT / a["slug"] / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page(a))
    print("wrote", out.relative_to(ROOT))

urls = [(f"{SITE}/", "1.0")] + [(f"{SITE}/{a['slug']}/", "0.8") for a in AREAS]
# Standalone sections that live alongside the wedding pages (not generated here).
urls += [(f"{SITE}/real-estate/", "0.5")]
sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for loc, pri in urls:
    sitemap += ["  <url>", f"    <loc>{loc}</loc>", f"    <lastmod>{TODAY}</lastmod>",
                "    <changefreq>monthly</changefreq>", f"    <priority>{pri}</priority>", "  </url>"]
sitemap.append("</urlset>")
(ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n")
print("wrote sitemap.xml")
