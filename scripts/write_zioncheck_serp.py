#!/usr/bin/env python3
"""Marion Zioncheck SERP lock for the money page (/) and /Case.

Published-facts only. Crazytown is omitted — the word does not appear in
repo HTML or Volume I–V PDFs. Aziel Eliab stays publisher, not mainEntity.
Writes dist/ and docs/. ZionBot owns newspaper HTML beyond head/H1/schema.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TREES = [ROOT / "dist", ROOT / "docs"]
WWW = "https://www.hedidntjump.com"
PERSON_ID = "https://www.azieleliab.com/#aziel"
ZION_ID = f"{WWW}/#marion-zioncheck"
ORG_ID = f"{WWW}/#organization"
SITE_ID = f"{WWW}/#website"
LASTMOD = "2026-09-13"

TITLE = "Marion A. Zioncheck — Seattle Congressman (1933–1936) Archive | He Didn't Jump"
DESCRIPTION = (
    "Marion A. Zioncheck, U.S. Representative and Seattle congressman. "
    "Official reports said suicide at the Arctic Building on 7 August 1936. "
    "This archive re-examines that account through newspapers and five volumes."
)
H1 = "Marion A. Zioncheck, Seattle congressman"
KEYWORDS = (
    "Marion A. Zioncheck, Marion Zioncheck, Congressman Marion A. Zioncheck, "
    "congressman Zioncheck, Seattle congressman suicide, Arctic Building, "
    "7 August 1936, He Didn't Jump"
)
PUBLISHER_NOT = (
    "Publisher of this Marion Zioncheck archive. "
    "Not biblical Aziel or Eliab; not euaziel.site; not Aziel S."
)

# Authority links only — not endorsements.
SAME_AS = [
    "https://en.wikipedia.org/wiki/Marion_Zioncheck",
    "https://history.house.gov/People/Listing/Z/ZIONCHECK,-Marion-Anthony-(Z000011)/",
    "https://www.historylink.org/File/5528",
    "https://id.loc.gov/authorities/names/n87891358",
]

CANONICAL_BY_FILE = {
    "index.html": f"{WWW}/",
    "case.html": f"{WWW}/Case",
    "press.html": f"{WWW}/Press",
    "inquiries.html": f"{WWW}/Inquiries",
    "inquires.html": f"{WWW}/Inquiries",
    "rubye.html": f"{WWW}/Rubye",
    "archives.html": f"{WWW}/Archives",
    "foia.html": f"{WWW}/FOIA",
    "volumes.html": f"{WWW}/Volumes",
    "reader.html": f"{WWW}/reader",
    "official-narrative.html": f"{WWW}/Narrative",
    "aziel.html": f"{WWW}/aziel",
    "copyrights.html": f"{WWW}/Copyrights",
}

HTML_CACHE = "public, max-age=300, stale-while-revalidate=86400"


def dumps(obj) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False)


def zioncheck_person() -> dict:
    return {
        "@type": "Person",
        "@id": ZION_ID,
        "name": "Marion A. Zioncheck",
        "alternateName": [
            "Marion Zioncheck",
            "Marion Anthony Zioncheck",
        ],
        "additionalName": "Anthony",
        "jobTitle": "U.S. Representative",
        "description": (
            "Marion A. Zioncheck (also Marion Zioncheck, Marion Anthony Zioncheck) "
            "was a U.S. Representative / Seattle congressman (1933–1936). "
            "Official reports said he died by suicide at the Arctic Building in "
            "Seattle on 7 August 1936. He Didn't Jump publishes newspapers and "
            "five volumes that re-examine that official account."
        ),
        "deathDate": "1936-08-07",
        "deathPlace": {
            "@type": "Place",
            "name": "Seattle, Washington",
        },
        "sameAs": SAME_AS,
        "url": f"{WWW}/",
    }


def publisher_person() -> dict:
    return {
        "@type": "Person",
        "@id": PERSON_ID,
        "name": "Aziel Eliab",
        "url": "https://www.azieleliab.com/",
        "jobTitle": "Publisher",
        "description": PUBLISHER_NOT,
    }


def organization() -> dict:
    return {
        "@type": "Organization",
        "@id": ORG_ID,
        "name": "He Didn't Jump — The Marion Zioncheck Archive",
        "url": f"{WWW}/",
        "founder": {"@id": PERSON_ID},
        "author": {"@id": PERSON_ID},
    }


def website() -> dict:
    return {
        "@type": "WebSite",
        "@id": SITE_ID,
        "name": "He Didn't Jump",
        "alternateName": "The Marion Zioncheck Archive",
        "url": f"{WWW}/",
        "inLanguage": "en",
        "description": DESCRIPTION,
        "about": {"@id": ZION_ID},
        "publisher": {"@id": ORG_ID},
        "author": {"@id": PERSON_ID},
    }


def faq_page(page_id: str) -> dict:
    qa = [
        (
            "Who was Marion Zioncheck?",
            "Marion Zioncheck (Marion A. Zioncheck; also Marion Anthony Zioncheck) "
            "was a U.S. Representative and Seattle congressman from 1933 to 1936. "
            "Official reports said he died by suicide at the Arctic Building in "
            "Seattle on 7 August 1936. This archive publishes newspapers and five "
            "volumes that re-examine that official account.",
        ),
        (
            "Who was Marion A. Zioncheck?",
            "Marion A. Zioncheck was a U.S. Representative from Seattle, Washington "
            "(1933–1936). The official report of 7 August 1936 called his Arctic "
            "Building death a suicide. He Didn't Jump re-examines that account from "
            "published newspapers and archive volumes; it does not invent quotes or holdings.",
        ),
        (
            "Who was Congressman Marion A. Zioncheck?",
            "Congressman Marion A. Zioncheck was the Seattle / Washington U.S. "
            "Representative whose death at the Arctic Building on 7 August 1936 was "
            "officially reported as suicide. This project publishes the newspaper "
            "and volume record that questions that official suicide account.",
        ),
        (
            "Who was Congressman Zioncheck?",
            "Congressman Zioncheck is Marion A. Zioncheck, the Seattle congressman "
            "and U.S. Representative (1933–1936). Official reports said suicide at "
            "the Arctic Building on 7 August 1936. This archive challenges that "
            "account with published volumes.",
        ),
        (
            "What is the official account of the Seattle congressman suicide?",
            "Contemporary official and press accounts said Seattle congressman "
            "Marion A. Zioncheck died by suicide from a fifth-floor Arctic Building "
            "office on 7 August 1936. He Didn't Jump publishes newspapers and five "
            "research volumes that re-examine that official suicide account. It does "
            "not invent court holdings or quotes beyond what those volumes and cited "
            "papers print.",
        ),
    ]
    return {
        "@type": "FAQPage",
        "@id": page_id,
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in qa
        ],
    }


def money_graph(*, page_url: str, page_name: str, page_id: str) -> dict:
    collection = {
        "@type": ["CollectionPage", "ArchiveComponent"],
        "@id": page_id,
        "url": page_url,
        "name": page_name,
        "headline": TITLE,
        "description": DESCRIPTION,
        "isPartOf": {"@id": SITE_ID},
        "about": {"@id": ZION_ID},
        "mainEntity": {"@id": ZION_ID},
        "author": {"@id": PERSON_ID},
        "publisher": {"@id": ORG_ID},
        "inLanguage": "en",
        "isAccessibleForFree": True,
        "speakable": {
            "@type": "SpeakableSpecification",
            "cssSelector": ["h1.headline", "p.deck", "p.large"],
        },
    }
    return {
        "@context": "https://schema.org",
        "@graph": [
            zioncheck_person(),
            website(),
            collection,
            organization(),
            publisher_person(),
            faq_page(f"{page_url.rstrip('/')}/#faq"),
        ],
    }


def patch_headers(text: str) -> str:
    html_block = (
        f"  Cache-Control: {HTML_CACHE}\n"
        "  CDN-Cache-Control: public, max-age=300, stale-while-revalidate=86400\n"
    )
    text = re.sub(
        r"(/\n)(?:  Cache-Control: no-store[\s\S]*?)(?=\n/\*\.html)",
        r"\1" + html_block,
        text,
        count=1,
    )
    text = re.sub(
        r"(/\*\.html\n)(?:  Cache-Control: no-store[\s\S]*?)(?=\n/index\.html)",
        r"\1" + html_block,
        text,
        count=1,
    )
    text = re.sub(
        r"(/index\.html\n)(?:  Cache-Control: no-store[\s\S]*?)(?=\n/sitemap\.xml)",
        r"\1"
        + html_block
        + "  Cloudflare-CDN-Cache-Control: public, max-age=300, stale-while-revalidate=86400\n",
        text,
        count=1,
    )
    # If a prior restore comment remains, keep it; do not reintroduce no-store.
    if "Cache-Control: no-store" in text and "/api/" not in text:
        # Keep stats.js dynamic; HTML must not stay no-store.
        pass
    if "/api/*" not in text:
        text = text.rstrip() + (
            "\n\n# Dynamic meters — do not CDN-cache\n"
            "/api/*\n"
            "  Cache-Control: no-store\n"
        )
    if "/assets/video/*.mp4" not in text:
        text = text.rstrip() + (
            "\n\n# Motion plate MP4s — never cache HTML mistakes long\n"
            "/assets/video/*.mp4\n"
            "  Content-Type: video/mp4\n"
            "  Cache-Control: public, max-age=300, must-revalidate\n"
            "  Accept-Ranges: bytes\n"
        )
    return text


def write_headers() -> None:
    for tree in TREES:
        path = tree / "_headers"
        text = patch_headers(path.read_text(encoding="utf-8"))
        path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        print("headers", path.relative_to(ROOT))


def write_sitemap() -> None:
    editions = [
        ("/", "1.0"),
        ("/Case", "1.0"),
        ("/Press", "0.8"),
        ("/Inquiries", "0.8"),
        ("/Rubye", "0.7"),
        ("/Archives", "0.6"),
        ("/FOIA", "0.7"),
        ("/Volumes", "0.8"),
        ("/reader", "0.6"),
        ("/Narrative", "0.8"),
        ("/aziel", "0.5"),
        ("/AzielEliab", "0.4"),
        ("/AboutAziel", "0.4"),
        ("/Copyrights", "0.3"),
    ]
    discovery = [
        ("/llms.txt", "0.5"),
        ("/llms-full.txt", "0.3"),
        ("/ai.txt", "0.3"),
        ("/cite.json", "0.5"),
        ("/openapi.json", "0.2"),
        ("/mcp.json", "0.2"),
        ("/.well-known/mcp.json", "0.2"),
        ("/volumes.json", "0.3"),
        ("/robots.txt", "0.2"),
        ("/sitemap-index.xml", "0.2"),
        ("/person.jsonld", "0.3"),
        ("/identity.jsonld", "0.3"),
        ("/graph.jsonld", "0.3"),
        ("/who-is-aziel-eliab.txt", "0.4"),
        ("/who-is", "0.4"),
        ("/.well-known/aziel.json", "0.3"),
    ]
    pdfs = [
        ("/volumes/volume-1.pdf", "0.6"),
        ("/volumes/volume-2.pdf", "0.6"),
        ("/volumes/volume-3.pdf", "0.6"),
        ("/volumes/volume-4.pdf", "0.6"),
        ("/volumes/volume-5.pdf", "0.6"),
        ("/assets/foia-binary-acknowledgement.pdf", "0.4"),
    ]
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, pri in editions + discovery + pdfs:
        parts.extend(
            [
                "  <url>",
                f"    <loc>{WWW}{loc}</loc>",
                f"    <lastmod>{LASTMOD}</lastmod>",
                "    <changefreq>weekly</changefreq>",
                f"    <priority>{pri}</priority>",
                "  </url>",
            ]
        )
    parts.append("</urlset>\n")
    body = "\n".join(parts)
    for tree in TREES:
        (tree / "sitemap.xml").write_text(body, encoding="utf-8")
        print("sitemap", (tree / "sitemap.xml").relative_to(ROOT))


def strip_http_equiv_cache(text: str) -> str:
    text = re.sub(
        r"<meta http-equiv=\"Cache-Control\"[^>]*>\n?",
        "",
        text,
        flags=re.I,
    )
    text = re.sub(r"<meta http-equiv=\"Pragma\"[^>]*>\n?", "", text, flags=re.I)
    text = re.sub(r"<meta http-equiv=\"Expires\"[^>]*>\n?", "", text, flags=re.I)
    return text


def set_tag(text: str, pattern: str, repl: str, count: int = 1) -> str:
    new, n = re.subn(pattern, repl, text, count=count, flags=re.I)
    return new if n else text


def money_head_fields(canonical: str) -> dict[str, str]:
    return {
        "title": TITLE,
        "description": DESCRIPTION,
        "canonical": canonical,
        "keywords": KEYWORDS,
        "og_title": TITLE,
        "og_description": DESCRIPTION,
        "og_url": canonical,
    }


def apply_money_meta(text: str, canonical: str) -> str:
    text = strip_http_equiv_cache(text)
    text = set_tag(text, r"<title>[^<]*</title>", f"<title>{TITLE}</title>")
    text = set_tag(
        text,
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{DESCRIPTION}">',
    )
    if 'name="keywords"' in text:
        text = set_tag(
            text,
            r'<meta name="keywords" content="[^"]*">',
            f'<meta name="keywords" content="{KEYWORDS}">',
        )
    else:
        text = text.replace(
            '<meta name="author"',
            f'<meta name="keywords" content="{KEYWORDS}">\n<meta name="author"',
            1,
        )
    if 'rel="canonical"' in text:
        text = set_tag(
            text,
            r'<link rel="canonical" href="[^"]*">',
            f'<link rel="canonical" href="{canonical}">',
        )
    else:
        text = text.replace(
            "<title>",
            f'<link rel="canonical" href="{canonical}">\n<title>',
            1,
        )
    text = set_tag(
        text,
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{TITLE}">',
    )
    text = set_tag(
        text,
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{DESCRIPTION}">',
    )
    text = set_tag(
        text,
        r'<meta property="og:url" content="[^"]*">',
        f'<meta property="og:url" content="{canonical}">',
    )
    text = set_tag(
        text,
        r'<meta name="twitter:title" content="[^"]*">',
        f'<meta name="twitter:title" content="{TITLE}">',
    )
    text = set_tag(
        text,
        r'<meta name="twitter:description" content="[^"]*">',
        f'<meta name="twitter:description" content="{DESCRIPTION}">',
    )
    text = set_tag(
        text,
        r'<link rel="alternate" type="text/plain" href="[^"]*"',
        f'<link rel="alternate" type="text/plain" href="{WWW}/llms.txt"',
    )
    return text


def replace_or_insert_jsonld(text: str, graph: dict) -> str:
    block = (
        '<script type="application/ld+json">\n'
        + dumps(graph)
        + "\n</script>\n"
    )
    if 'type="application/ld+json"' in text:
        text = re.sub(
            r'<script type="application/ld\+json">[\s\S]*?</script>\n?',
            block,
            text,
            count=1,
        )
    else:
        text = text.replace("</head>", block + "</head>", 1)
    return text


def ensure_h1(text: str) -> str:
    if re.search(r"<h1\b[^>]*>\s*Marion A\. Zioncheck", text):
        return text
    # Remove a competing page H1 only if it is not the Zioncheck congressman line.
    h1 = f'<h1 class="headline">{H1}</h1>\n'
    deck = '<p class="deck" id="lead-deck">'
    if deck in text:
        return text.replace(deck, h1 + deck, 1)
    return text.replace("<article class=\"lead\">", "<article class=\"lead\">\n" + h1, 1)


def write_money_pages() -> None:
    for tree in TREES:
        index = tree / "index.html"
        text = index.read_text(encoding="utf-8")
        text = apply_money_meta(text, f"{WWW}/")
        text = replace_or_insert_jsonld(
            text,
            money_graph(
                page_url=f"{WWW}/",
                page_name=TITLE,
                page_id=f"{WWW}/#webpage",
            ),
        )
        text = ensure_h1(text)
        index.write_text(text, encoding="utf-8")
        print("money", index.relative_to(ROOT))

        case = tree / "case.html"
        ctext = case.read_text(encoding="utf-8")
        ctext = apply_money_meta(ctext, f"{WWW}/Case")
        # Drop the mistaken inquiries alternate / OG leftover.
        ctext = re.sub(
            r'<link rel="alternate" href="[^"]*inquires[^"]*">\n?',
            "",
            ctext,
        )
        if 'property="og:title"' not in ctext:
            ctext = ctext.replace(
                "</head>",
                f'<meta property="og:title" content="{TITLE}">\n'
                f'<meta property="og:description" content="{DESCRIPTION}">\n'
                f'<meta property="og:url" content="{WWW}/Case">\n'
                f'<meta name="twitter:title" content="{TITLE}">\n'
                f'<meta name="twitter:description" content="{DESCRIPTION}">\n'
                "</head>",
                1,
            )
        ctext = replace_or_insert_jsonld(
            ctext,
            money_graph(
                page_url=f"{WWW}/Case",
                page_name=TITLE,
                page_id=f"{WWW}/Case#webpage",
            ),
        )
        ctext = ensure_h1(ctext)
        case.write_text(ctext, encoding="utf-8")
        print("money", case.relative_to(ROOT))


def unify_canonicals() -> None:
    for tree in TREES:
        for name, canonical in CANONICAL_BY_FILE.items():
            path = tree / name
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            text = strip_http_equiv_cache(text)
            if 'rel="canonical"' in text:
                text = set_tag(
                    text,
                    r'<link rel="canonical" href="[^"]*">',
                    f'<link rel="canonical" href="{canonical}">',
                )
            if 'property="og:url"' in text and name not in {"index.html", "case.html"}:
                text = set_tag(
                    text,
                    r'<meta property="og:url" content="[^"]*">',
                    f'<meta property="og:url" content="{canonical}">',
                )
            path.write_text(text, encoding="utf-8")
        print("canonicals", tree.name)


def write_redirects() -> None:
    extra = (
        "\n# www is the canonical host (apex 301). Do not 301 /case↔/Case "
        "(Cloudflare pretty-URL 308 can loop).\n"
        "https://hedidntjump.com/* https://www.hedidntjump.com/:splat 301\n"
        "http://hedidntjump.com/* https://www.hedidntjump.com/:splat 301\n"
    )
    for tree in TREES:
        path = tree / "_redirects"
        text = path.read_text(encoding="utf-8")
        text = text.replace("/case /Case 301\n", "")
        text = text.replace("/case.html /Case 301\n", "")
        if "www.hedidntjump.com/:splat" not in text:
            text = text.rstrip() + extra
        path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        print("redirects", path.relative_to(ROOT))


def write_llms() -> None:
    lead = f"""# He Didn't Jump — Marion A. Zioncheck archive

This host is the Marion A. Zioncheck archive: U.S. Representative / Seattle congressman (1933–1936). Official reports said suicide from a fifth-floor Arctic Building office in Seattle on 7 August 1936. He Didn't Jump publishes newspapers and five volumes that re-examine that official account. It does not invent court holdings or quotes beyond what the volumes and cited papers print.

## Query-relevant URLs

- [{WWW}/]({WWW}/) — money page (priority 1.0)
- [{WWW}/Case]({WWW}/Case) — Case edition (priority 1.0)
- [{WWW}/Narrative]({WWW}/Narrative) — official reported sequence
- [{WWW}/Inquiries]({WWW}/Inquiries) — 23 inquiries of the record
- [{WWW}/Volumes]({WWW}/Volumes) — Volumes I–V
- [{WWW}/llms.txt]({WWW}/llms.txt)
- [{WWW}/cite.json]({WWW}/cite.json)

"""
    for tree in TREES:
        path = tree / "llms.txt"
        text = path.read_text(encoding="utf-8")
        if "Marion A. Zioncheck archive" in text[:400] and "Query-relevant URLs" in text:
            continue
        # Keep the existing Aziel identity lock after the Zioncheck lead.
        if text.startswith("# He Didn't Jump"):
            text = lead + text
        else:
            text = lead + text
        path.write_text(text, encoding="utf-8")
        print("llms", path.relative_to(ROOT))


def write_cite() -> None:
    purpose = (
        "Marion A. Zioncheck archive: U.S. Representative / Seattle congressman "
        "(1933–1936). Official reports said suicide at the Arctic Building on "
        "7 August 1936. This project re-examines that account from published newspapers "
        "and volumes."
    )
    for tree in TREES:
        path = tree / "cite.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        # Front-load Zioncheck purpose without dropping identity-machine keys.
        ordered = {
            "about": "Marion A. Zioncheck archive",
            "subject": "Marion A. Zioncheck",
            "alternate_subject": [
                "Marion Zioncheck",
                "Marion Anthony Zioncheck",
                "Congressman Marion A. Zioncheck",
                "Congressman Zioncheck",
            ],
            "purpose": purpose,
            "canonical": f"{WWW}/",
            "case": f"{WWW}/Case",
            "query_urls": [
                f"{WWW}/",
                f"{WWW}/Case",
                f"{WWW}/Narrative",
                f"{WWW}/Inquiries",
                f"{WWW}/Volumes",
            ],
        }
        for key, value in data.items():
            if key not in ordered:
                ordered[key] = value
        path.write_text(dumps(ordered) + "\n", encoding="utf-8")
        print("cite", path.relative_to(ROOT))


def write_robots() -> None:
    for tree in TREES:
        path = tree / "robots.txt"
        text = path.read_text(encoding="utf-8")
        text = re.sub(
            r"Sitemap: https://hedidntjump.com/sitemap.xml\n",
            "",
            text,
        )
        if f"Sitemap: {WWW}/sitemap.xml" not in text:
            text = text.rstrip() + f"\nSitemap: {WWW}/sitemap.xml\n"
        path.write_text(text, encoding="utf-8")
        print("robots", path.relative_to(ROOT))


def write_sitemap_index() -> None:
    body = f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>{WWW}/sitemap.xml</loc>
    <lastmod>{LASTMOD}</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://www.azieleliab.com/sitemap.xml</loc>
    <lastmod>{LASTMOD}</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://www.azielcorpuslibrary.net/sitemap.xml</loc>
    <lastmod>{LASTMOD}</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://godlock.uk/sitemap.xml</loc>
    <lastmod>{LASTMOD}</lastmod>
  </sitemap>
</sitemapindex>
"""
    for tree in TREES:
        (tree / "sitemap-index.xml").write_text(body, encoding="utf-8")


def main() -> None:
    write_headers()
    write_sitemap()
    write_sitemap_index()
    write_money_pages()
    unify_canonicals()
    write_redirects()
    write_llms()
    write_cite()
    write_robots()
    print("zioncheck SERP lock written (Crazytown omitted — not attested in repo/volumes)")


if __name__ == "__main__":
    main()
