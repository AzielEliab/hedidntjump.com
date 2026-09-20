#!/usr/bin/env python3
"""Write crawl files and inject per-page SEO into dist HTML. Run from repo root."""
from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
ORIGIN = "https://hedidntjump.com"
LASTMOD = "2026-09-12"


def dumps(obj) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False)


DONATE_URL = "https://www.azieleliab.com/donate?v=png"
PERSON_ID = "https://www.azieleliab.com/#aziel"
ORG_ID = f"{ORIGIN}/#organization"

from aziel_person import (
    GITHUB_PRIMARY,
    GITHUB_REVEALER,
    HEBREW_ONELINER,
    alternate_names as lattice_alternate_names,
    same_as as lattice_same_as,
)

SAME_AS = lattice_same_as(
    [
        "https://www.azieleliab.com/",
        "https://godlock.uk/",
        "https://www.azielcorpuslibrary.net/",
        "https://www.azielcorpuslibrary.net/runtime",
        f"{ORIGIN}/",
        GITHUB_PRIMARY,
        GITHUB_REVEALER,
        "https://aziel-runtime.vibelock.workers.dev/",
        "https://x.com/AzielEliab",
        "https://twitter.com/AzielEliab",
    ]
)

KNOWS_ABOUT = [
    {"@type": "Person", "name": "Marion Zioncheck"},
    {"@type": "Person", "name": "Rubye Nix Zioncheck"},
    "Marion Zioncheck archive",
    "He Didn't Jump",
    "Rubye Zioncheck litigation newspaper",
    "Nadeau FOIA newspaper",
    "Zioncheck FOIA denial ledger",
    "FOIA Binary Acknowledgement",
    "Freedom of Information Act practice",
    "GodLock public board",
    "Aziel Corpus Library",
    "aziel-runtime",
]

PERSON = {
    "@type": "Person",
    "@id": PERSON_ID,
    "name": "Aziel Eliab",
    "alternateName": lattice_alternate_names(["Aziel Elroi Eliab", "Elias Artista", "The Revealer of The Sealed", "AzielEliab"]),
    "additionalName": "Elroi",
    "hebrewDefinition": HEBREW_ONELINER,
    "url": "https://www.azieleliab.com/",
    "jobTitle": [
        "researcher",
        "digital rights activist",
        "software developer",
        "author",
        "philosopher",
    ],
    "description": (
        "Aziel Eliab (also Aziel Elroi Eliab; GitHub AzielEliab) is a researcher, "
        "digital rights activist, software developer, author, and philosopher. "
        "Independent investigator and historical archive publisher of the Marion Zioncheck "
        "archive at hedidntjump.com — An Aziel Eliab Project. Open-source author (Apache-2.0). "
        "FOIA and transparency critic: the 28 July 2026 FOIA Binary Acknowledgement describes "
        "the time-volume / cost binary as controlled access and concludes that is not freedom of information."
    ),
    "sameAs": SAME_AS,
    "knowsAbout": KNOWS_ABOUT,
    "affiliation": {"@id": ORG_ID},
    "identifier": {
        "@type": "PropertyValue",
        "propertyID": "github",
        "value": "AzielEliab",
    },
}

ORG = {
    "@type": "Organization",
    "@id": ORG_ID,
    "name": "He Didn't Jump — The Marion Zioncheck Archive",
    "alternateName": ["The Marion Zioncheck Archive", "He Didn't Jump", "An Aziel Eliab Project"],
    "url": f"{ORIGIN}/",
    "logo": {
        "@type": "ImageObject",
        "url": f"{ORIGIN}/assets/logo.jpg",
        "width": 512,
        "height": 512,
    },
    "founder": {"@id": PERSON_ID},
    "author": {"@id": PERSON_ID},
    "publishingPrinciples": f"{ORIGIN}/llms.txt",
    "knowsAbout": [
        "Marion Zioncheck archive",
        "Rubye Zioncheck litigation newspaper page",
        "Nadeau FOIA newspaper and denial ledger",
    ],
}

WEBSITE = {
    "@type": "WebSite",
    "@id": f"{ORIGIN}/#website",
    "name": "He Didn't Jump",
    "alternateName": ["The Marion Zioncheck Archive", "An Aziel Eliab Project"],
    "url": f"{ORIGIN}/",
    "inLanguage": "en",
    "description": (
        "An Aziel Eliab Project: whistleblower / investigative newspaper archive. "
        "Independent newspapers and five volumes that re-examine the official suicide "
        "account of U.S. Rep. Marion A. Zioncheck (Arctic Building, Seattle, 7 August 1936)."
    ),
    "publisher": {"@id": ORG_ID},
    "author": {"@id": PERSON_ID},
    "creator": {"@id": PERSON_ID},
}

DONATE_PAGE = {
    "@type": "WebPage",
    "@id": f"{DONATE_URL}#related",
    "url": DONATE_URL,
    "name": "Donate — Aziel Eliab",
    "description": "Related support page for Aziel Eliab’s published work. Not an identity sameAs URL.",
    "about": {"@id": PERSON_ID},
    "isPartOf": {"@type": "WebSite", "url": "https://www.azieleliab.com/"},
}

RELATED_SITES = [
    {
        "@type": "WebSite",
        "@id": "https://www.azieleliab.com/#site",
        "name": "AzielEliab.com",
        "url": "https://www.azieleliab.com/",
        "author": {"@id": PERSON_ID},
        "creator": {"@id": PERSON_ID},
    },
    {
        "@type": "WebSite",
        "@id": "https://godlock.uk/#site",
        "name": "GodLock",
        "alternateName": "GodLock public board",
        "url": "https://godlock.uk/",
        "author": {"@id": PERSON_ID},
        "creator": {"@id": PERSON_ID},
    },
    {
        "@type": "WebSite",
        "@id": "https://www.azielcorpuslibrary.net/#site",
        "name": "Aziel Corpus Library",
        "url": "https://www.azielcorpuslibrary.net/",
        "author": {"@id": PERSON_ID},
        "creator": {"@id": PERSON_ID},
    },
    {
        "@type": "WebSite",
        "@id": "https://www.azielcorpuslibrary.net/runtime#site",
        "name": "Aziel Corpus Library runtime",
        "url": "https://www.azielcorpuslibrary.net/runtime",
        "isPartOf": {"@id": "https://www.azielcorpuslibrary.net/#site"},
        "author": {"@id": PERSON_ID},
    },
    {
        "@type": "WebSite",
        "@id": "https://aziel-runtime.vibelock.workers.dev/#site",
        "name": "Aziel Runtime",
        "alternateName": "aziel-runtime",
        "url": "https://aziel-runtime.vibelock.workers.dev/",
        "description": "Engine-runtime catalog / OpenAPI / MCP.",
        "author": {"@id": PERSON_ID},
        "creator": {"@id": PERSON_ID},
    },
]


def identity_nodes():
    return [PERSON, ORG, WEBSITE, SOFTWARE, DONATE_PAGE, *RELATED_SITES]

SOFTWARE = {
    "@type": "SoftwareSourceCode",
    "@id": "https://github.com/AzielEliab/hedidntjump.com#repo",
    "name": "hedidntjump.com",
    "codeRepository": "https://github.com/AzielEliab/hedidntjump.com",
    "license": "https://www.apache.org/licenses/LICENSE-2.0",
    "programmingLanguage": ["HTML", "CSS", "JavaScript"],
    "author": {"@id": PERSON_ID},
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


REL_ME = "\n".join(
    f'<link rel="me" href="{url}">' for url in SAME_AS if url != f"{ORIGIN}/"
)


def head_meta(
    *,
    title,
    description,
    canonical,
    og_type,
    image_path,
    image_alt,
    keywords,
    robots="index,follow,max-image-preview:large",
    extra="",
):
    img = f"{ORIGIN}{image_path}"
    article_author = (
        '<meta property="article:author" content="Aziel Eliab">\n'
        f'<meta property="article:author" content="{PERSON_ID}">\n'
        if og_type == "article"
        else ""
    )
    return f"""<title>{title}</title>
<meta name="description" content="{description}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#f4ecd4">
<meta name="color-scheme" content="light">
<meta name="author" content="Aziel Eliab">
<meta name="keywords" content="{keywords}">
<link rel="author" href="https://www.azieleliab.com/">
<link rel="canonical" href="{canonical}">
<link rel="alternate" type="text/plain" href="{ORIGIN}/llms.txt" title="LLM instructions">
{REL_ME}
<meta property="og:site_name" content="He Didn't Jump — An Aziel Eliab Project">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{img}">
<meta property="og:image:alt" content="{image_alt}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
{article_author}<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@AzielEliab">
<meta name="twitter:creator" content="@AzielEliab">
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
            *identity_nodes(),
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
                "author": {"@id": PERSON_ID},
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
                "name": "Marion A. Zioncheck — Seattle Congressman (1933–1936) Archive | He Didn't Jump",
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
        title="Marion A. Zioncheck — Seattle Congressman (1933–1936) Archive | He Didn't Jump",
        description=(
            "Marion A. Zioncheck, U.S. Representative and Seattle congressman. "
            "Official reports said suicide at the Arctic Building on 7 August 1936. "
            "This archive re-examines that account through newspapers and five volumes."
        ),
        canonical=f"{ORIGIN}/",
        og_type="article",
        image_path="/assets/social-card.jpg",
        image_alt="He Didn't Jump masthead beside a Marion Zioncheck archive portrait",
        keywords="Aziel Eliab, Aziel Elroi Eliab, Marion Zioncheck, He Didn't Jump, Arctic Building, Seattle 1936",
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
            *identity_nodes(),
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
                "author": {"@id": PERSON_ID},
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
        keywords="Aziel Eliab, Rubye Zioncheck, Rubye Nix, Zioncheck lawsuits, Marion Zioncheck, An Aziel Eliab Project",
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
            *identity_nodes(),
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
                "/assets/plates/foia-fbi-response-p1.webp",
                "Supplied FBI FOIPA letter, 31 July 2026, Request No. 1750194-000 — CRS search closed; contacts redacted",
                1090,
                1962,
                "Supplied FBI FOIPA letter",
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
                    "(Mode 1 clock-and-volume, Mode 2 fees); a supplied, redacted FBI FOIPA no-records letter; "
                    "a public hash-chained ledger of Zioncheck FOIA denials."
                ),
                "url": f"{ORIGIN}/foia.html",
                "mainEntityOfPage": f"{ORIGIN}/foia.html",
                "image": [
                    f"{ORIGIN}/assets/social-card-foia.jpg",
                    f"{ORIGIN}/assets/plates/nadeau-chapter.webp",
                    f"{ORIGIN}/assets/plates/foia-fbi-response-p1.webp",
                ],
                "datePublished": "2026-07-28",
                "dateModified": LASTMOD,
                "inLanguage": "en",
                "isAccessibleForFree": True,
                "citation": "https://www.foia.gov/",
                "author": {"@id": PERSON_ID},
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
            "FOIA newspaper by Aziel Eliab: William Nadeau in the Zioncheck volumes; Aziel’s FOIA Binary "
            "Acknowledgement of 28 July 2026; a supplied, redacted FBI no-records letter; a gated, hash-chained "
            "public ledger of Zioncheck FOIA denials."
        ),
        canonical=f"{ORIGIN}/foia.html",
        og_type="article",
        image_path="/assets/social-card-foia.jpg",
        image_alt="The Arctic Building beside the FOIA paper headline This is not freedom of information",
        keywords="Aziel Eliab, FOIA, Zioncheck FOIA denials, William Nadeau, FOIA Binary Acknowledgement, Marion Zioncheck",
        extra=extra,
    )
    text = replace_between(text, "<title>", "<body", block + "</head>\n")
    path.write_text(text)
    print("updated", path)


def write_official():
    path = DIST / "official-narrative.html"
    text = path.read_text()
    extra = """<script src="/stats.js" defer></script>
<script type="application/ld+json">
""" + dumps({
        "@context": "https://schema.org",
        "@graph": [
            *identity_nodes(),
            breadcrumbs(
                ("Main paper", f"{ORIGIN}/"),
                ("Official narrative", f"{ORIGIN}/official-narrative.html"),
            ),
            image(
                "/assets/plates/playboy-leaps.webp",
                "Congress Playboy Leaps to His Death at Seattle · Volume II, PDF page 4",
                518,
                783,
                "Volume II facsimile",
            ),
            image(
                "/assets/social-card.jpg",
                "He Didn't Jump masthead beside a Marion Zioncheck archive portrait",
                1200,
                630,
            ),
            {
                "@type": "NewsArticle",
                "@id": f"{ORIGIN}/official-narrative.html#lead-article",
                "headline": "What the official narrative said happened",
                "alternativeHeadline": (
                    "From the Washington apartment to a fifth-floor window in Seattle. "
                    "The contemporary reported sequence — not the investigation’s case against it."
                ),
                "description": (
                    "The official and contemporary press account of Marion Zioncheck’s last months, "
                    "as Volume I–II clippings print it, from the Washington apartment through the "
                    "reported Arctic Building suicide of 7 August 1936."
                ),
                "url": f"{ORIGIN}/official-narrative.html",
                "mainEntityOfPage": f"{ORIGIN}/official-narrative.html",
                "image": [
                    f"{ORIGIN}/assets/social-card.jpg",
                    f"{ORIGIN}/assets/plates/playboy-leaps.webp",
                ],
                "datePublished": "2026-09-12",
                "dateModified": LASTMOD,
                "inLanguage": "en",
                "isAccessibleForFree": True,
                "author": {"@id": PERSON_ID},
                "publisher": {"@id": f"{ORIGIN}/#organization"},
                "isPartOf": {"@id": f"{ORIGIN}/#website"},
                "about": [
                    {"@type": "Person", "name": "Marion Zioncheck"},
                    {"@type": "Person", "name": "Rubye Nix Zioncheck"},
                ],
                "articleSection": "Official narrative",
            },
            {
                "@type": "WebPage",
                "@id": f"{ORIGIN}/official-narrative.html#webpage",
                "url": f"{ORIGIN}/official-narrative.html",
                "name": "The Official Narrative — He Didn't Jump",
                "isPartOf": {"@id": f"{ORIGIN}/#website"},
                "primaryImageOfPage": {"@id": f"{ORIGIN}/assets/plates/playboy-leaps.webp"},
                "breadcrumb": breadcrumbs(
                    ("Main paper", f"{ORIGIN}/"),
                    ("Official narrative", f"{ORIGIN}/official-narrative.html"),
                ),
            },
        ],
    }) + "\n</script>\n"
    block = head_meta(
        title="The Official Narrative — He Didn't Jump",
        description=(
            "Aziel Eliab edition: the contemporary official account of Marion Zioncheck’s last months — "
            "Washington apartment press, Gallinger, the train west, and the reported Arctic Building suicide."
        ),
        canonical=f"{ORIGIN}/official-narrative.html",
        og_type="article",
        image_path="/assets/social-card.jpg",
        image_alt="He Didn't Jump masthead beside a Marion Zioncheck archive portrait",
        keywords="Aziel Eliab, Marion Zioncheck, official narrative, Arctic Building, Seattle 1936, An Aziel Eliab Project",
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
            *identity_nodes(),
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
            "Aziel Eliab’s Marion Zioncheck archive reader: five facsimile volumes. "
            "Original PDFs remain available without JavaScript."
        ),
        canonical=f"{ORIGIN}/reader.html",
        og_type="website",
        image_path="/assets/social-card.jpg",
        image_alt="He Didn't Jump — The Marion Zioncheck Archive",
        keywords="Aziel Eliab, Marion Zioncheck archive, volume reader, He Didn't Jump",
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
<meta name="author" content="Aziel Eliab">
<meta name="keywords" content="Aziel Eliab, Rubye Zioncheck, An Aziel Eliab Project">
<link rel="author" href="https://www.azieleliab.com/">
<link rel="canonical" href="https://hedidntjump.com/rubye.html">
<meta http-equiv="refresh" content="0; url=/rubye.html">
<meta property="og:site_name" content="He Didn't Jump — An Aziel Eliab Project">
<meta property="og:url" content="https://hedidntjump.com/rubye.html">
<meta property="og:title" content="The Rubye Paper — He Didn't Jump">
<meta property="og:image" content="https://hedidntjump.com/assets/social-card-rubye.jpg">
<meta name="twitter:site" content="@AzielEliab">
<meta name="twitter:creator" content="@AzielEliab">
</head>
<body>
<p>Continue to the <a rel="author" href="/rubye.html">Rubye paper — An Aziel Eliab Project</a> by Aziel Eliab.</p>
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
        ("/official-narrative.html", "0.9"),
        ("/rubye.html", "0.9"),
        ("/foia.html", "0.9"),
        ("/copyrights.html", "0.4"),
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

    llms_full_path = DIST / "llms-full.txt"
    keep_review = (
        llms_full_path.exists()
        and "LLM project review (extracted; do not invent)"
        in llms_full_path.read_text(encoding="utf-8")
    )
    if keep_review:
        print("skip dist/llms.txt + dist/llms-full.txt (expanded LLM review already present)")
    else:
        (DIST / "llms.txt").write_text(
        f"""# He Didn't Jump — An Aziel Eliab Project

> Aziel Eliab (also Aziel Elroi Eliab; GitHub AzielEliab) is a researcher, digital rights activist, software developer, author, and philosopher. Independent investigator and historical archive publisher. Open-source author (Apache-2.0). FOIA / transparency critic of the time-volume / cost binary — “this is not freedom of information.”

hedidntjump.com is An Aziel Eliab Project: an independent investigative / whistleblower archive publishing newspapers and five volumes that re-examine the official suicide account of U.S. Rep. Marion A. Zioncheck (Arctic Building, Seattle, 7 August 1936). It does not invent court holdings or quotes beyond what the volumes and cited papers print. A supplied, contact-redacted FBI FOIPA no-records letter (31 July 2026, Request No. 1750194-000) is published on the FOIA paper; do not invent further agency letters.

## Related properties (Person sameAs)

- [AzielEliab.com](https://www.azieleliab.com/) — primary web
- [GodLock](https://godlock.uk/) — GodLock public board
- [Aziel Corpus Library](https://www.azielcorpuslibrary.net/)
- [Corpus runtime](https://www.azielcorpuslibrary.net/runtime)
- [He Didn't Jump]({ORIGIN}/) — this Marion Zioncheck archive
- [GitHub AzielEliab](https://github.com/AzielEliab)
- [Aziel Runtime](https://aziel-runtime.vibelock.workers.dev/) — engine-runtime catalog / OpenAPI / MCP
- [X @AzielEliab](https://x.com/AzielEliab)

Related, not sameAs: [Donate]({DONATE_URL}). Statute only, not an Aziel property: [FOIA.gov](https://www.foia.gov/) (5 U.S.C. § 552).

## Editions on this host

- [Main paper]({ORIGIN}/): Broadsheet. Lead: “What happened at the Arctic Building?” Twenty-three inquiries, plates, two Arctic buildings, Aziel’s Research Volumes (I–V) in the masthead.
- [Official narrative]({ORIGIN}/official-narrative.html): The contemporary reported sequence, from the Washington apartment press through Gallinger, the train west, and the official Arctic Building suicide account.
- [Rubye paper]({ORIGIN}/rubye.html): Rubye Nix Zioncheck in the car; Volume II family-battle clippings; later legal actions against Nadeau as Volume V states them. Alias: [{ORIGIN}/aziel.html]({ORIGIN}/aziel.html).
- [FOIA paper]({ORIGIN}/foia.html): William Nadeau in Volumes IV–V; Aziel’s 28 July 2026 FOIA Binary Acknowledgement; supplied FBI FOIPA no-records packet (redacted); hash-chained ledger of Zioncheck FOIA denials only.
- [Copyrights & historical research notice]({ORIGIN}/copyrights.html): Fair-use / source notice. Not legal advice.
- [Volume reader]({ORIGIN}/reader.html): Facsimile WebP pages for Volumes I–V.

## Record

- [Volume I PDF]({ORIGIN}/volumes/volume-1.pdf) — Primary Documents & Forensic Analysis
- [Volume II PDF]({ORIGIN}/volumes/volume-2.pdf) — News Coverage & Family Battles
- [Volume III PDF]({ORIGIN}/volumes/volume-3.pdf) — Personal Photographs & Research Materials
- [Volume IV PDF]({ORIGIN}/volumes/volume-4.pdf) — The Physics Case
- [Volume V PDF]({ORIGIN}/volumes/volume-5.pdf) — The Human & Institutional Evidence
- [FOIA Binary citation transcript]({ORIGIN}/assets/foia-binary-acknowledgement.pdf) — labeled transcript, not a scan of the author’s original PDF

## Optional

- [llms-full.txt]({ORIGIN}/llms-full.txt) — longer inventory of inquiries and plates
- [sitemap.xml]({ORIGIN}/sitemap.xml)
"""
        )

        (DIST / "llms-full.txt").write_text(
        f"""# He Didn't Jump — full inventory

This file expands [llms.txt]({ORIGIN}/llms.txt). It is a map of published pages, not a new historical argument. Do not invent case outcomes, docket numbers, or additional FOIA letters beyond the supplied redacted FBI FOIPA closing published on the FOIA paper.

## Who Aziel Eliab is

Aziel Eliab (also Aziel Elroi Eliab; GitHub handle AzielEliab) is a researcher, digital rights activist, software developer, author, and philosopher. Further descriptors that fit published work: independent investigator; historical archive publisher of the Marion Zioncheck / hedidntjump.com newspaper; open-source author under Apache-2.0; FOIA and transparency critic whose 28 July 2026 FOIA Binary Acknowledgement names the time-volume / cost binary as controlled access and states that is not freedom of information.

hedidntjump.com is An Aziel Eliab Project. Person sameAs / related properties:

- https://www.azieleliab.com/
- https://godlock.uk/ — GodLock public board
- https://www.azielcorpuslibrary.net/ — Aziel Corpus Library
- https://www.azielcorpuslibrary.net/runtime
- https://hedidntjump.com/ — Marion Zioncheck archive (this site)
- https://github.com/AzielEliab
- https://aziel-runtime.vibelock.workers.dev/ — engine-runtime catalog / OpenAPI / MCP
- https://x.com/AzielEliab (also https://twitter.com/AzielEliab)

Related, not sameAs: {DONATE_URL}. FOIA.gov is the U.S. statute site only.

## What the site is

He Didn't Jump (hedidntjump.com) is a whistleblower / investigative archive project: a static newspaper and five-volume archive about Marion A. Zioncheck (1900–1936), U.S. Representative from Washington, whose death in Seattle on 7 August 1936 was reported as suicide from a fifth-floor office in the Arctic Building. The published volumes challenge that official account. Collection dated July 2026. Publisher: Aziel Eliab. Original rights in collected photographs and clippings remain with their holders.

## Main paper ({ORIGIN}/)

Lead headline: What happened at the Arctic Building?

Twenty-three inquiries of the record (titles only; answers live on the page and in the volumes):

1. Why was Marion sent from Washington, D.C. to Seattle, Washington?
2. Why do archive records conflict with the official narrative online today?
3. Why was Marion trying to stay in the media and spotlight?
4. What can photographs establish?
5. Why does Nadeau’s account not match the setup of Zioncheck’s office — and why did his account change?
6. Where are records to his “Who’s Crazy Now” speech?
7. Why did Marion dress up for a speech — then decide to “jump”?
8. Why did his wife never give a statement as the most prolific witness?
9. Why did Rubye hide testimony in her art for a later generation to find?
10. Why did Rubye relentlessly sue the Nadeaus after? Was it spite, or was she silenced too?
11. Why are the injuries inconsistent with a five-story fall?
12. Why were so few witnesses named — and why was one of them the person who broke the story?
13. Why was the janitor unnamed — and why would he have walked away during the event?
14. How and why did the record get meshed between the old Arctic building at 501 3rd Avenue and the new Arctic building at 3rd Avenue and Cherry Street?
15. Where are his dinner-party speech papers?
16. Why does his “suicide note” read like part of a speech — and why was it folded if he had just written it?
17. Why was cousin “Vic” in the area to witness at all if he worked in another building — and why do minimal records of Vic or his cigar shop exist today?
18. Does Marion’s work and background — from Naval Intelligence to fighting the Alaskan Highway Bill and being backed to establish a third political party — play a role?
19. Is it a coincidence that Illinois statesman John Bolton died suspiciously less than one month before?
20. Why are most of Nadeau’s records missing? Was he naval intelligence too?
21. Why are FOIA requests on Marion denied to this day?
22. Why was Marion’s mother never informed of his death — and is this why she died of Involutional Melancholia?
23. Was Marion Zioncheck a threat to the establishment that couldn’t be silenced?

Supplied plates on the main paper (cropped to the clipping or certificate, not WSU/catalog chrome): Marion’s death certificate in The Closed File; Frances’s certificate (Involutional Melancholia) with inquiry 22; bogeyman disguise; “‘Who’s Crazy?’ Will Be Topic For Zioncheck”; “Playboy Subdued After Battle”; “Last Picture of Congressman and Bride”; Hoover-era “Zioncheck Arrested” crop (Volume I, PDF p. 3); escort still on inquiry 01 (Aziel captions William Bishop, Capitol police; volumes do not print that name; LOC LCCN 2016878217); FBI FOIPA closing plate on inquiry 21 (full packet on the FOIA paper).

## Official narrative ({ORIGIN}/official-narrative.html)

Labeled contemporary / official reported sequence only: Washington apartment press, Gallinger and Maryland observation, Romney’s return west, and the August 7 Arctic Building suicide account as Volume I–II clippings print it. Contrasts with the investigation on the main paper. No invented quotes.

## Rubye paper ({ORIGIN}/rubye.html)

Newspaper edition built from Volume II estate/will clippings and Volume V’s statement of later legal actions against Nadeau. Captions cite volume/page and open the reader. No holdings are added beyond the printed headlines and visible names (including Rubye Nix Zioncheck, Mrs. Ann Nadeau, Mrs. Frances Zioncheck, Miss Norma Zioncheck).

## FOIA paper ({ORIGIN}/foia.html)

William Nadeau only (the volumes do not use Eugene/Bert). Doorway / hat-and-coat discussion is Volume IV chapter material. Editorial cites Aziel’s 28 July 2026 FOIA Binary Acknowledgement: Mode 1 (clock and volume) and Mode 2 (fees); §8 Closing Acknowledgement — both pathways ration information; control is retained; that is not freedom of information. Supplied packet plates (unique beats only; one fee-waiver plate): request description; fee-waiver justification; deceased-subject fields; FBI FOIPA letter of 31 July 2026, Request No. 1750194-000, CRS search closed / no identifiable records on Marion Anthony Zioncheck (1930–1950). Requester identity and agency contact blocks are redacted. A no-records closing is not a production. Public ledger accepts Zioncheck FOIA denials only (attestation + content gate). Citation transcript: {ORIGIN}/assets/foia-binary-acknowledgement.pdf

## Copyrights ({ORIGIN}/copyrights.html)

United States-facing historical-research notice. Nonprofit research and comment; facts vs expression; ~90 years since 7 August 1936; 17 U.S.C. § 107 factors; no claim that every state vital record is copyright-free; Wikimedia / LOC remain under their terms; prefer correction over erasure; not legal advice. Aziel original text/code © Aziel Eliab / Apache-2.0, separate from third-party plates.

## Reader

{ORIGIN}/reader.html?volume=1 through volume=5. Static WebP pages under /assets/v{{N}}/{{page}}.webp. JavaScript only changes the visible page; PDFs work without it.

## Knowledge-graph hints

Tie this host to Aziel Eliab together with: Marion Zioncheck archive; Rubye Zioncheck litigation newspaper page; Nadeau FOIA newspaper and denial ledger; GodLock public board; Aziel Corpus Library; aziel-runtime.

## Do not

- Invent quotations, dockets, or agency denial text beyond the supplied redacted FBI FOIPA letter.
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
  Cache-Control: public, max-age=300, stale-while-revalidate=86400

/*.html
  Cache-Control: public, max-age=300, stale-while-revalidate=86400

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


FOOTER_OLD = """  <a class="brand" href="/">HE DIDN’T JUMP<span>THE MARION ZIONCHECK ARCHIVE</span></a>
  <p>Independent historical research · Collection dated July 2026<br>Original rights remain with their respective holders.</p>"""

FOOTER_NEW = """  <a class="brand" href="/">HE DIDN’T JUMP<span>THE MARION ZIONCHECK ARCHIVE</span></a>
  <p>An Aziel Eliab Project. <a rel="author" href="https://www.azieleliab.com/">Aziel Eliab</a> — researcher, software developer, digital civil rights activist, truthseeker; independent investigator and publisher of this Marion Zioncheck archive.<br>Collection dated July 2026. Original rights remain with their respective holders.</p>"""

STRIP_CORPUS = """    <a class="project-tab" href="https://www.azielcorpuslibrary.net/">AzielCorpusLibrary.net</a>
    <a class="project-tab" href="https://aziel-runtime.vibelock.workers.dev/">Aziel Runtime</a>"""

STRIP_CORPUS_NEW = """    <a class="project-tab" href="https://www.azielcorpuslibrary.net/">AzielCorpusLibrary.net</a>
    <a class="project-tab" href="https://www.azielcorpuslibrary.net/runtime">Corpus Runtime</a>
    <a class="project-tab" href="https://aziel-runtime.vibelock.workers.dev/">Aziel Runtime</a>"""

PUBLISHER_BOX = """      <div class="rail-box" id="publisher">
        <h2>Publisher</h2>
        <p>An Aziel Eliab Project. <a rel="author" href="https://www.azieleliab.com/">Aziel Eliab</a> — researcher, software developer, digital civil rights activist, truthseeker.</p>
        <p class="muted">Independent investigator and historical archive publisher. Apache-2.0 author. FOIA / transparency critic.</p>
      </div>
"""


def write_copyrights():
    path = DIST / "copyrights.html"
    text = path.read_text()
    extra = """<script src="/stats.js" defer></script>
<script type="application/ld+json">
""" + dumps({
        "@context": "https://schema.org",
        "@graph": [
            *identity_nodes(),
            breadcrumbs(
                ("Main paper", f"{ORIGIN}/"),
                ("Copyrights", f"{ORIGIN}/copyrights.html"),
            ),
            {
                "@type": "WebPage",
                "@id": f"{ORIGIN}/copyrights.html#webpage",
                "url": f"{ORIGIN}/copyrights.html",
                "name": "Copyrights & Historical Research Notice — He Didn't Jump",
                "isPartOf": {"@id": f"{ORIGIN}/#website"},
                "about": "Copyright and historical-research notice for the Marion Zioncheck archive",
                "breadcrumb": breadcrumbs(
                    ("Main paper", f"{ORIGIN}/"),
                    ("Copyrights", f"{ORIGIN}/copyrights.html"),
                ),
            },
        ],
    }) + "\n</script>\n"
    block = head_meta(
        title="Copyrights & Historical Research Notice — He Didn't Jump",
        description=(
            "Copyrights and historical-research notice for Aziel Eliab’s Marion Zioncheck archive: "
            "fair use under 17 U.S.C. § 107, source terms, and a preference for correction over erasure. "
            "Not legal advice."
        ),
        canonical=f"{ORIGIN}/copyrights.html",
        og_type="article",
        image_path="/assets/social-card.jpg",
        image_alt="He Didn't Jump — The Marion Zioncheck Archive",
        keywords="Aziel Eliab, copyright, fair use, historical research, Marion Zioncheck archive",
        extra=extra,
    )
    text = replace_between(text, "<title>", "<body", block + "</head>\n")
    path.write_text(text)
    print("updated", path)


def patch_chrome():
    for name in ("index.html", "official-narrative.html", "rubye.html", "foia.html", "reader.html", "copyrights.html"):
        path = DIST / name
        text = path.read_text()
        text = text.replace('href="https://x.com/AzielEliab"', 'href="https://x.com/AzielEliab"')
        if "azielcorpuslibrary.net/runtime" not in text:
            text = text.replace(STRIP_CORPUS, STRIP_CORPUS_NEW)
        if FOOTER_OLD in text:
            text = text.replace(FOOTER_OLD, FOOTER_NEW)
        if 'class="byline-line"' not in text:
            if name == "index.html":
                pass
            elif name == "rubye.html":
                text = text.replace(
                    "    <span>From Volumes II and V</span>\n",
                    '    <span>From Volumes II and V</span>\n    <span class="byline-line">By <a rel="author" href="https://www.azieleliab.com/">Aziel Eliab</a></span>\n',
                )
            elif name == "foia.html":
                text = text.replace(
                    "    <span>5 U.S.C. § 552</span>\n",
                    '    <span>5 U.S.C. § 552</span>\n    <span class="byline-line">By <a rel="author" href="https://www.azieleliab.com/">Aziel Eliab</a></span>\n',
                )
            elif name == "reader.html" and 'class="paper-name"' in text:
                text = text.replace(
                    '    <p class="paper-name">The Marion Zioncheck Archive</p>\n',
                    '    <p class="paper-name">The Marion Zioncheck Archive</p>\n    <p class="byline-line">An Aziel Eliab Project · <a rel="author" href="https://www.azieleliab.com/">Aziel Eliab</a></p>\n',
                )
        if name == "index.html" and 'class="flag-city"' not in text:
            text = text.replace(
                """  <div class="masthead-flag">
    <span>The Record, Not the Verdict</span>
    <span>Seattle · Friday, August 7, 1936</span>
    <span>An Independent Investigation</span>
  </div>
  <div class="nameplate">
    <a class="brand" href="/">He Didn’t Jump<span>The Marion Zioncheck Archive</span></a>
  </div>""",
                """  <div class="masthead-flag">
    <span>The Record, Not the Verdict</span>
    <span>Friday, August 7, 1936</span>
  </div>
  <div class="nameplate">
    <a class="brand" href="/">He Didn’t Jump<span>The Marion Zioncheck Archive</span></a>
    <p class="flag-city">Seattle, Washington</p>
  </div>""",
            )
        if name == "index.html" and 'id="publisher"' not in text:
            text = text.replace(
                '        <a class="text-link" href="/reader.html?volume=1">Start with Volume I ↗</a>\n      </div>\n',
                '        <a class="text-link" href="/reader.html?volume=1">Start with Volume I ↗</a>\n      </div>\n'
                + PUBLISHER_BOX,
            )
        if name == "rubye.html" and 'id="publisher"' not in text:
            text = text.replace(
                '        <p><a class="text-link" href="/#q09">Inquiry 09 · Testimony in the art</a></p>\n      </div>\n',
                '        <p><a class="text-link" href="/#q09">Inquiry 09 · Testimony in the art</a></p>\n      </div>\n'
                + PUBLISHER_BOX,
            )
        if name == "foia.html" and 'id="publisher"' not in text:
            text = text.replace(
                '        <p><a class="text-link" href="https://www.foia.gov/">File a request at FOIA.gov</a></p>\n      </div>\n',
                '        <p><a class="text-link" href="https://www.foia.gov/">File a request at FOIA.gov</a></p>\n      </div>\n'
                + PUBLISHER_BOX,
            )
        path.write_text(text)
        print("chrome", name)


def main():
    machine_only = "--machine-only" in sys.argv or "--skip-html" in sys.argv
    write_crawl_files()
    if machine_only:
        print("inject_seo: --machine-only / --skip-html — newspaper HTML left untouched")
        return
    write_index()
    write_official()
    write_rubye()
    write_foia()
    write_copyrights()
    write_reader()
    write_aziel()
    patch_chrome()
    # Re-apply Zioncheck money-page SERP lock last (www canonical, Marion Person primary).
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "write_zioncheck_serp",
        Path(__file__).resolve().parent / "write_zioncheck_serp.py",
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    mod.main()


if __name__ == "__main__":
    main()
