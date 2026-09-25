#!/usr/bin/env python3
"""Marion Zioncheck SERP lock.

Published-facts only. Crazytown is omitted — the word does not appear in
repo HTML or Volume I–V PDFs. Aziel Eliab stays publisher, not mainEntity.

Operator 2026-09-24: main() is machine-only. It writes cite / graph / llms /
ai.txt / openapi / sitemap / robots / _headers and does not open *.html or
_redirects. --rewrite-html is refused. ZionBot owns newspaper HTML.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from aziel_living import (
    ARG_FAQ_ROWS,
    HDJ_GENRE,
    HDJ_PURPOSE,
    LLMS_LEAD,
    MONEY_DESCRIPTION,
)
from aziel_person import publisher_person as aziel_publisher_person

ROOT = Path(__file__).resolve().parents[1]
TREES = [ROOT / "dist", ROOT / "docs"]
# ZionBot inventory: money page + canonical are apex. www is an alias.
APEX = "https://hedidntjump.com"
WWW = "https://www.hedidntjump.com"
PERSON_ID = "https://www.azieleliab.com/#aziel"
ZION_ID = f"{APEX}/#marion-zioncheck"
ORG_ID = f"{APEX}/#organization"
SITE_ID = f"{APEX}/#website"
LASTMOD = "2026-09-13"

TITLE = "Marion A. Zioncheck — Seattle Congressman (1933–1936) Archive | He Didn't Jump"
CASE_TITLE = "The Case — Marion A. Zioncheck, Seattle congressman | He Didn't Jump"
DESCRIPTION = MONEY_DESCRIPTION
H1 = "Marion A. Zioncheck, Seattle congressman"
KEYWORDS = (
    "Marion A. Zioncheck, Marion Zioncheck, Congressman Marion A. Zioncheck, "
    "congressman Zioncheck, Seattle congressman suicide, Arctic Building, "
    "7 August 1936, He Didn't Jump"
)

PUBLISHER_NOT = (
    "Publisher of this Marion Zioncheck archive. "
    "Public identity is Aziel Eliab only."
)

# Authority links only — not endorsements.
SAME_AS = [
    "https://en.wikipedia.org/wiki/Marion_Zioncheck",
    "https://history.house.gov/People/Listing/Z/ZIONCHECK,-Marion-Anthony-(Z000011)/",
    "https://www.historylink.org/File/5528",
    "https://id.loc.gov/authorities/names/n87891358",
]

CANONICAL_BY_FILE = {
    "index.html": f"{APEX}/",
    "case.html": f"{APEX}/Case",
    "press.html": f"{APEX}/Press",
    "inquiries.html": f"{APEX}/Inquiries",
    "inquires.html": f"{APEX}/Inquiries",
    "rubye.html": f"{APEX}/Rubye",
    "archives.html": f"{APEX}/Archives",
    "foia.html": f"{APEX}/FOIA",
    "volumes.html": f"{APEX}/Volumes",
    "reader.html": f"{APEX}/reader",
    "official-narrative.html": f"{APEX}/Narrative",
    "aziel.html": f"{APEX}/aziel",
    "copyrights.html": f"{APEX}/Copyrights",
}

HTML_CACHE = "public, max-age=300, stale-while-revalidate=86400"


def dumps(obj) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False)


def zioncheck_person() -> dict:
    from zioncheck_serp_lattice import zioncheck_person as lattice_person

    return lattice_person()


def publisher_person() -> dict:
    return aziel_publisher_person(
        job_title="Publisher",
        existing={
            "@type": "Person",
            "@id": PERSON_ID,
            "name": "Aziel Eliab",
            "url": "https://www.azieleliab.com/",
            "jobTitle": "Publisher",
            "description": PUBLISHER_NOT,
        },
    )


def organization() -> dict:
    return {
        "@type": "Organization",
        "@id": ORG_ID,
        "name": "He Didn't Jump — The Marion Zioncheck Archive",
        "url": f"{APEX}/",
        "founder": {"@id": PERSON_ID},
        "author": {"@id": PERSON_ID},
    }


def website() -> dict:
    return {
        "@type": "WebSite",
        "@id": SITE_ID,
        "name": "He Didn't Jump",
        "alternateName": "The Marion Zioncheck Archive",
        "url": f"{APEX}/",
        "inLanguage": "en",
        "description": DESCRIPTION,
        "genre": HDJ_GENRE,
        "about": {"@id": ZION_ID},
        "publisher": {"@id": ORG_ID},
        "author": {"@id": PERSON_ID},
    }


def faq_page(page_id: str) -> dict:
    qa = zioncheck_faq_pairs()
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
        "genre": HDJ_GENRE,
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
    """Patch priorities and missing pretty aliases. Do not rebuild the urlset."""
    from zioncheck_serp_lattice import _patch_sitemap

    for tree in TREES:
        path = tree / "sitemap.xml"
        path.write_text(_patch_sitemap(path.read_text(encoding="utf-8")), encoding="utf-8")
        print("sitemap", path.relative_to(ROOT))


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


def apply_money_meta(text: str, canonical: str, title: str = TITLE) -> str:
    text = strip_http_equiv_cache(text)
    text = set_tag(text, r"<title>[^<]*</title>", f"<title>{title}</title>")
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
        f'<meta property="og:title" content="{title}">',
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
        f'<meta name="twitter:title" content="{title}">',
    )
    text = set_tag(
        text,
        r'<meta name="twitter:description" content="[^"]*">',
        f'<meta name="twitter:description" content="{DESCRIPTION}">',
    )
    text = set_tag(
        text,
        r'<link rel="alternate" type="text/plain" href="[^"]*"',
        f'<link rel="alternate" type="text/plain" href="{APEX}/llms.txt"',
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


def _refuse_visible_surface(action: str) -> None:
    raise SystemExit(
        f"refusing {action} (operator 2026-09-24). "
        "Default and --machine-only leave every *.html byte and _redirects unchanged."
    )


def write_money_pages() -> None:
    _refuse_visible_surface("HTML rewrite")
    for tree in TREES:
        index = tree / "index.html"
        text = index.read_text(encoding="utf-8")
        text = apply_money_meta(text, f"{APEX}/")
        text = replace_or_insert_jsonld(
            text,
            money_graph(
                page_url=f"{APEX}/",
                page_name=TITLE,
                page_id=f"{APEX}/#webpage",
            ),
        )
        text = ensure_h1(text)
        index.write_text(text, encoding="utf-8")
        print("money", index.relative_to(ROOT))

        case = tree / "case.html"
        ctext = case.read_text(encoding="utf-8")
        ctext = apply_money_meta(ctext, f"{APEX}/Case", title=CASE_TITLE)
        # Drop the mistaken inquiries alternate / OG leftover.
        ctext = re.sub(
            r'<link rel="alternate" href="[^"]*inquires[^"]*">\n?',
            "",
            ctext,
        )
        if 'property="og:title"' not in ctext:
            ctext = ctext.replace(
                "</head>",
                f'<meta property="og:title" content="{CASE_TITLE}">\n'
                f'<meta property="og:description" content="{DESCRIPTION}">\n'
                f'<meta property="og:url" content="{APEX}/Case">\n'
                f'<meta name="twitter:title" content="{CASE_TITLE}">\n'
                f'<meta name="twitter:description" content="{DESCRIPTION}">\n'
                "</head>",
                1,
            )
        ctext = replace_or_insert_jsonld(
            ctext,
            money_graph(
                page_url=f"{APEX}/Case",
                page_name=CASE_TITLE,
                page_id=f"{APEX}/Case#webpage",
            ),
        )
        ctext = ensure_h1(ctext)
        case.write_text(ctext, encoding="utf-8")
        print("money", case.relative_to(ROOT))


def unify_canonicals() -> None:
    _refuse_visible_surface("HTML canonical rewrite")
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
    _refuse_visible_surface("_redirects rewrite")
    extra = (
        "\n# ZionBot inventory: apex is canonical. www aliases 301 here. "
        "Do not 301 /case↔/Case (Cloudflare pretty-URL 308 can loop).\n"
        "https://www.hedidntjump.com/* https://hedidntjump.com/:splat 301\n"
        "http://www.hedidntjump.com/* https://hedidntjump.com/:splat 301\n"
    )
    for tree in TREES:
        path = tree / "_redirects"
        text = path.read_text(encoding="utf-8")
        text = text.replace("/case /Case 301\n", "")
        text = text.replace("/case.html /Case 301\n", "")
        # Drop the earlier apex→www experiment.
        text = re.sub(
            r"\n# www is the canonical host[\s\S]*?(?=\Z)",
            "",
            text,
        )
        text = re.sub(
            r"https://hedidntjump.com/\* https://www.hedidntjump.com/:splat 301\n",
            "",
            text,
        )
        text = re.sub(
            r"http://hedidntjump.com/\* https://www.hedidntjump.com/:splat 301\n",
            "",
            text,
        )
        if "https://www.hedidntjump.com/* https://hedidntjump.com/:splat 301" not in text:
            text = text.rstrip() + extra
        path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        print("redirects", path.relative_to(ROOT))



def zioncheck_faq_pairs():
    from zioncheck_serp_lattice import faq_pairs

    return [*faq_pairs(), *[(row["q"], row["a"]) for row in ARG_FAQ_ROWS]]


def write_machine_surfaces() -> None:
    """Marion Person + Zioncheck FAQ on cite / llms / graph only — never HTML."""
    qa = zioncheck_faq_pairs()
    marion = zioncheck_person()
    faq = {
        "@type": "FAQPage",
        "@id": f"{WWW}/#zioncheck-faq",
        "url": f"{APEX}/",
        "name": "Marion A. Zioncheck — query FAQ",
        "isPartOf": {"@id": SITE_ID},
        "about": {"@id": ZION_ID},
        "mainEntity": [
            {
                "@type": "Question",
                "@id": f"{WWW}/#zioncheck-faq-{i}",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for i, (q, a) in enumerate(qa, 1)
        ],
    }
    section = "## Marion A. Zioncheck FAQ (machine)\n\n"
    for q, a in qa:
        section += f"Q: {q}\nA: {a}\n\n"
    section += (
        f"Marion Person `@id`: {ZION_ID}\n"
        f"Machine graph: {APEX}/graph.jsonld\n"
        f"Cite FAQ block: {APEX}/cite.json → zioncheck_faq\n\n"
    )
    for tree in TREES:
        gpath = tree / "graph.jsonld"
        g = json.loads(gpath.read_text(encoding="utf-8"))
        nodes = [
            n
            for n in g["@graph"]
            if n.get("@id") not in (ZION_ID, f"{WWW}/#zioncheck-faq")
        ]
        new_nodes = [marion]
        inserted = False
        for n in nodes:
            new_nodes.append(n)
            if n.get("@type") == "FAQPage" and not inserted:
                new_nodes.append(faq)
                inserted = True
        if not inserted:
            new_nodes.append(faq)
        g["@graph"] = new_nodes
        gpath.write_text(dumps(g) + "\n", encoding="utf-8")
        print("graph-machine", gpath.relative_to(ROOT))

        cpath = tree / "cite.json"
        cite = json.loads(cpath.read_text(encoding="utf-8"))
        cite["marion_person_id"] = ZION_ID
        from zioncheck_serp_lattice import cite_person

        cite["marion_person"] = cite_person()
        cite["zioncheck_faq"] = [{"q": q, "a": a} for q, a in qa]
        cpath.write_text(dumps(cite) + "\n", encoding="utf-8")
        print("cite-machine", cpath.relative_to(ROOT))

        lpath = tree / "llms.txt"
        text = lpath.read_text(encoding="utf-8")
        if "## Marion A. Zioncheck FAQ (machine)" in text:
            text = re.sub(
                r"## Marion A\. Zioncheck FAQ \(machine\)[\s\S]*?(?=\n## |\n# |\Z)",
                section,
                text,
                count=1,
            )
        else:
            m = re.search(r"(\n# He Didn't Jump — An Aziel Eliab Project)", text)
            if m:
                text = text[: m.start()] + "\n" + section + text[m.start() + 1 :]
            else:
                text = text.rstrip() + "\n\n" + section
        lpath.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        print("llms-machine", lpath.relative_to(ROOT))


def write_llms() -> None:
    for tree in TREES:
        path = tree / "llms.txt"
        text = path.read_text(encoding="utf-8")
        if text.startswith("# He Didn't Jump — Marion A. Zioncheck archive"):
            text = re.sub(
                r"(# He Didn't Jump — Marion A. Zioncheck archive\n\n)[\s\S]*?(?=\n## Query-relevant URLs|\n## |\n# |\Z)",
                rf"\1{LLMS_LEAD}\n",
                text,
                count=1,
            )
        elif "This host is the Marion A. Zioncheck archive:" in text:
            text = text.replace(
                "This host is the Marion A. Zioncheck archive: U.S. Representative / "
                "Seattle congressman (1933–1936). Official reports said suicide from a "
                "fifth-floor Arctic Building office in Seattle on 7 August 1936. He Didn't "
                "Jump publishes newspapers and five volumes that re-examine that official "
                "account. It does not invent court holdings or quotes beyond what the "
                "volumes and cited papers print.",
                LLMS_LEAD,
                1,
            )
        path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        print("llms", path.relative_to(ROOT))


def write_cite() -> None:
    purpose = HDJ_PURPOSE
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
            "canonical": f"{APEX}/",
            "case": f"{APEX}/Case",
            "query_urls": [
                f"{APEX}/",
                f"{APEX}/Case",
                f"{APEX}/Narrative",
                f"{APEX}/Press",
                f"{APEX}/Inquiries",
                f"{APEX}/Rubye",
                f"{APEX}/Archives",
                f"{APEX}/FOIA",
                f"{APEX}/Volumes",
                f"{APEX}/reader",
                f"{APEX}/Copyrights",
                f"{APEX}/aziel",
                f"{APEX}/who",
                f"{APEX}/receipts",
                f"{APEX}/ingest-as-receipt.json",
                f"{APEX}/llms.txt",
                f"{APEX}/ai.txt",
                f"{APEX}/cite.json",
                f"{APEX}/openapi.json",
                f"{APEX}/shelves",
                f"{APEX}/lockset.json",
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
        if f"Sitemap: {APEX}/sitemap.xml" not in text:
            text = text.rstrip() + f"\nSitemap: {APEX}/sitemap.xml\n"
        path.write_text(text, encoding="utf-8")
        print("robots", path.relative_to(ROOT))


def write_sitemap_index() -> None:
    body = f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>{APEX}/sitemap.xml</loc>
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
    if "--rewrite-html" in sys.argv:
        _refuse_visible_surface("HTML rewrite")
    # --machine-only is the default. Lattice writes machine files only.
    from zioncheck_serp_lattice import apply_zioncheck_subsurface

    apply_zioncheck_subsurface()
    print("zioncheck SERP lock written (machine-only; HTML and _redirects untouched)")


if __name__ == "__main__":
    main()
