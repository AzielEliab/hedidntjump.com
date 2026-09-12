#!/usr/bin/env python3
"""Write crawl files and inject per-page SEO into dist HTML. Run from repo root."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
ORIGIN = "https://hedidntjump.com"
LASTMOD = "2026-09-12"


def dumps(obj) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False)


PERSON = {
    "@type": "Person",
    "@id": f"{ORIGIN}/#aziel-eliab",
    "name": "Aziel Eliab",
    "alternateName": ["Aziel Elroi Eliab"],
    "url": "https://www.azieleliab.com/",
    "jobTitle": "Independent investigator and archive publisher",
    "description": (
        "Publisher of the Marion Zioncheck archive at hedidntjump.com; "
        "software developer and Apache-2.0 author; researcher whose 28 July 2026 "
        "paper Acknowledgement of Structural Failure in FOIA Practice is cited on the FOIA edition."
    ),
    "sameAs": [
        "https://www.azieleliab.com/",
        "https://godlock.uk/",
        "https://www.azielcorpuslibrary.net/",
        f"{ORIGIN}/",
        "https://github.com/AzielEliab",
        "https://aziel-runtime.vibelock.workers.dev/",
        "https://x.com/azieleliab",
        "https://x.com/AzielEliab",
    ],
}

ORG = {
    "@type": "Organization",
    "@id": f"{ORIGIN}/#organization",
    "name": "He Didn't Jump — The Marion Zioncheck Archive",
    "alternateName": ["The Marion Zioncheck Archive", "He Didn't Jump"],
    "url": f"{ORIGIN}/",
    "logo": {
        "@type": "ImageObject",
        "url": f"{ORIGIN}/assets/logo.jpg",
        "width": 512,
        "height": 512,
    },
    "founder": {"@id": f"{ORIGIN}/#aziel-eliab"},
    "publishingPrinciples": f"{ORIGIN}/llms.txt",
}

WEBSITE = {
    "@type": "WebSite",
    "@id": f"{ORIGIN}/#website",
    "name": "He Didn't Jump",
    "alternateName": "The Marion Zioncheck Archive",
    "url": f"{ORIGIN}/",
    "inLanguage": "en",
    "description": (
        "Independent historical newspaper and five-volume archive examining the death of "
        "U.S. Representative Marion Zioncheck in Seattle on 7 August 1936."
    ),
    "publisher": {"@id": f"{ORIGIN}/#organization"},
    "author": {"@id": f"{ORIGIN}/#aziel-eliab"},
}

SOFTWARE = {
    "@type": "SoftwareSourceCode",
    "@id": "https://github.com/AzielEliab/hedidntjump.com#repo",
    "name": "hedidntjump.com",
    "codeRepository": "https://github.com/AzielEliab/hedidntjump.com",
    "license": "https://www.apache.org/licenses/LICENSE-2.0",
    "programmingLanguage": ["HTML", "CSS", "JavaScript"],
    "author": {"@id": f"{ORIGIN}/#aziel-eliab"},
}


def breadcrumbs(*pairs):
    items = []
    for i, (name, url) in enumerate(pairs, 1):
        items.append(
            {
                "@type": "ListItem",
                "position": i,
                "name": name,
                "item": url,
            }
        )
    return {
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }


def image(path, caption, width, height, credit=None):
    obj = {
        "@type": "ImageObject",
        "@id": f"{ORIGIN}{path}",
        "url": f"{ORIGIN}{path}",
        "contentUrl": f"{ORIGIN}{path}",
        "caption": caption,
        "width": width,
        "height": height,
        "inLanguage": "en",
    }
    if credit:
        obj["creditText"] = credit
    return obj


def head_meta(
    *,
    title,
    description,
    canonical,
    og_type,
    image_path,
    image_alt,
    robots="index,follow,max-image-preview:large",
    extra="",
):
    img = f"{ORIGIN}{image_path}"
    return f"""<title>{title}</title>
<meta name="description" content="{description}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#f4ecd4">
<meta name="color-scheme" content="light">
<meta name="author" content="Aziel Eliab">
<link rel="canonical" href="{canonical}">
<link rel="alternate" type="text/plain" href="{ORIGIN}/llms.txt" title="LLM instructions">
<meta property="og:site_name" content="He Didn't Jump">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{img}">
<meta property="og:image:alt" content="{image_alt}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{img}">
<meta name="twitter:image:alt" content="{image_alt}">
<meta name="hdj-stats-api" content="https://hedidntjump-stats.vibelock.workers.dev">
<link rel="stylesheet" href="/assets/fonts/fonts.css">
<link rel="stylesheet" href="/style.css">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{extra}"""


def replace_between(text: str, start: str, end: str, replacement: str) -> str:
    i = text.find(start)
    j = text.find(end)
    if i < 0 or j < 0 or j < i:
        raise SystemExit(f"markers not found: {start!r} … {end!r}")
    return text[:i] + replacement + text[j:]


def write_index():
    path = DIST / "index.html"
    text = path.read_text()
    extra = """<script src="/stats.js" defer></script>
<script type="application/ld+json">
""" + dumps({
        "@context": "https://schema.org",
        "@graph": [
            PERSON,
            ORG,
            WEBSITE,
            SOFTWARE,
            breadcrumbs(("Main paper", f"{ORIGIN}/")),
            image(
                "/assets/marion-zioncheck.webp",
                "Marion A. Zioncheck archive plate · Volume I, PDF page 9",
                1500,
                1949,
                "Marion Zioncheck archive, Volume I, PDF p. 9",
            ),
            image(
                "/assets/arctic-building.webp",
                "The Arctic Building, Seattle · Third Avenue and Cherry Street · circa 1917",
                1400,
                1806,
                "Marion Zioncheck archive photograph",
            ),
            image(
                "/assets/social-card.jpg",
                "He Didn't Jump — The Marion Zioncheck Archive",
                1200,
                630,
            ),
            {
                "@type": "NewsArticle",
                "@id": f"{ORIGIN}/#lead-article",
                "headline": "What happened at the Arctic Building?",
                "alternativeHeadline": "The death of Marion Zioncheck. The record deserves another reading.",
                "description": (
                    "Marion Zioncheck was a U.S. congressman from Washington. His death in Seattle "
                    "on August 7, 1936 was reported as suicide following a fall from his fifth-floor office. "
                    "This project challenges that account."
                ),
                "url": f"{ORIGIN}/",
                "mainEntityOfPage": f"{ORIGIN}/",
                "image": [
                    f"{ORIGIN}/assets/social-card.jpg",
                    f"{ORIGIN}/assets/marion-zioncheck.webp",
                ],
                "datePublished": "2026-07-01",
                "dateModified": LASTMOD,
                "inLanguage": "en",
                "isAccessibleForFree": True,
                "author": {"@id": f"{ORIGIN}/#aziel-eliab"},
                "publisher": {"@id": f"{ORIGIN}/#organization"},
                "isPartOf": {"@id": f"{ORIGIN}/#website"},
                "about": [
                    {"@type": "Person", "name": "Marion Zioncheck"},
                    {"@type": "Place", "name": "Arctic Building, Seattle"},
                ],
                "articleSection": "The case",
            },
            {
                "@type": "WebPage",
                "@id": f"{ORIGIN}/#webpage",
                "url": f"{ORIGIN}/",
                "name": "He Didn't Jump — The Marion Zioncheck Archive",
                "isPartOf": {"@id": f"{ORIGIN}/#website"},
                "primaryImageOfPage": {"@id": f"{ORIGIN}/assets/marion-zioncheck.webp"},
                "breadcrumb": breadcrumbs(("Main paper", f"{ORIGIN}/")),
                "speakable": {
                    "@type": "SpeakableSpecification",
                    "cssSelector": ["h1.headline", "p.deck", "p.large"],
                },
            },
        ],
    }) + "\n</script>\n"
    block = head_meta(
        title="He Didn't Jump — The Marion Zioncheck Archive",
        description=(
            "Independent newspaper archive on Marion Zioncheck’s 7 August 1936 death in Seattle. "
            "Five research volumes, contemporary plates, and 17 inquiries of the record."
        ),
        canonical=f"{ORIGIN}/",
        og_type="article",
        image_path="/assets/social-card.jpg",
        image_alt="He Didn't Jump masthead beside a Marion Zioncheck archive portrait",
        extra=extra,
    )
    text = replace_between(text, "<title>", "<body", block + "</head>\n")
    path.write_text(text)
    print("updated", path)


def write_rubye():
    path = DIST / "rubye.html"
    text = path.read_text()
    extra = """<script src="/stats.js" defer></script>
<script type="application/ld+json">
""" + dumps({
        "@context": "https://schema.org",
        "@graph": [
            PERSON,
            ORG,
            WEBSITE,
            breadcrumbs(
                ("Main paper", f"{ORIGIN}/"),
                ("Rubye paper", f"{ORIGIN}/rubye.html"),
            ),
            image(
                "/assets/marion-rubye.webp",
                "Marion A. Zioncheck with Rubye Louise Nix · 1936",
                1200,
                1488,
                "Marion Zioncheck archive photograph",
            ),
            image(
                "/assets/plates/kin-fight-will.webp",
                "Kin Fight Over Zioncheck Will · Volume II, PDF page 19 · WSU plate date 1937-01-19",
                710,
                900,
                "Volume II facsimile",
            ),
            image(
                "/assets/social-card-rubye.jpg",
                "The Rubye Paper — An Aziel Eliab Project",
                1200,
                630,
            ),
            {
                "@type": "NewsArticle",
                "@id": f"{ORIGIN}/rubye.html#lead-article",
                "headline": "Rubye in the record, and in court against Nadeau",
                "alternativeHeadline": (
                    "The contemporary report places her in the car. Volume V places later lawsuits on the same name."
                ),
                "description": (
                    "Rubye Nix Zioncheck in the archive: the car below the window, Volume II family-battle "
                    "clippings, and later legal actions against Nadeau as Volume V states them."
                ),
                "url": f"{ORIGIN}/rubye.html",
                "mainEntityOfPage": f"{ORIGIN}/rubye.html",
                "image": [
                    f"{ORIGIN}/assets/social-card-rubye.jpg",
                    f"{ORIGIN}/assets/marion-rubye.webp",
                ],
                "datePublished": "2026-07-01",
                "dateModified": LASTMOD,
                "inLanguage": "en",
                "isAccessibleForFree": True,
                "author": {"@id": f"{ORIGIN}/#aziel-eliab"},
                "publisher": {"@id": f"{ORIGIN}/#organization"},
                "isPartOf": {"@id": f"{ORIGIN}/#website"},
                "about": [
                    {"@type": "Person", "name": "Rubye Nix Zioncheck"},
                    {"@type": "Person", "name": "Marion Zioncheck"},
                ],
                "articleSection": "The Rubye Paper",
            },
            {
                "@type": "WebPage",
                "@id": f"{ORIGIN}/rubye.html#webpage",
                "url": f"{ORIGIN}/rubye.html",
                "name": "The Rubye Paper — He Didn't Jump",
                "isPartOf": {"@id": f"{ORIGIN}/#website"},
                "primaryImageOfPage": {"@id": f"{ORIGIN}/assets/marion-rubye.webp"},
                "breadcrumb": breadcrumbs(
                    ("Main paper", f"{ORIGIN}/"),
                    ("Rubye paper", f"{ORIGIN}/rubye.html"),
                ),
            },
        ],
    }) + "\n</script>\n"
    block = head_meta(
        title="The Rubye Paper — He Didn't Jump",
        description=(
            "Aziel Eliab project paper: Rubye Nix Zioncheck in the car, Volume II estate clippings, "
            "and later legal actions against Nadeau as printed in Volume V. Captioned to the reader."
        ),
        canonical=f"{ORIGIN}/rubye.html",
        og_type="article",
        image_path="/assets/social-card-rubye.jpg",
        image_alt="Marion and Rubye Zioncheck, archive photograph used on the Rubye paper",
        extra=extra,
    )
    text = replace_between(text, "<title>", "<body", block + "</head>\n")
    path.write_text(text)
    print("updated", path)


def write_foia():
    path = DIST / "foia.html"
    text = path.read_text()
    extra = """<script src="/stats.js" defer></script>
<script src="/foia.js" defer></script>
<script type="application/ld+json">
""" + dumps({
        "@context": "https://schema.org",
        "@graph": [
            PERSON,
            ORG,
            WEBSITE,
            breadcrumbs(
                ("Main paper", f"{ORIGIN}/"),
                ("FOIA paper", f"{ORIGIN}/foia.html"),
            ),
            image(
                "/assets/plates/nadeau-chapter.webp",
                "Volume IV, PDF page 11 — Nadeau doorway chapter as preserved",
                930,
                1200,
                "Volume IV facsimile",
            ),
            image(
                "/assets/social-card-foia.jpg",
                "FOIA paper: This is not freedom of information",
                1200,
                630,
            ),
            {
                "@type": "NewsArticle",
                "@id": f"{ORIGIN}/foia.html#lead-article",
                "headline": "This is not freedom of information",
                "alternativeHeadline": "A time-volume door. A cost door. Both leave the file on the institution’s side of the desk.",
                "description": (
                    "Nadeau in the Zioncheck volumes; Aziel’s 28 July 2026 FOIA Binary Acknowledgement "
                    "(Mode 1 clock-and-volume, Mode 2 fees); a public hash-chained ledger of Zioncheck FOIA denials."
                ),
                "url": f"{ORIGIN}/foia.html",
                "mainEntityOfPage": f"{ORIGIN}/foia.html",
                "image": [
                    f"{ORIGIN}/assets/social-card-foia.jpg",
                    f"{ORIGIN}/assets/plates/nadeau-chapter.webp",
                ],
                "datePublished": "2026-07-28",
                "dateModified": LASTMOD,
                "inLanguage": "en",
                "isAccessibleForFree": True,
                "citation": "https://www.foia.gov/",
                "author": {"@id": f"{ORIGIN}/#aziel-eliab"},
                "publisher": {"@id": f"{ORIGIN}/#organization"},
                "isPartOf": {"@id": f"{ORIGIN}/#website"},
                "about": [
                    {"@type": "Legislation", "name": "Freedom of Information Act", "legislationIdentifier": "5 U.S.C. § 552"},
                    {"@type": "Person", "name": "William Nadeau"},
                ],
                "articleSection": "FOIA paper",
            },
            {
                "@type": "WebPage",
                "@id": f"{ORIGIN}/foia.html#webpage",
                "url": f"{ORIGIN}/foia.html",
                "name": "This Is Not Freedom of Information — He Didn't Jump",
                "isPartOf": {"@id": f"{ORIGIN}/#website"},
                "primaryImageOfPage": {"@id": f"{ORIGIN}/assets/social-card-foia.jpg"},
                "breadcrumb": breadcrumbs(
                    ("Main paper", f"{ORIGIN}/"),
                    ("FOIA paper", f"{ORIGIN}/foia.html"),
                ),
            },
        ],
    }) + "\n</script>\n"
    block = head_meta(
        title="This Is Not Freedom of Information — He Didn't Jump",
        description=(
            "FOIA newspaper: William Nadeau in the Zioncheck volumes; Aziel’s FOIA Binary "
            "Acknowledgement of 28 July 2026; a gated, hash-chained public ledger of Zioncheck FOIA denials."
        ),
        canonical=f"{ORIGIN}/foia.html",
        og_type="article",
        image_path="/assets/social-card-foia.jpg",
        image_alt="The Arctic Building beside the FOIA paper headline This is not freedom of information",
        extra=extra,
    )
    text = replace_between(text, "<title>", "<body", block + "</head>\n")
    path.write_text(text)
    print("updated", path)


def write_reader():
    path = DIST / "reader.html"
    text = path.read_text()
    extra = """<script src="/reader.js" defer></script>
<script src="/stats.js" defer></script>
<script type="application/ld+json">
""" + dumps({
        "@context": "https://schema.org",
        "@graph": [
            PERSON,
            ORG,
            WEBSITE,
            breadcrumbs(
                ("Main paper", f"{ORIGIN}/"),
                ("Volume reader", f"{ORIGIN}/reader.html"),
            ),
            image(
                "/assets/social-card.jpg",
                "He Didn't Jump volume reader",
                1200,
                630,
            ),
            {
                "@type": "WebPage",
                "@id": f"{ORIGIN}/reader.html#webpage",
                "url": f"{ORIGIN}/reader.html",
                "name": "Volume Reader — He Didn't Jump",
                "description": (
                    "Facsimile reader for five Marion Zioncheck archive volumes. "
                    "Page images are static WebP files; original PDFs remain downloadable without JavaScript."
                ),
                "isPartOf": {"@id": f"{ORIGIN}/#website"},
                "breadcrumb": breadcrumbs(
                    ("Main paper", f"{ORIGIN}/"),
                    ("Volume reader", f"{ORIGIN}/reader.html"),
                ),
            },
        ],
    }) + "\n</script>\n"
    block = head_meta(
        title="Volume Reader — He Didn't Jump",
        description=(
            "Read the five Marion Zioncheck archive volumes as facsimile pages. "
            "Original PDFs remain available without JavaScript."
        ),
        canonical=f"{ORIGIN}/reader.html",
        og_type="website",
        image_path="/assets/social-card.jpg",
        image_alt="He Didn't Jump — The Marion Zioncheck Archive",
        extra=extra,
    )
    text = replace_between(text, "<title>", "<body", block + "</head>\n")
    if 'class="skip"' not in text:
        text = text.replace(
            '<body data-stats-page="reader">\n',
            '<body data-stats-page="reader">\n<a class="skip" href="#title">Skip to content</a>\n',
        )
    old_noscript = """  <noscript>
    <p>Enable JavaScript for page navigation, or <a href="/#archive">return to the archive</a>. Download originals: <a href="/volumes/volume-1.pdf">I</a>, <a href="/volumes/volume-2.pdf">II</a>, <a href="/volumes/volume-3.pdf">III</a>, <a href="/volumes/volume-4.pdf">IV</a>, <a href="/volumes/volume-5.pdf">V</a>.</p>
  </noscript>"""
    new_noscript = """  <noscript>
    <p>JavaScript turns the page images. The original PDFs are the record:</p>
    <ul>
      <li><a href="/volumes/volume-1.pdf">Volume I — Primary Documents &amp; Forensic Analysis (PDF)</a></li>
      <li><a href="/volumes/volume-2.pdf">Volume II — News Coverage &amp; Family Battles (PDF)</a></li>
      <li><a href="/volumes/volume-3.pdf">Volume III — Personal Photographs &amp; Research Materials (PDF)</a></li>
      <li><a href="/volumes/volume-4.pdf">Volume IV — The Physics Case (PDF)</a></li>
      <li><a href="/volumes/volume-5.pdf">Volume V — The Human &amp; Institutional Evidence (PDF)</a></li>
    </ul>
    <p><a href="/#archive">Return to the archive on the main paper</a></p>
  </noscript>"""
    if old_noscript in text:
        text = text.replace(old_noscript, new_noscript)
    path.write_text(text)
    print("updated", path)


def write_aziel():
    (DIST / "aziel.html").write_text(
        """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>An Aziel Eliab Project — He Didn't Jump</title>
<meta name="description" content="Alias for the Rubye paper, the Aziel Eliab project edition of the Marion Zioncheck archive.">
<meta name="robots" content="noindex,follow">
<meta name="theme-color" content="#f4ecd4">
<link rel="canonical" href="https://hedidntjump.com/rubye.html">
<meta http-equiv="refresh" content="0; url=/rubye.html">
<meta property="og:url" content="https://hedidntjump.com/rubye.html">
<meta property="og:title" content="The Rubye Paper — He Didn't Jump">
<meta property="og:image" content="https://hedidntjump.com/assets/social-card-rubye.jpg">
</head>
<body>
<p>Continue to the <a href="/rubye.html">Rubye paper — An Aziel Eliab Project</a>.</p>
</body>
</html>
"""
    )
    print("updated aziel.html")


def write_crawl_files():
    (DIST / "robots.txt").write_text(
        """User-agent: *
Allow: /

User-agent: Googlebot
Allow: /

User-agent: Googlebot-Image
Allow: /

User-agent: Bingbot
Allow: /

User-agent: DuckDuckBot
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Bytespider
Allow: /

# No private or admin surfaces are published on this static site.
# Cloudflare Pages Functions under /api/ are machine endpoints, not editions.
Disallow: /api/
Disallow: /functions/

Sitemap: https://hedidntjump.com/sitemap.xml
"""
    )

    urls = [
        ("/", "1.0"),
        ("/rubye.html", "0.9"),
        ("/foia.html", "0.9"),
        ("/reader.html", "0.8"),
        ("/reader.html?volume=1", "0.7"),
        ("/reader.html?volume=2", "0.7"),
        ("/reader.html?volume=3", "0.7"),
        ("/reader.html?volume=4", "0.7"),
        ("/reader.html?volume=5", "0.7"),
        ("/llms.txt", "0.4"),
        ("/llms-full.txt", "0.3"),
    ]
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, pri in urls:
        parts.append("  <url>")
        parts.append(f"    <loc>{ORIGIN}{loc}</loc>")
        parts.append(f"    <lastmod>{LASTMOD}</lastmod>")
        parts.append("    <changefreq>weekly</changefreq>")
        parts.append(f"    <priority>{pri}</priority>")
        parts.append("  </url>")
    parts.append("</urlset>\n")
    (DIST / "sitemap.xml").write_text("\n".join(parts))

    (DIST / "llms.txt").write_text(
        f"""# He Didn't Jump

> Independent historical newspaper and five-volume archive on the death of U.S. Representative Marion Zioncheck in Seattle on 7 August 1936. The official report called it suicide from a fifth-floor Arctic Building office. This project challenges that account and publishes the record for re-reading.

The site is an Aziel Eliab project. It does not invent court holdings, FOIA denial letters, or quotes beyond what the volumes and cited papers print. Send readers to the facsimile pages.

## Editions

- [Main paper]({ORIGIN}/): Broadsheet homepage. Lead: “What happened at the Arctic Building?” Seventeen inquiries of the record, contemporary plates, two Arctic buildings, volume downloads.
- [Rubye paper]({ORIGIN}/rubye.html): Aziel project edition. Rubye Nix Zioncheck in the car; Volume II family-battle clippings; later legal actions against Nadeau as Volume V states them. Alias: [{ORIGIN}/aziel.html]({ORIGIN}/aziel.html) (canonical is the Rubye paper).
- [FOIA paper]({ORIGIN}/foia.html): William Nadeau in Volumes IV–V; editorial citing Aziel’s 28 July 2026 FOIA Binary Acknowledgement (“This is not freedom of information”); public hash-chained ledger of Zioncheck FOIA denials only.
- [Volume reader]({ORIGIN}/reader.html): Facsimile WebP pages for Volumes I–V. Original PDFs remain downloadable.

## Record

- [Volume I PDF]({ORIGIN}/volumes/volume-1.pdf) — Primary Documents & Forensic Analysis
- [Volume II PDF]({ORIGIN}/volumes/volume-2.pdf) — News Coverage & Family Battles
- [Volume III PDF]({ORIGIN}/volumes/volume-3.pdf) — Personal Photographs & Research Materials
- [Volume IV PDF]({ORIGIN}/volumes/volume-4.pdf) — The Physics Case
- [Volume V PDF]({ORIGIN}/volumes/volume-5.pdf) — The Human & Institutional Evidence
- [FOIA Binary citation transcript]({ORIGIN}/assets/foia-binary-acknowledgement.pdf) — labeled transcript, not a scan of the author’s original PDF
- Statute: [FOIA.gov](https://www.foia.gov/) (5 U.S.C. § 552) — government site, not an Aziel property

## Publisher

- [AzielEliab.com](https://www.azieleliab.com/)
- [Donate](https://www.azieleliab.com/donate?v=png) — related support page, not a sameAs identity URL
- [GodLock](https://godlock.uk/)
- [AzielCorpusLibrary.net](https://www.azielcorpuslibrary.net/)
- [Aziel Runtime](https://aziel-runtime.vibelock.workers.dev/)
- [GitHub](https://github.com/AzielEliab)
- [X](https://x.com/azieleliab)

## Optional

- [llms-full.txt]({ORIGIN}/llms-full.txt) — longer inventory of inquiries and plates
- [sitemap.xml]({ORIGIN}/sitemap.xml)
"""
    )

    (DIST / "llms-full.txt").write_text(
        f"""# He Didn't Jump — full inventory

This file expands [llms.txt]({ORIGIN}/llms.txt). It is a map of published pages, not a new historical argument. Do not invent case outcomes, docket numbers, or FOIA letters.

## What the site is

He Didn't Jump (hedidntjump.com) is a static newspaper and archive about Marion A. Zioncheck (1900–1936), U.S. Representative from Washington, whose death in Seattle on 7 August 1936 was reported as suicide from a fifth-floor office in the Arctic Building. The published volumes challenge that account. Collection dated July 2026. Publisher: Aziel Eliab. Original rights in collected photographs and clippings remain with their holders.

## Main paper ({ORIGIN}/)

Lead headline: What happened at the Arctic Building?

Seventeen inquiries of the record (titles only; answers live on the page and in the volumes):

1. Why was Marion sent from Washington, D.C. to Seattle, Washington?
2. Why do archive records conflict with the official narrative online today?
3. Why was Marion trying to stay in the media and spotlight?
4. What can photographs establish?
5. Where are records to his “Who’s Crazy Now” speech?
6. Why did Marion dress up for a speech — then decide to “jump”?
7. Why did his wife never give a statement as the most prolific witness?
8. Why are the injuries inconsistent with a five-story fall?
9. Why were so few witnesses named — and why was one of them the person who broke the story?
10. How and why did the record get meshed between the old Arctic building at 501 3rd Avenue and the new Arctic building at 3rd Avenue and Cherry Street?
11. Where are his dinner-party speech papers?
12. Why does his “suicide note” read like part of a speech — and why was it folded if he had just written it?
13. Where did cousin “Vic” go after that fateful day?
14. Why was “Vic” there that night when he worked in the opposite Arctic building?
15. Does Marion’s work and background — from Naval Intelligence to fighting the Alaskan Highway Bill and being backed to establish a third political party — play a role?
16. Is it a coincidence that Illinois statesman John Bolton died suspiciously less than one month before?
17. Why are FOIA requests on Marion denied to this day?

## Rubye paper ({ORIGIN}/rubye.html)

Newspaper edition built from Volume II estate/will clippings and Volume V’s statement of later legal actions against Nadeau. Captions cite volume/page and open the reader. No holdings are added beyond the printed headlines and visible names (including Rubye Nix Zioncheck, Mrs. Ann Nadeau, Mrs. Frances Zioncheck, Miss Norma Zioncheck).

## FOIA paper ({ORIGIN}/foia.html)

William Nadeau only (the volumes do not use Eugene/Bert). Doorway / hat-and-coat discussion is Volume IV chapter material. Editorial cites Aziel’s 28 July 2026 FOIA Binary Acknowledgement: Mode 1 (clock and volume) and Mode 2 (fees); §8 Closing Acknowledgement — both pathways ration information; control is retained; that is not freedom of information. Public ledger accepts Zioncheck FOIA denials only (attestation + content gate). Citation transcript: {ORIGIN}/assets/foia-binary-acknowledgement.pdf

## Reader

{ORIGIN}/reader.html?volume=1 through volume=5. Static WebP pages under /assets/v{{N}}/{{page}}.webp. JavaScript only changes the visible page; PDFs work without it.

## Identity

Person: Aziel Eliab (also Aziel Elroi Eliab). Roles evidenced on this site: independent investigator, archive publisher, software developer, FOIA-practice critic. SameAs URLs published in the project strip: azieleliab.com, godlock.uk, azielcorpuslibrary.net, hedidntjump.com, github.com/AzielEliab, aziel-runtime.vibelock.workers.dev, x.com/azieleliab. Donate is a related support URL, not an identity sameAs. FOIA.gov is the statute, not an Aziel site.

## Do not

- Invent quotations, dockets, or agency denial text.
- Treat the FOIA Binary PDF on this host as a scan of the author’s original file; it is a labeled citation transcript.
- Collapse the two Arctic buildings (old 501 3rd / Morrison vs newer 3rd & Cherry).
"""
    )

    (DIST / "_headers").write_text(
        """# Cloudflare Pages header rules (ignored by GitHub Pages).
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN

/
  Cache-Control: public, max-age=300, must-revalidate

/*.html
  Cache-Control: public, max-age=300, must-revalidate

/sitemap.xml
  Content-Type: application/xml; charset=utf-8
  Cache-Control: public, max-age=3600

/robots.txt
  Content-Type: text/plain; charset=utf-8
  Cache-Control: public, max-age=3600

/llms.txt
  Content-Type: text/plain; charset=utf-8
  Cache-Control: public, max-age=3600

/llms-full.txt
  Content-Type: text/plain; charset=utf-8
  Cache-Control: public, max-age=3600

/assets/fonts/*
  Cache-Control: public, max-age=31536000, immutable

/assets/*
  Cache-Control: public, max-age=86400
"""
    )
    print("wrote crawl files")


def main():
    write_crawl_files()
    write_index()
    write_rubye()
    write_foia()
    write_reader()
    write_aziel()


if __name__ == "__main__":
    main()
