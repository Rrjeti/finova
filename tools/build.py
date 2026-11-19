#!/usr/bin/env python3
"""Finova static-site builder.

Generates every .html page in the repository root from the shared partials
below (header, footer, SEO tags, structured data). Edit the content here and run:

    python3 tools/build.py

No dependencies beyond Python 3.8+.
"""
import json, os, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ------------------------------------------------------------------ site data
SITE = "https://finova-ks.com"          # <- change if the domain is different
NAME = "Finova"
PHONE = "+383 44 123 456"
PHONE_RAW = "+38344123456"
EMAIL = "info@finova-ks.com"
STREET = "Rr. Agim Ramadani 15"
CITY = "Prishtinë"
ZIP = "10000"
GEO = (42.6600, 21.1600)                 # <- set exact office coordinates
FOUNDED = "2011"
MAP_EMBED = "https://www.google.com/maps?q=Rr.+Agim+Ramadani+15,+Prishtin%C3%AB&output=embed"
MAP_LINK = "https://www.google.com/maps/search/?api=1&query=Rr.+Agim+Ramadani+15%2C+Prishtin%C3%AB"
SOCIAL = {  # add real profile URLs; empty ones are hidden
    "linkedin": "",
    "facebook": "",
    "instagram": "",
}

# ------------------------------------------------------------------ icons
I = {
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "doc": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h4"/>',
 "book": '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 21V5M9 7h6"/>',
 "percent": '<path d="M19 5 5 19"/><circle cx="7" cy="7" r="2.5"/><circle cx="17" cy="17" r="2.5"/>',
 "wallet": '<rect x="3" y="6" width="18" height="14" rx="3"/><path d="M3 10h18M16 15h2"/>',
 "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
 "check": '<path d="M5 12l5 5 9-10"/>',
 "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="m3 7 9 6 9-6"/>',
 "pin": '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
 "lock": '<rect x="4" y="10" width="16" height="11" rx="3"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
 "bell": '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 8 3 8H3s3-1 3-8"/><path d="M10 20a2 2 0 0 0 4 0"/>',
 "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2 20c0-3.5 3-6 7-6s7 2.5 7 6"/><circle cx="17" cy="7" r="2.5"/><path d="M22 18c0-2.5-2-4.5-5-4.5"/>',
 "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
 "store": '<path d="M4 9l1.5-5h13L20 9M4 9v11h16V9M4 9h16M9 20v-6h6v6"/>',
 "factory": '<path d="M3 21V10l6 4V10l6 4V6l6 3v12z"/><path d="M7 17h2M12 17h2M17 17h2"/>',
 "crane": '<path d="M5 21V4l14 4H5M9 21h6M12 8v6M10 14h4v3h-4z"/>',
 "brief": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 13h18"/>',
 "heart": '<path d="M12 20s-8-4.8-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 9c0 6.2-8 11-8 11z"/>',
 "rocket": '<path d="M12 15l-3-3c1-5 4.5-8.5 11-9-.5 6.5-4 10-9 11z"/><path d="M9 12H5l3-4h4M12 15v4l4-3v-4M6 18c-1 1-1.5 3-1.5 3s2-.5 3-1.5"/>',
 "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
 "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 "up": '<path d="M12 19V5M6 11l6-6 6 6"/>',
 "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z" fill="currentColor" stroke="none"/>',
 "linkedin": '<path d="M4 9h4v11H4zM6 3a2 2 0 1 1 0 4 2 2 0 0 1 0-4zM10 9h4v1.6c.6-1 1.9-1.9 3.8-1.9 3.4 0 4.2 2.2 4.2 5V20h-4v-5.4c0-1.3 0-3-1.8-3S14 13 14 14.5V20h-4z" fill="currentColor" stroke="none"/>',
 "facebook": '<path d="M14 8h3V4h-3a4 4 0 0 0-4 4v2H7v4h3v8h4v-8h3l1-4h-4V8.5c0-.3.2-.5.5-.5z" fill="currentColor" stroke="none"/>',
 "instagram": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/>',
}
def ic(name, size=None, cls=""):
    s = f' width="{size}" height="{size}"' if size else ""
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c}{s} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[name]}</svg>')
ARROW = ic("arrow")

LOGO = ('<svg viewBox="398 370 1206 352" role="img" aria-label="Finova"><g fill="currentColor" fill-rule="evenodd">'
 '<path d="M430,712 L430,520 L402,520 L402,460 L430,460 A90,85 0 0 1 520,375 L555,375 L555,442 L520,442 A23,18 0 0 0 497,460 L555,460 L555,520 L497,520 L497,712 Z"/>'
 '<path d="M570,548 L638,518 L638,712 L570,712 Z"/>'
 '<path d="M654,712 L654,460 L770,460 A108,108 0 0 1 878,568 L878,712 L810,712 L810,572 A44,44 0 0 0 722,572 L722,712 Z"/>'
 '<path d="M890,586 a133,133 0 1 0 266,0 a133,133 0 1 0 -266,0 Z M962,586 a61,61 0 1 0 122,0 a61,61 0 1 0 -122,0 Z"/>'
 '<path d="M1132,460 L1202,460 L1249,595 L1297,460 L1367,460 L1282,712 L1215,712 Z"/>'
 '<path d="M1531,460 L1600,460 L1600,712 L1531,712 L1531,701 A130,130 0 1 1 1531,471 Z M1409,586 a61,61 0 1 0 122,0 a61,61 0 1 0 -122,0 Z"/>'
 '</g><path fill="#27E39A" d="M570,460 L638,460 L638,494 L570,524 Z"/></svg>')

IMG = {  # name: (full w, h, small w, h)
 "accountant": (1125, 750, 640, 427), "audit": (1125, 750, 640, 427), "payroll": (1125, 750, 640, 427),
 "tax": (1125, 750, 640, 427), "advice": (500, 750, 400, 600), "calc": (500, 750, 400, 600),
 "meeting": (1260, 709, 640, 360), "team": (1260, 709, 640, 360),
}
def img(name, alt, sizes="(max-width: 820px) 100vw, 50vw", eager=False, cls=""):
    w, h, sw, sh = IMG[name]
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="images/{name}.webp" srcset="images/{name}-sm.webp {sw}w, images/{name}.webp {w}w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{H.escape(alt)}" {load} decoding="async">')

# ------------------------------------------------------------------ structured data
BUSINESS = {
  "@type": ["AccountingService", "ProfessionalService"],
  "@id": f"{SITE}/#business",
  "name": NAME,
  "alternateName": "Finova Auditim & Kontabilitet",
  "description": "Kompani auditimi, kontabiliteti dhe këshillimi tatimor në Prishtinë, Kosovë. Auditues të licencuar nga KKRF.",
  "url": f"{SITE}/",
  "logo": f"{SITE}/images/logo.png",
  "image": f"{SITE}/images/og-image.png",
  "telephone": PHONE_RAW,
  "email": EMAIL,
  "foundingDate": FOUNDED,
  "priceRange": "€€",
  "currenciesAccepted": "EUR",
  "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": CITY,
              "postalCode": ZIP, "addressCountry": "XK"},
  "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]},
  "areaServed": [{"@type": "Country", "name": "Kosovë"}, {"@type": "Place", "name": "Diaspora shqiptare"}],
  "availableLanguage": ["sq", "en"],
  "knowsAbout": ["Auditim statutor", "Kontabilitet", "Tatimi mbi vlerën e shtuar (TVSH)", "Tatimi në fitim",
                 "Pagat dhe kontributet pensionale", "SNRF / IFRS", "Standardet Ndërkombëtare të Auditimit (SNA/ISA)",
                 "Due diligence", "Vlerësim biznesi"],
  "openingHoursSpecification": [
    {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
     "opens": "08:00", "closes": "16:30"},
    {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "13:00"}],
  "contactPoint": {"@type": "ContactPoint", "telephone": PHONE_RAW, "email": EMAIL,
                   "contactType": "customer service", "availableLanguage": ["sq", "en"]},
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Shërbimet e Finova", "itemListElement": [
     {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "url": f"{SITE}/sherbimet.html#{a}"}}
     for n, a in [("Auditim", "auditim"), ("Kontabilitet", "kontabilitet"), ("Këshillim tatimor", "tatime"),
                  ("Pagat", "pagat"), ("Këshillim financiar", "keshillim")]]},
}
sameas = [u for u in SOCIAL.values() if u]
if sameas: BUSINESS["sameAs"] = sameas
WEBSITE = {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": NAME,
           "inLanguage": "sq", "publisher": {"@id": f"{SITE}/#business"}}

def faq_ld(items):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

def crumbs_ld(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": f"{SITE}/{u}"} for i, (n, u) in enumerate(trail)]}

# ------------------------------------------------------------------ partials
NAV = [("index.html", "Ballina"), ("sherbimet.html", "Shërbimet"), ("rreth-nesh.html", "Rreth nesh"), ("kontakt.html", "Kontakt")]

def head(title, desc, path, ld=(), page_type="WebPage", preload=None, noindex=False):
    url = f"{SITE}/{'' if path == 'index.html' else path}"
    graph = [BUSINESS, WEBSITE, {"@type": page_type, "@id": url + "#webpage", "url": url, "name": title,
             "description": desc, "inLanguage": "sq", "isPartOf": {"@id": f"{SITE}/#website"},
             "about": {"@id": f"{SITE}/#business"}}] + list(ld)
    ld_json = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    pre = ""
    if preload:
        n = preload; w, h, sw, sh = IMG[n]
        pre = (f'<link rel="preload" as="image" href="images/{n}.webp" imagesrcset="images/{n}-sm.webp {sw}w, '
               f'images/{n}.webp {w}w" imagesizes="(max-width: 1080px) 100vw, 33vw">\n')
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large, max-snippet:-1"
    return f'''<!doctype html>
<html lang="sq" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{H.escape(title)}</title>
<meta name="description" content="{H.escape(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="sq" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta name="theme-color" content="#0B1E62">
<meta name="format-detection" content="telephone=no">
<meta name="geo.region" content="XK"><meta name="geo.placename" content="{CITY}">
<meta name="geo.position" content="{GEO[0]};{GEO[1]}"><meta name="ICBM" content="{GEO[0]}, {GEO[1]}">
<meta property="og:type" content="website">
<meta property="og:locale" content="sq_AL">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{H.escape(title)}">
<meta property="og:description" content="{H.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/images/og-image.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Finova: auditim, kontabilitet dhe këshillim tatimor në Prishtinë">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{H.escape(title)}">
<meta name="twitter:description" content="{H.escape(desc)}">
<meta name="twitter:image" content="{SITE}/images/og-image.png">
<link rel="icon" href="images/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="images/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preload" href="assets/fonts/poppins-800.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/poppins-400.woff2" as="font" type="font/woff2" crossorigin>
{pre}<link rel="stylesheet" href="assets/css/style.css">
<script>document.documentElement.className='js'</script>
<script src="assets/js/main.js" defer></script>
<script type="application/ld+json">{ld_json}</script>
</head>
<body>
<a class="skip" href="#main">Kalo te përmbajtja</a>
<div class="progress" aria-hidden="true"></div>
'''

def header(active):
    links = "".join(f'<a href="{u}"{" aria-current=page" if u == active else ""}>{t}</a>' for u, t in NAV)
    dlinks = "".join(f'<a href="{u}"{" aria-current=page" if u == active else ""}>{t}<small>0{i+1}</small></a>' for i, (u, t) in enumerate(NAV))
    return f'''<header class="site-header">
  <div class="bar"><div class="inner">
    <a class="logo" href="index.html" aria-label="Finova, ballina">{LOGO}</a>
    <nav class="nav" aria-label="Kryesore">{links}</nav>
    <div class="header-cta">
      <a class="btn btn--white btn--sm" href="kontakt.html">Takim falas {ARROW}</a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Hap menunë"><span></span></button>
    </div>
  </div></div>
</header>
<div class="drawer" id="drawer" aria-hidden="true">
  <nav aria-label="Menuja mobile">{dlinks}<a href="privatesia.html">Privatësia<small>05</small></a></nav>
  <div class="drawer-foot">
    <a class="btn" href="kontakt.html">Rezervo takimin falas {ARROW}</a>
    <a class="btn btn--glass" href="tel:{PHONE_RAW}">{ic("phone")} {PHONE}</a>
  </div>
</div>
'''

def footer():
    soc = "".join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{k.title()}">{ic(k)}</a>' for k, u in SOCIAL.items() if u)
    soc_html = f'<div class="socials">{soc}</div>' if soc else ""
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="top">
      <div class="col brand" data-reveal="up">
        <a class="logo" href="index.html" aria-label="Finova, ballina" style="margin-bottom:6px">{LOGO}</a>
        <p>Auditim, kontabilitet dhe këshillim tatimor në Prishtinë. Saktësi me qasje njerëzore, për bizneset në Kosovë dhe në diasporë.</p>
        {soc_html}
      </div>
      <div class="col" data-reveal="up" style="--d:.08s"><span class="ttl">Shërbimet</span>
        <a href="sherbimet.html#auditim">Auditim</a><a href="sherbimet.html#kontabilitet">Kontabilitet</a>
        <a href="sherbimet.html#tatime">Këshillim tatimor</a><a href="sherbimet.html#pagat">Pagat</a><a href="sherbimet.html#keshillim">Këshillim financiar</a></div>
      <div class="col" data-reveal="up" style="--d:.16s"><span class="ttl">Kompania</span>
        <a href="rreth-nesh.html">Rreth nesh</a><a href="rreth-nesh.html#ekipi">Ekipi</a><a href="index.html#procesi">Procesi</a>
        <a href="sherbimet.html#pyetje">Pyetje të shpeshta</a><a href="kontakt.html">Kontakt</a></div>
      <div class="col" data-reveal="up" style="--d:.24s"><span class="ttl">Kontakt</span>
        <address style="font-style:normal;display:grid;gap:12px">
          <a href="{MAP_LINK}" target="_blank" rel="noopener">{STREET}, {ZIP} {CITY}</a>
          <a href="mailto:{EMAIL}">{EMAIL}</a>
          <a href="tel:{PHONE_RAW}">{PHONE}</a>
        </address>
        <span>E hënë – E premte · 08:00 – 16:30</span></div>
    </div>
    <div class="bottom">
      <span>© <span data-year>2026</span> Finova. Të gjitha të drejtat e rezervuara.</span>
      <span><a href="privatesia.html">Politika e privatësisë</a> · <a href="privatesia.html#kushtet">Kushtet e përdorimit</a></span>
    </div>
  </div>
  <div class="chips" aria-hidden="true"></div>
</footer>
<div class="mbar" aria-label="Veprime të shpejta">
  <a href="tel:{PHONE_RAW}">{ic("phone")} Telefono</a>
  <a href="kontakt.html">Takim falas {ARROW}</a>
</div>
<button class="to-top" type="button" aria-label="Kthehu në krye">{ic("up")}</button>
</body>
</html>
'''

def cta(title="Gati për një bilanc që barazohet?", text="Takimi i parë është falas. Na tregoni ku jeni, ne ju tregojmë rrugën."):
    return f'''<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="cta" data-reveal="mask">
      <div class="stack">
        <span class="eyebrow eyebrow--dark"><i class="dot"></i> Takimi i parë falas</span>
        <h2 data-split>{title}</h2>
        <p class="lead">{text}</p>
        <div class="cta-actions">
          <a class="btn" href="kontakt.html">Rezervo takimin {ARROW}</a>
          <a class="btn btn--glass" href="tel:{PHONE_RAW}">{ic("phone")} {PHONE}</a>
        </div>
      </div>
      <div class="seal" aria-hidden="true">
        <svg class="rot" viewBox="0 0 200 200"><defs><path id="sealPath" d="M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0"/></defs>
          <circle cx="100" cy="100" r="96" fill="rgba(255,255,255,.06)" stroke="rgba(255,255,255,.25)"/>
          <text fill="#fff" font-size="13" font-weight="600" letter-spacing="5"><textPath href="#sealPath">AUDITIM · KONTABILITET · TATIME · PAGAT ·</textPath></text></svg>
        <div class="mid glass sheen"><span><b>15+</b>vite<br>besim</span></div>
      </div>
    </div>
  </div>
</section>
'''

def faq_html(items):
    return '<div class="faq" data-stagger=".08">' + "".join(
        f'<details data-reveal="up"><summary>{H.escape(q)}<i aria-hidden="true"></i></summary><div class="ans">{H.escape(a)}</div></details>'
        for q, a in items) + '</div>'

def write(name, content):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", name, len(content.encode()) // 1024, "KB")

# ------------------------------------------------------------------ content
SERVICES = [
 ("auditim", "Auditim", "doc", "audit", "Opinion i pavarur mbi pasqyrat tuaja",
  "Auditim statutor dhe vullnetar i pasqyrave financiare, sipas Standardeve Ndërkombëtare të Auditimit (SNA). Afër klientit, por gjithmonë të pavarur: kështu ndërtojmë besimin te bankat, investitorët dhe institucionet.",
  ["Auditim statutor", "Auditim i brendshëm", "Rishikim i pasqyrave", "Procedura të dakorduara"], ("3–6", "javë deri te raporti")),
 ("kontabilitet", "Kontabilitet", "book", "accountant", "Libra të rregullt, çdo muaj",
  "Mbajtja e librave, regjistrimi i transaksioneve dhe pasqyra mujore që i kuptoni pa qenë kontabilist. Raportim sipas SNRF/IFRS dhe Standardeve të Kosovës.",
  ["Mbajtja e librave", "Pasqyra mujore", "Pasqyrat vjetore", "Raporte për menaxhmentin"], ("10", "ditë pas fundmuajit")),
 ("tatime", "Këshillim tatimor", "percent", "tax", "Deklarime në kohë, pa surpriza",
  "Planifikim tatimor, deklarime periodike në EDI dhe përfaqësim para Administratës Tatimore të Kosovës (ATK). Ju kujtojmë çdo afat para se të bëhet problem.",
  ["TVSH dhe tatimi në fitim", "Planifikim tatimor", "Përfaqësim në ATK", "Çmimet e transferimit"], ("24h", "kujtesë para çdo afati")),
 ("pagat", "Pagat", "wallet", "payroll", "Paga të sakta, çdo herë",
  "Llogaritja e pagave, tatimi në paga, kontributet pensionale në Trust dhe raportimi mujor për stafin tuaj, me konfidencialitet të plotë.",
  ["Llogaritja e pagave", "Kontributet pensionale", "Raportimi mujor", "Kontratat e punës"], ("100%", "konfidenciale")),
 ("keshillim", "Këshillim financiar", "chart", "advice", "Vendime të bazuara në numra",
  "Buxhetim, analiza e rrjedhës së parasë, vlerësim biznesi dhe mbështetje për investime e financime bankare.",
  ["Buxhetim dhe parashikim", "Analiza e cash-flow", "Vlerësim biznesi", "Due diligence"], ("1", "partner për çdo vendim")),
]

FAQ_HOME = [
 ("Çfarë shërbimesh ofron Finova?", "Finova ofron auditim statutor dhe të brendshëm, kontabilitet mujor, këshillim tatimor dhe përfaqësim në ATK, llogaritje pagash e kontributesh pensionale, si dhe këshillim financiar (buxhetim, cash-flow, vlerësim biznesi dhe due diligence) për biznese në Kosovë dhe në diasporë."),
 ("A janë auditorët tuaj të licencuar?", "Po. Auditorët tanë janë të licencuar nga Këshilli i Kosovës për Raportim Financiar (KKRF) dhe punojmë sipas Standardeve Ndërkombëtare të Auditimit (SNA/ISA) dhe SNRF/IFRS."),
 ("Sa kushton kontabiliteti mujor për një biznes të vogël?", "Çmimi varet nga numri i transaksioneve, punonjësve dhe nga detyrimet tatimore (p.sh. nëse jeni në sistemin e TVSH-së). Pas takimit të parë falas, ju dërgojmë një ofertë fikse mujore brenda 48 orëve, pa kosto të fshehura."),
 ("A punoni me biznese nga diaspora?", "Po. Shumë klientë tanë drejtojnë biznese në Kosovë nga jashtë vendit. Komunikojmë online, dokumentet i ndajmë në mënyrë të sigurt dhe raportet i dërgojmë në shqip ose anglisht."),
 ("Ku ndodhet zyra e Finova?", f"Zyra jonë ndodhet në {STREET}, {ZIP} {CITY}. Jemi të hapur të hënën deri të premten 08:00–16:30 dhe të shtunën 09:00–13:00."),
]
FAQ_SVC = [
 ("Sa kushton një auditim?", "Çmimi varet nga madhësia e biznesit, numri i transaksioneve dhe kompleksiteti i pasqyrave. Pas takimit të parë falas, ju dërgojmë një ofertë fikse brenda 48 orëve."),
 ("Sa zgjat procesi i auditimit?", "Për shumicën e bizneseve, nga takimi i parë deri te raporti përfundimtar kalojnë 3 deri në 6 javë."),
 ("A mund të punoni me sistemin tonë kontabël?", "Po. Punojmë me shumicën e programeve kontabël që përdoren në Kosovë, si dhe me Excel. Nëse keni sistem tjetër, ne përshtatemi."),
 ("A ofroni shërbime për biznese të vogla?", "Sigurisht. Kemi paketa mujore për biznese të vogla dhe startup-e, që përfshijnë kontabilitetin, pagat dhe deklarimet tatimore."),
 ("Si e ndërroj kontabilistin pa humbur të dhëna?", "Ne kujdesemi për gjithçka: marrim librat dhe dokumentet nga kontabilisti i mëparshëm, kontrollojmë saldot hapëse dhe sigurohemi që asnjë deklaratë të mos mbetet pa u dorëzuar gjatë kalimit."),
 ("A më përfaqësoni në rast kontrolli nga ATK?", "Po. Përgatisim dokumentacionin, ju shoqërojmë gjatë kontrollit dhe, nëse duhet, hartojmë ankesat dhe përgjigjet zyrtare ndaj Administratës Tatimore të Kosovës."),
]
FAQ_CONTACT = [
 ("A është takimi i parë vërtet falas?", "Po. Takimi i parë (30–45 minuta, në zyrë ose online) është pa pagesë dhe pa asnjë detyrim."),
 ("Sa shpejt më ktheni përgjigje?", "Brenda 24 orëve të punës. Për afate urgjente tatimore, na telefononi direkt."),
 ("Çfarë dokumentesh duhet të sjell?", "Certifikatën e regjistrimit të biznesit, pasqyrat e fundit financiare (nëse i keni) dhe deklaratat e fundit tatimore. Nëse nuk i keni, nisim nga e para bashkë."),
]

STANDARDS = ["SNRF / IFRS", "SNA / ISA", "Licencuar nga KKRF", "Deklarime në EDI · ATK", "Trusti Pensional", "TVSH", "Tatimi në fitim", "Çmimet e transferimit", "Due diligence"]

# ------------------------------------------------------------------ pages
def page_index():
    pillars = "".join(f'''<div class="p" data-reveal="up"><span class="icon icon--glass">{ic(i)}</span><h3>{t}</h3><p>{d}</p></div>''' for i, t, d in [
        ("doc", "Auditim", "Auditim i pavarur i pasqyrave financiare, sipas standardeve ndërkombëtare."),
        ("book", "Kontabilitet", "Libra të rregullt, pasqyra mujore dhe raporte që lexohen lehtë."),
        ("percent", "Këshillim tatimor", "Deklarime në kohë dhe planifikim tatimor pa surpriza.")])
    marquee = "".join(f"<span>{s}</span>" for s in STANDARDS * 2)
    svc_cards = "".join(f'''<a class="svc-card" href="sherbimet.html#{a}" data-reveal="flip">
        {img(im, t, "(max-width: 600px) 100vw, (max-width: 1080px) 50vw, 33vw")}
        <div class="glass"><span class="num">0{n+1}</span><h3>{t}</h3><p>{sub}</p>
        <span class="more">Mëso më shumë <i>{ic("arrow")}</i></span></div></a>''' for n, (a, t, _, im, sub, *_r) in enumerate(SERVICES[:3]))
    quotes = "".join(f'''<figure class="quote glass-light" data-reveal="up">
        <div class="stars" aria-label="5 nga 5">{ic("star")*5}</div>
        <blockquote>“{q}”</blockquote>
        <footer><img src="images/{av}.webp" width="46" height="46" alt="" loading="lazy"><div><b>{n}</b><span>{r}</span></div></footer></figure>''' for q, n, r, av in [
        ("Për herë të parë i kuptojmë pasqyrat tona. Raporti mujor është një faqe, jo dhjetë tabela.", "Blerina H.", "Drejtoreshë, kompani tregtare", "av1"),
        ("Auditimi përfundoi në kohë për aplikimin në bankë. Profesionalë dhe gjithmonë të arritshëm.", "Arben G.", "Pronar, kompani ndërtimi", "av2"),
        ("Si biznes në diasporë, kishim nevojë për dikë të besueshëm në Kosovë. Finova është ai partner.", "Leart M.", "Themelues, startup IT", "av3")])
    cal = "".join(f'''<div class="cal-item glass" data-reveal="zoom"><div class="day"><b>{d}</b><span>{m}</span></div><h3>{t}</h3><p>{x}</p></div>''' for d, m, t, x in [
        ("15", "çdo muaj", "Tatimi në paga & Trusti", "Deklarimi dhe pagesa e tatimit në paga dhe kontributeve pensionale për muajin e kaluar."),
        ("20", "çdo muaj", "Deklarata e TVSH-së", "Deklarimi dhe pagesa e TVSH-së për periudhën e kaluar, përmes EDI."),
        ("15", "pas tremujorit", "Kësti i tatimit në fitim", "Pagesat tremujore paraprake të tatimit në fitim të korporatave."),
        ("31", "mars", "Deklarata vjetore", "Deklarata vjetore e tatimit në fitim dhe pasqyrat financiare për vitin e kaluar.")])
    steps = "".join(f'''<div class="step" data-step><span class="n">0{i+1}</span><div><h3>{t}</h3><p>{d}</p></div></div>''' for i, (t, d) in enumerate([
        ("Takimi", "Dëgjojmë biznesin tuaj dhe kuptojmë ku ndodhen numrat sot."),
        ("Analiza", "Shqyrtojmë dokumentet dhe identifikojmë rreziqet e mundësitë."),
        ("Raporti", "Dorëzojmë gjetjet në gjuhë të qartë, me hapa konkretë."),
        ("Mbështetja", "Mbetemi pranë jush gjatë gjithë vitit fiskal.")]))
    return head("Finova · Auditim, Kontabilitet & Këshillim Tatimor në Prishtinë",
                "Finova ofron auditim të licencuar nga KKRF, kontabilitet mujor, këshillim tatimor dhe pagat për biznese në Kosovë dhe diasporë. Takimi i parë falas.",
                "index.html", [faq_ld(FAQ_HOME)], preload=None) + header("index.html") + f'''
<main id="main">
<section class="hero">
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="blob blob--g" aria-hidden="true"></div><div class="blob blob--b" aria-hidden="true"></div>
  <div class="wrap">
    <div class="hero-copy">
      <span class="eyebrow eyebrow--dark intro" style="--d:.05s"><i class="dot"></i> Fin + Nova · Auditim &amp; Kontabilitet</span>
      <h1 class="intro" style="--d:.15s">Financa,<br>e lexuar <span class="accent underline">ndryshe.</span></h1>
      <p class="lead intro" style="--d:.3s;max-width:540px">Auditim, kontabilitet dhe këshillim tatimor në Prishtinë, për bizneset që duan numra të qartë dhe vendime të sigurta. Saktësi me qasje njerëzore.</p>
      <div class="hero-actions intro" style="--d:.45s">
        <a class="btn" href="kontakt.html">Rezervo një takim falas {ARROW}</a>
        <a class="btn btn--glass" href="sherbimet.html">Shërbimet tona</a>
      </div>
      <div class="hero-meta intro" style="--d:.6s">
        <div><b><span data-count="15">15</span>+</b><small>Vite përvojë</small></div>
        <div><b><span data-count="320">320</span>+</b><small>Biznese klientë</small></div>
        <div class="avatars"><span><img src="images/av1.webp" width="38" height="38" alt=""><img src="images/av2.webp" width="38" height="38" alt=""><img src="images/av3.webp" width="38" height="38" alt=""></span>Auditues të licencuar<br>nga KKRF</div>
      </div>
    </div>
    <div class="scene intro-pop" style="--d:.3s" aria-hidden="true">
      <div class="orbit"><i></i></div><div class="orbit orbit--2"><i></i></div>
      <div data-depth=".4" style="position:absolute;inset:0">
        <div class="core glass sheen">
          <div class="core-head"><span>FITIMI NETO · 2026</span><span class="core-chip">{ic("up",12)} +12%</span></div>
          <div class="core-num">€ 218,420</div>
          <svg class="chart" viewBox="0 0 300 110" preserveAspectRatio="none">
            <defs><linearGradient id="gArea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#27E39A" stop-opacity=".45"/><stop offset="1" stop-color="#27E39A" stop-opacity="0"/></linearGradient></defs>
            <path class="area" d="M0,95 C30,90 45,70 75,72 S120,50 150,55 S200,30 225,34 S270,12 300,8 L300,110 L0,110 Z"/>
            <path class="line" d="M0,95 C30,90 45,70 75,72 S120,50 150,55 S200,30 225,34 S270,12 300,8"/>
          </svg>
          <div class="bars"><i style="height:40%;animation-delay:1.2s"></i><i style="height:55%;animation-delay:1.3s"></i><i style="height:48%;animation-delay:1.4s"></i><i style="height:70%;animation-delay:1.5s"></i><i style="height:62%;animation-delay:1.6s"></i><i style="height:90%;animation-delay:1.7s"></i></div>
        </div>
      </div>
      <div data-depth="1" style="position:absolute;inset:0">
        <div class="float-card glass fc-1"><span class="ic">{ic("shield")}</span><span><b>Raporti i auditit</b><small>Përfunduar · dorëzuar</small></span></div>
      </div>
      <div data-depth="1.4" style="position:absolute;inset:0">
        <div class="float-card glass fc-2"><span class="ic">{ic("check")}</span><span><b>Bilanci u barazua</b><small>Aktivet = Detyrimet + Kapitali</small></span></div>
      </div>
      <div data-depth=".8" style="position:absolute;inset:0">
        <div class="float-card fc-3"><span class="ic">{ic("bell")}</span><span><span data-deadline-day="20"><b>–</b></span><small style="color:inherit;opacity:.8">deri te afati i TVSH-së</small></span></div>
      </div>
    </div>
  </div>
</section>

<section class="overlap">
  <div class="wrap pillars">
    <div class="pill-photo" data-reveal="left">
      {img("meeting", "Ekspertët e Finova në takim me një klient", "(max-width: 1080px) 100vw, 33vw")}
      <a class="glass" href="#procesi"><b>Si punojmë?</b><span class="link" style="color:var(--green)">Shiko procesin {ARROW}</span></a>
    </div>
    <div class="pill-panel" data-stagger=".12">{pillars}</div>
  </div>
</section>

<section class="section" style="padding-bottom:40px">
  <div class="marquee" aria-label="Standardet dhe institucionet me të cilat punojmë"><div class="track">{marquee}</div></div>
</section>

<section class="section" id="rreth" style="padding-top:60px">
  <div class="wrap split">
    <div class="photo-stack" data-reveal="mask">
      <div class="main" data-parallax=".06">{img("team", "Ekipi i Finova në zyrën në Prishtinë", "(max-width: 820px) 100vw, 50vw")}</div>
      <div class="badge" data-reveal="zoom" style="--d:.4s"><b>KKRF</b>Auditues<br>të licencuar</div>
      <div class="note glass-light" data-reveal="up" style="--d:.3s">
        <small>NJË DETAJ. DY KUPTIME.</small>
        <p><b>01 Rritja.</b> E matur, jo e supozuar.</p>
        <p><b>02 Pavarësia.</b> Afër klientit, por gjithmonë i ndarë prej tij.</p>
      </div>
    </div>
    <div class="stack">
      <span class="eyebrow" data-reveal="up">Rreth nesh</span>
      <h2 data-split>Rreptësia e numrave. Qartësia e fjalëve.</h2>
      <p class="lead" data-reveal="up">FIN është disiplina: llogaria, rregulli, përgjegjësia. NOVA është mënyra: e qartë, e shpejtë, njerëzore. Finova i bashkon të dyja në një fjalë, dhe në çdo raport që dorëzojmë.</p>
      <div class="mv" data-stagger=".12">
        <div class="card" data-reveal="up"><h3>Misioni</h3><p>T’u japim bizneseve numra të saktë dhe të kuptueshëm, që vendimet të merren me siguri.</p></div>
        <div class="card" data-reveal="up"><h3>Vizioni</h3><p>Të jemi partneri financiar më i besuar për bizneset në Kosovë dhe në diasporë.</p></div>
      </div>
      <div data-reveal="up"><a class="btn btn--navy" href="rreth-nesh.html">Njihuni me ekipin {ARROW}</a></div>
    </div>
  </div>
</section>

<section class="section stats-bg" style="padding-top:20px" aria-label="Finova në shifra">
  <div class="wrap stats" data-stagger=".1">
    <div class="stat glass-light" data-reveal="up"><b><span data-count="15">15</span><sup>+</sup></b><span>Vite përvojë në auditim</span></div>
    <div class="stat glass-light" data-reveal="up"><b><span data-count="320">320</span><sup>+</sup></b><span>Biznese që na besojnë</span></div>
    <div class="stat glass-light" data-reveal="up"><b><span data-count="1200">1,200</span></b><span>Raporte të dorëzuara</span></div>
    <div class="stat glass-light" data-reveal="up"><b><span data-count="24">24</span></b><span>Ekspertë në ekip</span></div>
  </div>
</section>

<section class="section section--soft">
  <div class="wrap" style="display:grid;gap:48px">
    <div class="head head--split">
      <div><span class="eyebrow" data-reveal="up">Shërbimet</span>
        <h2 data-split>Shërbime financiare që mbajnë bilancin në rregull</h2></div>
      <div class="stack" style="gap:16px;max-width:360px" data-reveal="up">
        <p class="lead">Nga libri i parë kontabël deri te raporti i auditit: një ekip, një standard.</p>
        <a class="btn" href="sherbimet.html">Të gjitha shërbimet {ARROW}</a>
      </div>
    </div>
    <div class="svc" data-stagger=".14">{svc_cards}</div>
  </div>
</section>

<section class="section section--navy on-dark">
  <div class="blob blob--g" aria-hidden="true" style="top:-200px"></div>
  <div class="wrap" style="position:relative;display:grid;gap:48px">
    <div class="head center"><span class="eyebrow eyebrow--dark" data-reveal="up">Pse Finova</span>
      <h2 data-split>Një partner, jo vetëm një kontabilist</h2>
      <p class="lead" data-reveal="up">Bizneset na zgjedhin për saktësinë. Na qëndrojnë për mënyrën si u flasim.</p></div>
    <div class="bento" data-stagger=".1">
      <div class="b-wide glass sheen" data-reveal="up" data-tilt="4">
        <span class="icon icon--glass">{ic("shield")}</span>
        <h3>Të pavarur dhe të licencuar</h3>
        <p>Auditues të licencuar nga KKRF, që punojnë sipas SNA dhe SNRF. Opinioni ynë pranohet nga bankat, donatorët dhe institucionet.</p>
        <div class="tag-row"><span class="tag">SNA / ISA</span><span class="tag">SNRF / IFRS</span><span class="tag">KKRF</span><span class="tag">ATK</span></div>
      </div>
      <div class="b-narrow glass" data-reveal="up" data-tilt="6">
        <h3>Afate të respektuara</h3>
        <svg class="ring" viewBox="0 0 120 120" style="--v:.99"><circle class="bg" cx="60" cy="60" r="50"/><circle class="fg" cx="60" cy="60" r="50"/>
          <text x="60" y="68" text-anchor="middle" fill="#fff" font-size="24" font-weight="800">99%</text></svg>
      </div>
      <div class="b-mid glass" data-reveal="up" data-tilt="5">
        <span class="big">48h</span>
        <h3>Ofertë fikse, pa surpriza</h3>
        <p>Pas takimit të parë, merrni një çmim të qartë brenda 48 orëve. Pa tarifa të fshehura në fund të vitit.</p>
      </div>
      <div class="b-mid glass" data-reveal="up" data-tilt="5">
        <span class="icon icon--glass">{ic("lock")}</span>
        <h3>Të dhëna të sigurta</h3>
        <p>Dokumentet ndahen me kanale të enkriptuara dhe trajtohen me konfidencialitet të plotë, sipas Ligjit për Mbrojtjen e të Dhënave Personale.</p>
      </div>
      <div class="b-narrow glass" data-reveal="up" data-tilt="6">
        <span class="icon icon--glass">{ic("users")}</span>
        <h3>Një kontakt i dedikuar</h3>
        <p>Një ekspert që e njeh biznesin tuaj, jo një qendër thirrjesh.</p>
      </div>
      <div class="b-wide glass" data-reveal="up" data-tilt="4">
        <span class="icon icon--glass">{ic("spark")}</span>
        <h3>Shqip ose anglisht, në zyrë ose online</h3>
        <p>Raporte dygjuhëshe për investitorë të huaj dhe biznese në diasporë. Takime në Prishtinë ose me video, si t’ju përshtatet.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="stack">
      <span class="eyebrow" data-reveal="up">Raportimi</span>
      <h2 data-split>Numrat tuaj, të qartë në çdo ekran</h2>
      <p class="lead" data-reveal="up">Pasqyrat mujore, afatet tatimore dhe dokumentet e auditimit, të përmbledhura në një vend. Pa tabela të pafundme, vetëm ajo që ju duhet për të vendosur.</p>
      <ul class="check" data-stagger=".1">
        <li data-reveal="left">Përmbledhje mujore e fitimit dhe shpenzimeve</li>
        <li data-reveal="left">Kujtesa për çdo afat tatimor</li>
        <li data-reveal="left">Dokumente të ndara në mënyrë të sigurt</li>
      </ul>
      <div data-reveal="up"><a class="btn btn--navy" href="kontakt.html">Kërkoni një demonstrim {ARROW}</a></div>
    </div>
    <div class="phones" data-reveal="tilt" aria-hidden="true">
      <div class="phone phone--back" data-parallax=".08"><div class="screen">
        <small style="opacity:.7;letter-spacing:.14em">CASH-FLOW</small><b style="font-size:24px">€ 27,950</b>
        <svg viewBox="0 0 200 120" style="margin-top:10px"><path d="M0,100 L30,80 L60,88 L90,50 L120,62 L150,30 L200,20" fill="none" stroke="#27E39A" stroke-width="3"/></svg>
        <div class="ph-card" style="background:rgba(255,255,255,.08);color:#fff;margin-top:auto">Të hyrat ↑ 8%</div>
      </div></div>
      <div class="phone phone--front"><div class="screen">
        <span style="opacity:.6">Përshëndetje,</span><b style="font-size:16px;margin-top:-8px">Dardania Trade</b>
        <div class="ph-card dark"><span style="opacity:.7">Fitimi neto · Tetor</span><b>€ 18,420</b><span style="color:var(--green)">+12% nga muaji i kaluar</span></div>
        <div class="ph-row"><div class="ph-card" style="flex:1"><span class="muted">Të hyrat</span><br><strong>€ 64,300</strong></div><div class="ph-card" style="flex:1"><span class="muted">Shpenzimet</span><br><strong>€ 45,880</strong></div></div>
        <div class="ph-card ph-row"><span>Deklarata e TVSH-së</span><span class="ph-pill warn">Afati 20</span></div>
        <div class="ph-card ph-row"><span>Raporti i auditit</span><span class="ph-pill">Gati</span></div>
      </div></div>
      <div class="float-card glass-light fc-a"><span class="ic">{ic("bell")}</span><span><b>Afati tatimor</b><small>pas 7 ditësh</small></span></div>
      <div class="float-card glass-light fc-b"><span class="ic">{ic("check")}</span><span><b>Bilanci u barazua</b><small>Pasqyra e tetorit</small></span></div>
    </div>
  </div>
</section>

<section class="section section--soft" id="procesi">
  <div class="wrap" style="display:grid;gap:56px">
    <div class="head"><span class="eyebrow" data-reveal="up">Procesi</span>
      <h2 data-split>Katër hapa, asnjë boshllëk në llogari</h2></div>
    <div class="process" data-progress>{steps}</div>
  </div>
</section>

<section class="section section--navy on-dark">
  <div class="blob blob--b" aria-hidden="true" style="left:auto;right:-200px;top:-100px"></div>
  <div class="wrap" style="position:relative;display:grid;gap:44px">
    <div class="head head--split">
      <div><span class="eyebrow eyebrow--dark" data-reveal="up">Kalendari tatimor</span>
        <h2 data-split>Afatet që nuk duhet t’i harroni</h2></div>
      <div class="countdown glass" data-reveal="right" data-deadline-day="20">{ic("clock",20)}<span>TVSH-ja e radhës (<span data-deadline-date>20</span>) pas <b>–</b></span></div>
    </div>
    <div class="cal" data-stagger=".1">{cal}</div>
    <p style="font-size:13px;color:rgba(255,255,255,.55)" data-reveal="up">Afatet janë orientuese. Për rastin tuaj specifik, ju njoftojmë ne paraprakisht.</p>
  </div>
</section>

<section class="section">
  <div class="wrap" style="display:grid;gap:48px">
    <div class="head center"><span class="eyebrow" data-reveal="up">Klientët tanë</span>
      <h2 data-split>Çfarë thonë bizneset që punojnë me ne</h2></div>
    <!-- ZËVENDËSONI këto me dëshmi reale (me lejen e klientëve) para publikimit -->
    <div class="quotes" data-stagger=".12">{quotes}</div>
  </div>
</section>

<section class="section section--soft">
  <div class="wrap" style="display:grid;gap:48px">
    <div class="head center"><span class="eyebrow" data-reveal="up">Pyetje të shpeshta</span>
      <h2 data-split>Përgjigje të shpejta para takimit</h2></div>
    {faq_html(FAQ_HOME)}
  </div>
</section>

<div style="height:clamp(72px,10vw,120px)"></div>
{cta()}
</main>
''' + footer()


def page_services():
    blocks = "".join(f'''<article class="svc-block" id="{a}" data-reveal="up">
      <div class="svc-media" data-reveal="mask">{img(im, t, "(max-width: 820px) 100vw, 560px")}
        <div class="glass"><b>{k[0]}</b><span>{k[1]}</span></div></div>
      <div class="svc-body">
        <span class="eyebrow">Shërbimi 0{n+1}</span>
        <h2 data-split style="font-size:clamp(28px,3.4vw,40px)">{t}</h2>
        <p style="font-weight:600;font-size:18px">{sub}</p>
        <p class="lead">{desc}</p>
        <ul class="tags" data-stagger=".06">{"".join(f'<li data-reveal="zoom">{x}</li>' for x in tags)}</ul>
        <div><a class="btn btn--navy" href="kontakt.html?sherbimi={a}">Kërko ofertë {ARROW}</a></div>
      </div></article>''' for n, (a, t, _, im, sub, desc, tags, k) in enumerate(SERVICES))
    idx = "".join(f'<a href="#{a}">{t}</a>' for a, t, *_ in SERVICES)
    sheets = "".join(f'<div class="sheet glass"><span>0{5-i}</span>{l}</div>' for i, l in enumerate(["KËSHILLIM", "PAGAT", "TATIME", "KONTABILITET", "AUDITIM"]))
    inds = "".join(f'<div class="ind" data-reveal="up"><span class="icon">{ic(i)}</span>{t}</div>' for i, t in [
        ("store", "Tregti dhe shitje"), ("factory", "Prodhim"), ("crane", "Ndërtim"),
        ("brief", "Shërbime profesionale"), ("heart", "OJQ dhe projekte me donatorë"), ("rocket", "Startup-e dhe IT")])
    pk = [("Start", "Për startup-e & biznese të vogla", ["Kontabilitet mujor", "Deklarimi i TVSH-së dhe tatimeve", "Pagat deri në 5 punonjës", "Pasqyrat vjetore"], False),
          ("Rritje", "Për biznese në zgjerim", ["Gjithçka në Start", "Raport menaxherial mujor", "Pagat pa kufi punonjësish", "Planifikim tatimor tremujor", "Kontakt i dedikuar"], True),
          ("Korporatë", "Për kompani & OJQ", ["Auditim statutor ose i brendshëm", "Raportim sipas SNRF", "Çmimet e transferimit", "Due diligence dhe vlerësim"], False)]
    pkgs = "".join(f'''<div class="pkg{' pkg--hot' if hot else ''}" data-reveal="up">
        {'<span class="flag">Më i zgjedhuri</span>' if hot else ''}<span class="who">{w}</span><span class="price">{n}</span>
        <ul class="check{' ' if not hot else ''}">{"".join(f'<li>{x}</li>' for x in f)}</ul>
        <a class="btn {'' if hot else 'btn--ghost'}" href="kontakt.html">Merr ofertë fikse {ARROW}</a></div>''' for n, w, f, hot in pk)
    svc_ld = [{"@type": "Service", "@id": f"{SITE}/sherbimet.html#{a}", "name": t, "serviceType": t, "description": desc,
               "provider": {"@id": f"{SITE}/#business"}, "areaServed": {"@type": "Country", "name": "Kosovë"}}
              for a, t, _, im, sub, desc, tags, k in SERVICES]
    return head("Shërbimet · Auditim, Kontabilitet, Tatime & Pagat | Finova",
                "Auditim statutor, kontabilitet mujor, këshillim tatimor dhe përfaqësim në ATK, pagat dhe këshillim financiar për biznese në Kosovë. Ofertë fikse brenda 48 orëve.",
                "sherbimet.html", [faq_ld(FAQ_SVC), crumbs_ld([("Ballina", ""), ("Shërbimet", "sherbimet.html")])] + svc_ld,
                page_type="CollectionPage") + header("sherbimet.html") + f'''
<main id="main">
<section class="hero hero--short">
  <div class="grid-bg" aria-hidden="true"></div><div class="blob blob--g" aria-hidden="true"></div>
  <div class="wrap">
    <div class="hero-copy">
      <nav class="crumbs intro" aria-label="Breadcrumb"><a href="index.html">Ballina</a><span aria-hidden="true">/</span><span aria-current="page">Shërbimet</span></nav>
      <h1 class="intro" style="--d:.12s">Çdo shërbim,<br>një <span class="accent underline">standard.</span></h1>
      <p class="lead intro" style="--d:.25s;max-width:520px">Pesë fusha, një ekip. Zgjidhni atë që ju duhet sot, ne kujdesemi që të gjitha të flasin të njëjtën gjuhë.</p>
      <div class="svc-index intro" style="--d:.4s">{idx}</div>
    </div>
    <div class="ledger intro-pop" style="--d:.3s" aria-hidden="true" data-parallax="-.05">{sheets}</div>
  </div>
</section>

<section class="section" style="padding-top:20px">
  <div class="wrap" style="display:grid;gap:28px">{blocks}</div>
</section>

<section class="section section--soft">
  <div class="wrap" style="display:grid;gap:48px">
    <div class="head center"><span class="eyebrow" data-reveal="up">Paketat mujore</span>
      <h2 data-split>Një paketë për çdo fazë të biznesit</h2>
      <p class="lead" data-reveal="up">Çdo paketë përshtatet sipas vëllimit tuaj. Çmimi fiks e merrni pas takimit të parë falas.</p></div>
    <div class="packages" data-stagger=".12">{pkgs}</div>
  </div>
</section>

<section class="section">
  <div class="wrap" style="display:grid;gap:44px">
    <div class="head head--split"><div><span class="eyebrow" data-reveal="up">Për kë punojmë</span>
      <h2 data-split>Biznese të çdo madhësie, në çdo fazë</h2></div>
      <p class="lead" style="max-width:380px" data-reveal="up">Njohim rregullat dhe sfidat specifike të secilës industri në Kosovë.</p></div>
    <div class="industries" data-stagger=".08">{inds}</div>
  </div>
</section>

<section class="section section--soft" id="pyetje">
  <div class="wrap" style="display:grid;gap:48px">
    <div class="head center"><span class="eyebrow" data-reveal="up">Pyetje të shpeshta</span>
      <h2 data-split>Pyetje që na bëhen shpesh</h2></div>
    {faq_html(FAQ_SVC)}
  </div>
</section>
<div style="height:clamp(72px,10vw,120px)"></div>
{cta("Nuk jeni të sigurt cili shërbim ju duhet?", "Bisedoni 30 minuta me një ekspert, falas. Ju themi saktësisht çfarë ju duhet dhe çfarë jo.")}
</main>
''' + footer()


def page_about():
    team = [("Arta Krasniqi", "Partnere · Auditore e licencuar", "AK"), ("Driton Berisha", "Partner · Këshilltar tatimor", "DB"),
            ("Ekspert/e", "Menaxher/e i kontabilitetit", "F"), ("Ekspert/e", "Specialist/e i pagave", "F")]
    members = "".join(f'''<div class="member" data-reveal="up"><div class="ph"><span class="init">{i}</span></div>
        <div class="info"><b>{n}</b><span>{r}</span></div></div>''' for n, r, i in team)
    tl = "".join(f'<div class="tl" data-step data-reveal="left"><b>{y}</b><h3>{t}</h3><p>{d}</p></div>' for y, t, d in [
        (FOUNDED, "Fillimi", "Finova hap zyrën e parë në Prishtinë me dy partnerë dhe një ide: numra të saktë, të shpjeguar qartë."),
        ("2015", "Licenca e auditimit", "Ekipi licencohet nga KKRF dhe fillojmë auditimet statutore për kompani të mesme e të mëdha."),
        ("2019", "Shërbime për diasporën", "Nisim punën plotësisht online për bizneset kosovare të drejtuara nga jashtë vendit."),
        ("2023", "Raportim digjital", "Klientët marrin pasqyra mujore dhe kujtesa për afatet direkt në telefon."),
        ("Sot", "24 ekspertë, 320+ klientë", "Një ekip i plotë për auditim, kontabilitet, tatime, paga dhe këshillim financiar.")])
    vals = "".join(f'<div class="card" data-reveal="up" data-tilt="6"><span class="icon icon--glass">{ic(i)}</span><h3>{t}</h3><p>{d}</p></div>' for i, t, d in [
        ("target", "Saktësi", "Çdo shifër kontrollohet dy herë. Gabimet e vogla bëhen probleme të mëdha."),
        ("shield", "Pavarësi", "Opinioni ynë nuk blihet. Kjo e bën atë të vlefshëm për ju dhe për bankën tuaj."),
        ("eye", "Qartësi", "Shpjegojmë numrat në gjuhë të thjeshtë, pa zhargon të panevojshëm."),
        ("lock", "Konfidencialitet", "Të dhënat tuaja financiare mbeten vetëm tuajat.")])
    return head("Rreth nesh · Ekipi dhe historia e Finova | Auditim në Prishtinë",
                f"Njihuni me Finova: kompani auditimi dhe kontabiliteti në Prishtinë që nga {FOUNDED}. Auditues të licencuar nga KKRF, 24 ekspertë dhe 320+ biznese klientë.",
                "rreth-nesh.html", [crumbs_ld([("Ballina", ""), ("Rreth nesh", "rreth-nesh.html")])], page_type="AboutPage") + header("rreth-nesh.html") + f'''
<main id="main">
<section class="hero hero--short">
  <div class="grid-bg" aria-hidden="true"></div><div class="blob blob--g" aria-hidden="true"></div><div class="blob blob--b" aria-hidden="true"></div>
  <div class="wrap">
    <div class="hero-copy">
      <nav class="crumbs intro" aria-label="Breadcrumb"><a href="index.html">Ballina</a><span aria-hidden="true">/</span><span aria-current="page">Rreth nesh</span></nav>
      <h1 class="intro" style="--d:.12s">Njerëz që i duan<br><span class="accent underline">numrat e saktë.</span></h1>
      <p class="lead intro" style="--d:.25s;max-width:540px">Që nga {FOUNDED}, ndihmojmë bizneset në Kosovë dhe në diasporë të kuptojnë financat e tyre dhe të rriten me siguri.</p>
      <div class="hero-meta intro" style="--d:.4s">
        <div><b><span data-count="{2026-int(FOUNDED)}">15</span>+</b><small>Vite</small></div>
        <div><b><span data-count="24">24</span></b><small>Ekspertë</small></div>
        <div><b><span data-count="320">320</span>+</b><small>Klientë</small></div>
      </div>
    </div>
    <div class="pill-photo intro-pop" style="--d:.3s;min-height:420px" data-tilt="5">
      {img("team", "Ekipi i Finova", "(max-width: 1080px) 100vw, 45vw", eager=True)}
      <div class="glass"><b>Prishtinë · Kosovë</b><span style="font-size:14px;opacity:.8">{STREET}</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap" style="display:grid;gap:40px">
    <span class="eyebrow" data-reveal="up">Emri ynë</span>
    <div class="word" data-progress data-fill aria-label="FIN NOVA"><span class="fin" data-reveal="left">FIN</span><span class="nova" data-reveal="right">NOVA</span></div>
    <div class="grid g-2" data-stagger=".12">
      <p class="lead" data-reveal="up"><b style="color:var(--navy)">FIN</b> është disiplina: llogaria, rregulli, përgjegjësia. Është gjithçka që një auditor duhet të jetë: i saktë, i qëndrueshëm, i pavarur.</p>
      <p class="lead" data-reveal="up"><b style="color:var(--navy)">NOVA</b> është mënyra: e qartë, e shpejtë, njerëzore. Raporte që lexohen, ekspertë që përgjigjen dhe teknologji që kursen kohë.</p>
    </div>
  </div>
</section>

<section class="section section--navy on-dark values">
  <div class="blob blob--g" aria-hidden="true"></div>
  <div class="wrap" style="position:relative;display:grid;gap:48px">
    <div class="head center"><span class="eyebrow eyebrow--dark" data-reveal="up">Vlerat tona</span>
      <h2 data-split>Katër parime, çdo ditë</h2></div>
    <div class="grid g-4" data-stagger=".1">{vals}</div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="stack">
      <span class="eyebrow" data-reveal="up">Historia</span>
      <h2 data-split>Nga dy partnerë në një ekip të plotë</h2>
      <p class="lead" data-reveal="up">Rritja jonë ka ndjekur rritjen e klientëve tanë: e matur, jo e supozuar.</p>
      <div class="photo-stack" data-reveal="mask" style="padding-bottom:0"><div class="main" style="aspect-ratio:4/3">{img("calc", "Analizë e pasqyrave financiare", "(max-width: 820px) 100vw, 50vw")}</div></div>
    </div>
    <div class="timeline" data-progress>{tl}</div>
  </div>
</section>

<section class="section section--soft" id="ekipi">
  <div class="wrap" style="display:grid;gap:48px">
    <div class="head head--split"><div><span class="eyebrow" data-reveal="up">Ekipi</span>
      <h2 data-split>Ekspertët pas çdo raporti</h2></div>
      <p class="lead" style="max-width:380px" data-reveal="up">Auditues, kontabilistë dhe këshilltarë tatimorë me përvojë në biznese të çdo madhësie.</p></div>
    <!-- Shtoni foto reale të ekipit: vendosni <img> brenda .ph -->
    <div class="team" data-stagger=".1">{members}</div>
  </div>
</section>

<section class="section">
  <div class="wrap split split--rev">
    <div class="stack">
      <span class="eyebrow" data-reveal="up">Karriera</span>
      <h2 data-split>Doni të punoni me ne?</h2>
      <p class="lead" data-reveal="up">Kërkojmë gjithmonë kontabilistë dhe auditues të rinj që duan të mësojnë nga më të mirët. Ofrojmë mentorim, mbështetje për certifikimet profesionale dhe një ekip që kujdeset.</p>
      <ul class="check" data-stagger=".1"><li data-reveal="left">Mbështetje për licencimin nga SCAAK dhe KKRF</li><li data-reveal="left">Orar fleksibil dhe punë hibride</li><li data-reveal="left">Projekte me kompani vendore e ndërkombëtare</li></ul>
      <div data-reveal="up"><a class="btn btn--navy" href="mailto:{EMAIL}?subject=Aplikim%20p%C3%ABr%20pun%C3%AB">Dërgoni CV-në {ARROW}</a></div>
    </div>
    <div class="photo-stack" data-reveal="mask" style="padding-bottom:0"><div class="main" style="aspect-ratio:4/3" data-parallax=".05">{img("meeting", "Takim pune në zyrën e Finova", "(max-width: 820px) 100vw, 50vw")}</div></div>
  </div>
</section>
{cta("Le të njihemi personalisht.", "Kafeja e parë është nga ne. Ejani në zyrë ose bisedojmë online.")}
</main>
''' + footer()


def page_contact():
    hours = [("E hënë – E premte", "08:00 – 16:30", "1 2 3 4 5"), ("E shtunë", "09:00 – 13:00", "6"), ("E diel", "Mbyllur", "0")]
    hrs = "".join(f'<li data-day="{d}"><span>{a}</span><span>{b}</span></li>' for a, b, d in hours)
    topics = "".join(f'<label><input type="checkbox" name="topic" value="{t}"><span>{t}</span></label>' for t in ["Auditim", "Kontabilitet", "Tatime", "Pagat", "Këshillim", "Tjetër"])
    items = "".join(f'<a class="c-item glass" href="{h}" data-reveal="left"><span class="icon icon--glass">{ic(i)}</span><span><small>{l}</small><b>{v}</b></span></a>' for i, l, v, h in [
        ("phone", "TELEFONI", PHONE, f"tel:{PHONE_RAW}"), ("mail", "EMAIL", EMAIL, f"mailto:{EMAIL}"), ("pin", "ADRESA", f"{STREET}, {CITY}", MAP_LINK)])
    return head("Kontakt · Rezervoni një takim falas | Finova Prishtinë",
                f"Na kontaktoni për auditim, kontabilitet ose tatime. Telefon {PHONE}, email {EMAIL}, zyra në {STREET}, {CITY}. Përgjigje brenda 24 orëve.",
                "kontakt.html", [faq_ld(FAQ_CONTACT), crumbs_ld([("Ballina", ""), ("Kontakt", "kontakt.html")])], page_type="ContactPage") + header("kontakt.html") + f'''
<main id="main">
<section class="hero hero--short">
  <div class="grid-bg" aria-hidden="true"></div><div class="blob blob--g" aria-hidden="true"></div><div class="blob blob--b" aria-hidden="true"></div>
  <div class="wrap contact-grid">
    <div class="hero-copy">
      <nav class="crumbs intro" aria-label="Breadcrumb"><a href="index.html">Ballina</a><span aria-hidden="true">/</span><span aria-current="page">Kontakt</span></nav>
      <h1 class="intro" style="--d:.12s">Le të flasim<br>për <span class="accent underline">numrat.</span></h1>
      <p class="lead intro" style="--d:.25s">Takimi i parë është falas. Na shkruani dhe ju kthejmë përgjigje brenda 24 orëve të punës.</p>
      <div class="c-list" data-stagger=".1">{items}</div>
      <div class="avatars intro" style="--d:.6s"><span><img src="images/av1.webp" width="38" height="38" alt=""><img src="images/av2.webp" width="38" height="38" alt=""></span>Flisni drejtpërdrejt me një ekspert<br>Arta Krasniqi · Driton Berisha, partnerë</div>
    </div>
    <div class="intro-pop" style="--d:.35s">
      <!-- Për të marrë mesazhet direkt në email, krijoni një formë falas në formspree.io dhe vendosni URL-në në data-endpoint -->
      <form id="contact-form" class="form glass sheen" data-endpoint="" novalidate>
        <div><h2>Na dërgoni një mesazh</h2><p class="fine" style="margin-top:6px">Fushat me * janë të detyrueshme.</p></div>
        <fieldset class="topics"><legend>Për çfarë keni nevojë?</legend>{topics}</fieldset>
        <div class="fields">
          <label class="field">Emri dhe mbiemri *<input name="name" type="text" autocomplete="name" placeholder="Emri Mbiemri" required></label>
          <label class="field">Kompania<input name="company" type="text" autocomplete="organization" placeholder="Emri i biznesit"></label>
          <label class="field">Email *<input name="email" type="email" autocomplete="email" inputmode="email" placeholder="ju@kompania.com" required></label>
          <label class="field">Telefoni<input name="phone" type="tel" autocomplete="tel" inputmode="tel" placeholder="+383"></label>
          <label class="field full">Mesazhi *<textarea name="message" rows="4" placeholder="Na tregoni shkurt për biznesin tuaj dhe çfarë ju duhet." required></textarea></label>
        </div>
        <label class="hp" aria-hidden="true">Website<input name="website" tabindex="-1" autocomplete="off"></label>
        <p class="fine">Të dhënat tuaja trajtohen me konfidencialitet të plotë. Shih <a href="privatesia.html">politikën e privatësisë</a>.</p>
        <button class="btn" type="submit">Dërgo mesazhin {ARROW}</button>
      </form>
      <div id="form-done" class="form glass form-done" hidden tabindex="-1" role="status">
        <span class="ok">{ic("check")}</span>
        <h2>Faleminderit!</h2>
        <p class="lead">Mesazhi u përgatit. Një nga ekspertët tanë do t’ju kontaktojë brenda 24 orëve të punës.</p>
        <button class="btn btn--glass" type="button" data-action="reset">Dërgo një mesazh tjetër</button>
      </div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:20px">
  <div class="wrap" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:24px">
    <div class="map" data-reveal="mask" style="grid-column:span 2;min-width:0">
      <button class="map-cover" type="button" data-src="{MAP_EMBED}" aria-label="Shfaq hartën interaktive">
        <svg class="grid-map" aria-hidden="true" preserveAspectRatio="xMidYMid slice" viewBox="0 0 800 420"><g stroke="#fff" stroke-width="14" fill="none" opacity=".85"><path d="M-20 120 L820 80"/><path d="M-20 300 L820 340"/><path d="M200 -20 L260 440"/><path d="M560 -20 L520 440"/></g><g stroke="#fff" stroke-width="5" fill="none" opacity=".6"><path d="M-20 210 L820 200"/><path d="M380 -20 L400 440"/><path d="M80 -20 L120 440"/><path d="M700 -20 L680 440"/></g><path d="M600 230 q60 -40 120 0 t120 0 v200 h-240z" fill="#27E39A" opacity=".18"/></svg>
        <span class="pin"><i></i><span class="glass-light">Kliko për hartën · {STREET}</span></span>
      </button>
    </div>
    <div class="card" data-reveal="right" style="display:flex;flex-direction:column;gap:16px">
      <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap"><h3 style="margin:0">Orari i punës</h3><span class="open-now"><i class="dot"></i><span>Hapur</span></span></div>
      <ul class="hours" data-hours>{hrs}</ul>
      <p class="muted" style="font-size:14px">{STREET} · {CITY} {ZIP}</p>
      <a class="btn btn--navy" href="{MAP_LINK}" target="_blank" rel="noopener">Merr udhëzimet {ARROW}</a>
    </div>
  </div>
</section>

<section class="section section--soft">
  <div class="wrap" style="display:grid;gap:40px">
    <div class="head center"><span class="eyebrow" data-reveal="up">Para se të na shkruani</span><h2 data-split>Pyetje të shpeshta</h2></div>
    {faq_html(FAQ_CONTACT)}
  </div>
</section>
<div style="height:clamp(72px,10vw,120px)"></div>
{cta("Afatet tatimore po afrohen?", "Mos prisni deri në ditën e fundit. Rezervoni një takim sot.")}
</main>
''' + footer()


def page_privacy():
    return head("Politika e privatësisë dhe kushtet | Finova",
                "Si i mbledh, përdor dhe mbron Finova të dhënat personale të vizitorëve dhe klientëve, sipas Ligjit nr. 06/L-082 për Mbrojtjen e të Dhënave Personale.",
                "privatesia.html", [crumbs_ld([("Ballina", ""), ("Privatësia", "privatesia.html")])]) + header("") + f'''
<main id="main">
<section class="hero hero--short" style="padding-bottom:140px">
  <div class="grid-bg" aria-hidden="true"></div><div class="blob blob--g" aria-hidden="true"></div>
  <div class="wrap" style="grid-template-columns:1fr">
    <div class="hero-copy">
      <nav class="crumbs intro" aria-label="Breadcrumb"><a href="index.html">Ballina</a><span aria-hidden="true">/</span><span aria-current="page">Privatësia</span></nav>
      <h1 class="intro" style="--d:.12s">Politika e <span class="accent">privatësisë</span></h1>
      <p class="lead intro" style="--d:.25s">Përditësuar më: nëntor 2026</p>
    </div>
  </div>
</section>
<section class="section" style="padding-top:20px">
  <!-- Teksti është model. Kërkoni rishikim ligjor para publikimit. -->
  <article class="prose" data-reveal="up">
    <p>Finova (“ne”) respekton privatësinë tuaj. Kjo politikë shpjegon cilat të dhëna mbledhim përmes kësaj uebfaqeje, pse i mbledhim dhe si i mbrojmë, në përputhje me Ligjin nr. 06/L-082 për Mbrojtjen e të Dhënave Personale në Republikën e Kosovës.</p>
    <h2>Çfarë të dhënash mbledhim</h2>
    <ul><li>Të dhënat që na i jepni vullnetarisht në formularin e kontaktit: emri, kompania, email-i, telefoni dhe mesazhi.</li>
        <li>Të dhëna teknike bazë (p.sh. lloji i shfletuesit), vetëm nëse aktivizohet një mjet statistikash që respekton privatësinë.</li></ul>
    <h2>Pse i përdorim</h2>
    <ul><li>Për t’iu përgjigjur kërkesës suaj dhe për t’ju dërguar ofertë.</li><li>Për të ofruar shërbimet e kontraktuara.</li><li>Për të përmbushur detyrimet ligjore (p.sh. ligjet tatimore dhe kundër pastrimit të parave).</li></ul>
    <h2>Sa kohë i ruajmë</h2>
    <p>Mesazhet nga formulari i ruajmë deri në 12 muaj nëse nuk bëheni klient. Dokumentet e klientëve ruhen sipas afateve të kërkuara me ligj.</p>
    <h2>Ndarja me palë të treta</h2>
    <p>Nuk i shesim dhe nuk i ndajmë të dhënat tuaja për marketing. Harta e Google ngarkohet vetëm kur ju klikoni mbi të.</p>
    <h2>Të drejtat tuaja</h2>
    <p>Keni të drejtë të kërkoni qasje, korrigjim ose fshirje të të dhënave tuaja, si dhe të paraqisni ankesë në Agjencinë për Informim dhe Privatësi. Na shkruani në <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    <h2 id="kushtet">Kushtet e përdorimit</h2>
    <p>Përmbajtja e kësaj uebfaqeje ka karakter informues dhe nuk përbën këshillë profesionale për rastin tuaj specifik. Për këshilla të përshtatura, na kontaktoni. Të gjitha të drejtat mbi përmbajtjen dhe logon i takojnë Finova.</p>
  </article>
</section>
</main>
''' + footer()


def page_404():
    return head("Faqja nuk u gjet | Finova", "Kjo faqe nuk ekziston. Kthehuni në ballinë të Finova.", "404.html", noindex=True) + header("") + f'''
<main id="main" class="hero nf" style="padding:0">
  <div class="grid-bg" aria-hidden="true"></div><div class="blob blob--g" aria-hidden="true"></div>
  <div class="stack" style="position:relative;align-items:center">
    <div class="big intro">404</div>
    <h1 class="intro" style="--d:.15s;font-size:clamp(28px,4vw,40px)">Ky bilanc nuk barazohet.</h1>
    <p class="lead intro" style="--d:.3s">Faqja që kërkoni nuk ekziston ose është zhvendosur.</p>
    <div class="hero-actions intro" style="--d:.45s;justify-content:center"><a class="btn" href="index.html">Kthehu në ballinë {ARROW}</a><a class="btn btn--glass" href="kontakt.html">Na kontaktoni</a></div>
  </div>
</main>
</body></html>
'''

# ------------------------------------------------------------------ extras
def extras():
    pages = [("", "1.0", "weekly"), ("sherbimet.html", "0.9", "monthly"), ("rreth-nesh.html", "0.7", "monthly"),
             ("kontakt.html", "0.8", "monthly"), ("privatesia.html", "0.3", "yearly")]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{SITE}/{p}</loc><lastmod>2026-11-19</lastmod><changefreq>{c}</changefreq><priority>{pr}</priority></url>\n" for p, pr, c in pages) + "</urlset>\n"
    write("sitemap.xml", sm)
    write("robots.txt", f"""# Finova
User-agent: *
Allow: /
Disallow: /tools/

# AI search & assistants are welcome (GEO)
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /

Sitemap: {SITE}/sitemap.xml
""")
    svc = "\n".join(f"- [{t}]({SITE}/sherbimet.html#{a}): {desc}" for a, t, _, im, sub, desc, tags, k in SERVICES)
    faqs = "\n".join(f"### {q}\n{a}\n" for q, a in FAQ_HOME + FAQ_SVC)
    write("llms.txt", f"""# Finova

> Finova është kompani auditimi, kontabiliteti dhe këshillimi tatimor me seli në {CITY}, Kosovë (themeluar më {FOUNDED}). Auditorët janë të licencuar nga Këshilli i Kosovës për Raportim Financiar (KKRF). Shërben 320+ biznese në Kosovë dhe në diasporë, me një ekip prej 24 ekspertësh. Takimi i parë është falas.

Finova (FIN + NOVA) — "Saktësi me qasje njerëzore". Punon sipas SNA/ISA dhe SNRF/IFRS, dorëzon deklarata në EDI të ATK-së dhe raporton në shqip dhe anglisht.

## Kontakt
- Adresa: {STREET}, {ZIP} {CITY}, Kosovë
- Telefoni: {PHONE}
- Email: {EMAIL}
- Orari: E hënë–E premte 08:00–16:30, E shtunë 09:00–13:00

## Shërbimet
{svc}

## Faqet
- [Ballina]({SITE}/)
- [Shërbimet]({SITE}/sherbimet.html)
- [Rreth nesh]({SITE}/rreth-nesh.html)
- [Kontakt]({SITE}/kontakt.html)

## Pyetje të shpeshta
{faqs}""")
    write("site.webmanifest", json.dumps({"name": "Finova · Auditim & Kontabilitet", "short_name": "Finova", "lang": "sq",
        "start_url": "./", "display": "standalone", "background_color": "#0B1E62", "theme_color": "#0B1E62",
        "icons": [{"src": "images/favicon.svg", "sizes": "any", "type": "image/svg+xml"},
                  {"src": "images/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "images/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    write("index.html", page_index())
    write("sherbimet.html", page_services())
    write("rreth-nesh.html", page_about())
    write("kontakt.html", page_contact())
    write("privatesia.html", page_privacy())
    write("404.html", page_404())
    extras()
