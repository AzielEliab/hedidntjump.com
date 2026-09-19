#!/usr/bin/env python3
"""AZindex GROWTH-ON discovery pass for hedidntjump.com.

Machine surfaces + sitemap/robots/llms/cite/openapi/headers only.
Does not invent biography, FOIA letters, holdings, DOIs, or a local MCP.
Does not change /ingest-as-receipt.json (tip stays stable).
Writes dist/ and docs/.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

ROOT = Path(__file__).resolve().parents[1]
TREES = [ROOT / "dist", ROOT / "docs"]
APEX = "https://hedidntjump.com"
WWW = "https://www.hedidntjump.com"
LASTMOD = "2026-09-18"
PERSON_ID = "https://www.azieleliab.com/#aziel"
ZION_ID = f"{APEX}/#marion-zioncheck"
HDJ_INGEST_TIP = "ef967e4acb47ba913ce3959b673767278da605b307de33210b2dc2f1cfd86f60"

MARION_AKA = [
    "Marion Zioncheck",
    "Marion Anthony Zioncheck",
    "Congressman Marion A. Zioncheck",
    "Congressman Zioncheck",
]
MARION_SAME_AS = [
    "https://en.wikipedia.org/wiki/Marion_Zioncheck",
    "https://history.house.gov/People/Listing/Z/ZIONCHECK,-Marion-Anthony-(Z000011)/",
    "https://www.historylink.org/File/5528",
    "https://id.loc.gov/authorities/names/n87891358",
]

QUERY_URLS = [
    f"{APEX}/",
    f"{APEX}/Case",
    f"{APEX}/Press",
    f"{APEX}/Inquiries",
    f"{APEX}/Rubye",
    f"{APEX}/Archives",
    f"{APEX}/FOIA",
    f"{APEX}/Volumes",
    f"{APEX}/reader",
    f"{APEX}/Narrative",
    f"{APEX}/aziel",
    f"{APEX}/Copyrights",
    f"{APEX}/who",
    f"{APEX}/receipts",
    f"{APEX}/ingest-as-receipt.json",
    f"{APEX}/llms.txt",
    f"{APEX}/ai.txt",
    f"{APEX}/cite.json",
    f"{APEX}/openapi.json",
    f"{APEX}/shelves",
    f"{APEX}/lockset.json",
    f"{WWW}/shelves",
    f"{APEX}/redline",
    f"{WWW}/redline",
    f"{APEX}/runtime-launch.json",
    f"{WWW}/runtime-launch.json",
]

SITEMAP_EXTRAS = [
    ("/.well-known/llms.txt", "0.4"),
    ("/volumes.json", "0.3"),
]

OPENAPI_PATHS = {
    "/who-is": "Who is Aziel Eliab — plain-text identity lock (alias of /who-is-aziel-eliab.txt)",
    "/who-is-aziel-eliab.txt": "Who is Aziel Eliab — plain-text identity lock",
    "/graph.jsonld": "Machine graph (Marion Person + FAQ + publisher lattice)",
    "/identity.jsonld": "Identity JSON-LD (shared Person @id https://www.azieleliab.com/#aziel)",
    "/mcp.json": "Honest MCP pointer — aziel-runtime on Glama; no local tools/list",
    "/.well-known/mcp.json": "Same honest MCP pointer as /mcp.json",
    "/.well-known/aziel.json": "Hub identity discovery card",
    "/.well-known/llms.txt": "200 rewrite to /llms.txt (LLM crawler well-known)",
    "/sitemap-index.xml": "Cross-site sitemap index",
    "/volumes.json": "Volume metadata (facsimile page counts / titles)",
    "/ai.txt": "AI crawl aid",
}

AI_AGENTS = [
    "Google-CloudVertexBot",
    "GoogleOther",
    "Claude-User",
    "Claude-SearchBot",
    "YouBot",
    "MistralAI-User",
    "FacebookBot",
    "archive.org_bot",
    "ia_archiver",
    "Yandex",
    "Baiduspider",
    "Slurp",
    "ImagesiftBot",
    "Omgilibot",
    "DuckAssistBot",
]


def dumps(obj) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def sitemap_entry(loc: str, priority: str) -> str:
    return (
        "  <url>\n"
        f"    <loc>{APEX}{loc}</loc>\n"
        f"    <lastmod>{LASTMOD}</lastmod>\n"
        "    <changefreq>weekly</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        "  </url>\n"
    )


def patch_robots() -> None:
    extra_allows = (
        "Allow: /cite.json\n"
        "Allow: /llms.txt\n"
        "Allow: /llms-full.txt\n"
        "Allow: /ai.txt\n"
        "Allow: /openapi.json\n"
        "Allow: /receipts\n"
        "Allow: /ingest-as-receipt.json\n"
        "Allow: /.well-known/llms.txt\n"
    )
    for tree in TREES:
        path = tree / "robots.txt"
        text = path.read_text(encoding="utf-8")
        if "Allow: /cite.json" not in text:
            text = text.replace(
                "Allow: /runtime-launch.json\n",
                "Allow: /runtime-launch.json\n" + extra_allows,
                1,
            )
        if "Disallow: /api/" in text.split("User-agent: Googlebot")[0]:
            pass
        else:
            text = text.replace(
                "Content-Signal: search=yes, ai-input=yes, ai-train=yes\n",
                (
                    "Disallow: /api/\n"
                    "Disallow: /functions/\n"
                    "Content-Signal: search=yes, ai-input=yes, ai-train=yes\n"
                ),
                1,
            )
        # Keep a single * Disallow group. Trailing cohere-only Disallow is a parse trap.
        text = re.sub(
            r"\n# Machine/admin endpoints only[^\n]*\nDisallow: /api/\nDisallow: /functions/\n",
            "\n# Machine/admin endpoints (/api/, /functions/) are Disallow on User-agent: * only.\n"
            "# Do not Disallow GPTBot/Claude/Perplexity/Google-Extended for budget.\n",
            text,
            count=1,
        )
        block = ""
        for agent in AI_AGENTS:
            if f"User-agent: {agent}" not in text:
                block += f"\nUser-agent: {agent}\nAllow: /\n"
        if block:
            text = text.replace(
                "\nUser-agent: cohere-ai\nAllow: /\n",
                "\nUser-agent: cohere-ai\nAllow: /\n" + block,
                1,
            )
        path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        print("robots", path.relative_to(ROOT))


def patch_headers() -> None:
    link = (
        "  Link: </llms.txt>; rel=\"describedby\"; type=\"text/plain\", "
        "</cite.json>; rel=\"cite-as\"; type=\"application/json\", "
        "</sitemap.xml>; rel=\"index\"\n"
    )
    extras = """
/volumes.json
  Content-Type: application/json; charset=utf-8
  Cache-Control: public, max-age=3600

/.well-known/llms.txt
  Content-Type: text/plain; charset=utf-8
  Cache-Control: public, max-age=3600
"""
    for tree in TREES:
        path = tree / "_headers"
        text = path.read_text(encoding="utf-8")
        if "rel=\"describedby\"" not in text:
            text = text.replace(
                "  Content-Signal: search=yes, ai-input=yes, ai-train=yes\n"
                "  X-Content-Type-Options: nosniff\n",
                "  Content-Signal: search=yes, ai-input=yes, ai-train=yes\n"
                + link
                + "  X-Content-Type-Options: nosniff\n",
                1,
            )
        if "/volumes.json" not in text or "/.well-known/llms.txt" not in text:
            if "/volumes.json" not in text:
                text = text.rstrip() + extras
            elif "/.well-known/llms.txt" not in text:
                text = text.rstrip() + (
                    "\n/.well-known/llms.txt\n"
                    "  Content-Type: text/plain; charset=utf-8\n"
                    "  Cache-Control: public, max-age=3600\n"
                )
        path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        print("headers", path.relative_to(ROOT))


def patch_redirects() -> None:
    pin = (
        "# LLM well-known (200 rewrite). Do not add /who → who.html, "
        "/aziel → aziel.html, /reader → reader.html, /receipts → receipts.html.\n"
        "/.well-known/llms.txt /llms.txt 200\n"
    )
    for tree in TREES:
        path = tree / "_redirects"
        text = path.read_text(encoding="utf-8")
        if "/.well-known/llms.txt /llms.txt 200" not in text:
            text = text.replace(
                "/.well-known/aziel.json /.well-known/aziel.json 200\n",
                "/.well-known/aziel.json /.well-known/aziel.json 200\n" + pin,
                1,
            )
        path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        print("redirects", path.relative_to(ROOT))


def patch_sitemap() -> None:
    for tree in TREES:
        path = tree / "sitemap.xml"
        text = path.read_text(encoding="utf-8")
        for loc, pri in SITEMAP_EXTRAS:
            if f"{APEX}{loc}</loc>" not in text:
                text = text.replace("</urlset>", sitemap_entry(loc, pri) + "</urlset>", 1)
        path.write_text(text, encoding="utf-8")
        print("sitemap", path.relative_to(ROOT))


def patch_openapi() -> None:
    for tree in TREES:
        path = tree / "openapi.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        paths = data.setdefault("paths", {})
        for loc, summary in OPENAPI_PATHS.items():
            paths.setdefault(
                loc,
                {
                    "get": {
                        "summary": summary,
                        "responses": {"200": {"description": "OK"}},
                    }
                },
            )
        path.write_text(dumps(data), encoding="utf-8")
        print("openapi", path.relative_to(ROOT))


def patch_cite() -> None:
    extra_editions = [
        {"id": "who", "href": f"{APEX}/who"},
        {"id": "reader", "href": f"{APEX}/reader"},
        {"id": "press", "href": f"{WWW}/Press"},
    ]
    for tree in TREES:
        path = tree / "cite.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        q = list(data.get("query_urls") or [])
        for u in QUERY_URLS:
            if u not in q:
                q.append(u)
        data["query_urls"] = q
        marion = data.setdefault("marion_person", {})
        marion["@id"] = ZION_ID
        aka = list(marion.get("alternateName") or [])
        for name in MARION_AKA:
            if name not in aka:
                aka.append(name)
        marion["alternateName"] = aka
        same = list(marion.get("sameAs") or [])
        for url in MARION_SAME_AS:
            if url not in same:
                same.append(url)
        marion["sameAs"] = same
        eds = list(data.get("editions") or [])
        have = {e.get("id") for e in eds if isinstance(e, dict)}
        for row in extra_editions:
            if row["id"] not in have:
                eds.append(row)
        data["editions"] = eds
        ll = data.setdefault("lamb_lens", {})
        ll.setdefault("order", "Service → Clarity → Peace")
        ll.setdefault("shelf", "https://www.azielcorpuslibrary.net/corpus")
        data["growth_on"] = True
        data["author_id"] = PERSON_ID
        data["person_id"] = PERSON_ID
        data["marion_person_id"] = ZION_ID
        assert data["ingest_as_receipt"]["tip"] == HDJ_INGEST_TIP
        path.write_text(dumps(data), encoding="utf-8")
        print("cite", path.relative_to(ROOT))


def patch_llms() -> None:
    from aziel_living import LLMS_LEAD

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
        if f"{APEX}/Press" not in text.split("## Marion")[0]:
            text = text.replace(
                f"- [{APEX}/Inquiries]({APEX}/Inquiries) — 23 inquiries of the record\n",
                (
                    f"- [{APEX}/Press]({APEX}/Press) — press tip + investigative source directory\n"
                    f"- [{APEX}/Inquiries]({APEX}/Inquiries) — 23 inquiries of the record\n"
                    f"- [{APEX}/Rubye]({APEX}/Rubye) — Rubye paper\n"
                    f"- [{APEX}/Archives]({APEX}/Archives) — archive / volume downloads\n"
                    f"- [{APEX}/FOIA]({APEX}/FOIA) — FOIA paper (supplied FBI FOIPA no-records only)\n"
                ),
                1,
            )
            text = text.replace(
                f"- [{APEX}/who]({APEX}/who) — Who is Aziel Eliab (HTML lock)\n",
                (
                    f"- [{APEX}/Copyrights]({APEX}/Copyrights) — copyrights / historical-research notice\n"
                    f"- [{APEX}/aziel]({APEX}/aziel) — About Aziel (one body)\n"
                    f"- [{APEX}/reader]({APEX}/reader) — facsimile volume reader\n"
                    f"- [{APEX}/who]({APEX}/who) — Who is Aziel Eliab (HTML lock)\n"
                ),
                1,
            )
            if f"{APEX}/openapi.json" not in text.split("## Marion")[0]:
                text = text.replace(
                    f"- [{APEX}/ingest-as-receipt.json]({APEX}/ingest-as-receipt.json) — canonical ingest bytes (one tip)\n",
                    (
                        f"- [{APEX}/ingest-as-receipt.json]({APEX}/ingest-as-receipt.json) — canonical ingest bytes (one tip)\n"
                        f"- [{APEX}/openapi.json]({APEX}/openapi.json) — read-only public surfaces\n"
                        f"- [{APEX}/ai.txt]({APEX}/ai.txt) — AI crawl aid\n"
                        f"- [{APEX}/.well-known/llms.txt]({APEX}/.well-known/llms.txt) — well-known rewrite to /llms.txt\n"
                    ),
                    1,
                )
        text = text.replace(
            f"[Official narrative]({APEX}/official-narrative.html)",
            f"[Official narrative]({APEX}/Narrative)",
        )
        text = text.replace(
            f"[Rubye paper]({APEX}/rubye.html)",
            f"[Rubye paper]({APEX}/Rubye)",
        )
        text = text.replace(
            f"[FOIA paper]({APEX}/foia.html)",
            f"[FOIA paper]({APEX}/FOIA)",
        )
        text = text.replace(
            f"[Copyrights & historical research notice]({APEX}/copyrights.html)",
            f"[Copyrights & historical research notice]({APEX}/Copyrights)",
        )
        if "Service → Clarity → Peace" not in text:
            text = text.replace(
                "Lamb Lens (Corpus ingest, not this host): https://www.azielcorpuslibrary.net/corpus",
                (
                    "Lamb Lens (Corpus ingest, not this host): https://www.azielcorpuslibrary.net/corpus\n"
                    "Lamb Lens order: Service → Clarity → Peace. HDJ is not a Lamb Lens ingest host."
                ),
                1,
            )
        path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        print("llms", path.relative_to(ROOT))

        full = tree / "llms-full.txt"
        ft = full.read_text(encoding="utf-8")
        ft = ft.replace(f"{APEX}/official-narrative.html", f"{APEX}/Narrative")
        ft = ft.replace(f"{APEX}/rubye.html", f"{APEX}/Rubye")
        ft = ft.replace(f"{APEX}/foia.html", f"{APEX}/FOIA")
        ft = ft.replace(f"{APEX}/copyrights.html", f"{APEX}/Copyrights")
        if "Service → Clarity → Peace" not in ft:
            ft = ft.replace(
                "Lamb Lens (Corpus ingest, not this host): https://www.azielcorpuslibrary.net/corpus",
                (
                    "Lamb Lens (Corpus ingest, not this host): https://www.azielcorpuslibrary.net/corpus\n"
                    "Lamb Lens order: Service → Clarity → Peace. HDJ is not a Lamb Lens ingest host."
                ),
                1,
            )
        full.write_text(ft if ft.endswith("\n") else ft + "\n", encoding="utf-8")
        print("llms-full", full.relative_to(ROOT))

        ai = tree / "ai.txt"
        at = ai.read_text(encoding="utf-8")
        if f"{APEX}/.well-known/llms.txt" not in at:
            at = at.replace(
                f"- {WWW}/openapi.json\n",
                f"- {WWW}/openapi.json\n- {APEX}/.well-known/llms.txt\n",
                1,
            )
        if "Service → Clarity → Peace" not in at:
            at = at.replace(
                "- Lamb Lens: https://www.azielcorpuslibrary.net/corpus (HDJ is not a Lamb Lens ingest host)",
                (
                    "- Lamb Lens: https://www.azielcorpuslibrary.net/corpus (HDJ is not a Lamb Lens ingest host)\n"
                    "- Lamb Lens order: Service → Clarity → Peace"
                ),
                1,
            )
        ai.write_text(at if at.endswith("\n") else at + "\n", encoding="utf-8")
        print("ai", ai.relative_to(ROOT))


def patch_money_jsonld() -> None:
    old = """      "alternateName": [
        "Marion Zioncheck",
        "Marion Anthony Zioncheck"
      ],"""
    new = """      "alternateName": [
        "Marion Zioncheck",
        "Marion Anthony Zioncheck",
        "Congressman Marion A. Zioncheck",
        "Congressman Zioncheck"
      ],"""
    alternates = (
        '<link rel="alternate" type="text/plain" href="https://hedidntjump.com/llms.txt" title="LLM instructions">\n'
        '<link rel="alternate" type="application/json" href="https://hedidntjump.com/cite.json" title="cite.json">\n'
        '<link rel="alternate" type="text/plain" href="https://hedidntjump.com/ai.txt" title="ai.txt">\n'
    )
    for tree in TREES:
        for name in ("index.html", "case.html"):
            path = tree / name
            text = path.read_text(encoding="utf-8")
            if old in text:
                text = text.replace(old, new, 1)
            if 'href="https://hedidntjump.com/cite.json"' not in text:
                if 'href="https://hedidntjump.com/llms.txt"' in text:
                    text = text.replace(
                        '<link rel="alternate" type="text/plain" href="https://hedidntjump.com/llms.txt" title="LLM instructions">\n',
                        alternates,
                        1,
                    )
                else:
                    text = text.replace(
                        '<link rel="canonical"',
                        alternates + '<link rel="canonical"',
                        1,
                    )
            path.write_text(text, encoding="utf-8")
            print("money-head", path.relative_to(ROOT))


def patch_edition_og() -> None:
    pages = {
        "press.html": {
            "og_title": "Press · Investigative Sources — He Didn't Jump",
            "og_desc": (
                "Public tip and newsroom emails for investigative outlets — "
                "ask them to look at the Marion Zioncheck archive on hedidntjump.com."
            ),
            "drop_inquires_alt": True,
        },
        "archives.html": {
            "og_title": "Archives — He Didn't Jump",
            "og_desc": "Research volumes and archive downloads — Marion Zioncheck collection on hedidntjump.com.",
            "drop_inquires_alt": True,
        },
    }
    for tree in TREES:
        for name, fields in pages.items():
            path = tree / name
            text = path.read_text(encoding="utf-8")
            text = re.sub(
                r'<meta property="og:title" content="[^"]*">',
                f'<meta property="og:title" content="{fields["og_title"]}">',
                text,
                count=1,
            )
            text = re.sub(
                r'<meta property="og:description" content="[^"]*">',
                f'<meta property="og:description" content="{fields["og_desc"]}">',
                text,
                count=1,
            )
            text = re.sub(
                r'<meta name="twitter:title" content="[^"]*">',
                f'<meta name="twitter:title" content="{fields["og_title"]}">',
                text,
                count=1,
            )
            if 'name="twitter:description"' not in text:
                text = text.replace(
                    f'<meta name="twitter:title" content="{fields["og_title"]}">\n',
                    (
                        f'<meta name="twitter:title" content="{fields["og_title"]}">\n'
                        f'<meta name="twitter:description" content="{fields["og_desc"]}">\n'
                    ),
                    1,
                )
            if fields["drop_inquires_alt"]:
                text = re.sub(
                    r'<link rel="alternate" href="https://hedidntjump.com/inquires.html">\n',
                    "",
                    text,
                    count=1,
                )
            path.write_text(text, encoding="utf-8")
            print("edition-og", path.relative_to(ROOT))


def patch_cold_shelf_writer() -> None:
    """Keep lamb_lens order if write_cold_shelf is re-run later."""
    path = ROOT / "scripts" / "write_cold_shelf.py"
    text = path.read_text(encoding="utf-8")
    old = (
        '        "lamb_lens": {\n'
        '            "shelf": "https://www.azielcorpuslibrary.net/corpus",\n'
        '            "note": "Public Lamb Lens / Corpus ingest lives on azielcorpuslibrary.net. This host is not a Lamb Lens ingest host.",\n'
        "        },"
    )
    new = (
        '        "lamb_lens": {\n'
        '            "shelf": "https://www.azielcorpuslibrary.net/corpus",\n'
        '            "order": "Service → Clarity → Peace",\n'
        '            "note": "Public Lamb Lens / Corpus ingest lives on azielcorpuslibrary.net. This host is not a Lamb Lens ingest host.",\n'
        "        },"
    )
    if old in text and "Service → Clarity → Peace" not in text:
        path.write_text(text.replace(old, new, 1), encoding="utf-8")
        print("writer", path.relative_to(ROOT))


def patch_serp_writer() -> None:
    path = ROOT / "scripts" / "write_zioncheck_serp.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        """        "alternateName": [
            "Marion Zioncheck",
            "Marion Anthony Zioncheck",
        ],""",
        """        "alternateName": [
            "Marion Zioncheck",
            "Marion Anthony Zioncheck",
            "Congressman Marion A. Zioncheck",
            "Congressman Zioncheck",
        ],""",
        1,
    )
    if '("/Press", "0.8")' in text and '"/who"' not in text[text.find("def write_sitemap") :]:
        text = text.replace(
            '        ("/receipts", "0.4"),\n    ]',
            '        ("/receipts", "0.4"),\n        ("/who", "0.6"),\n    ]',
            1,
        )
        text = text.replace(
            '        ("/.well-known/aziel.json", "0.3"),\n    ]',
            (
                '        ("/.well-known/aziel.json", "0.3"),\n'
                '        ("/.well-known/llms.txt", "0.4"),\n'
                '        ("/redline", "0.4"),\n'
                '        ("/redline.json", "0.4"),\n'
                '        ("/runtime-launch.json", "0.4"),\n'
                "    ]"
            ),
            1,
        )
    text = text.replace(
        """                f"{APEX}/Inquiries",
                f"{APEX}/Volumes",
                f"{APEX}/receipts",
                f"{APEX}/ingest-as-receipt.json",
                f"{APEX}/llms.txt",
                f"{APEX}/shelves",
                f"{APEX}/lockset.json",
            ],""",
        """                f"{APEX}/Press",
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
            ],""",
        1,
    )
    path.write_text(text, encoding="utf-8")
    print("writer", path.relative_to(ROOT))


PAGE_HEADS = {
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
    "receipts.html": f"{APEX}/receipts",
    "who.html": f"{APEX}/who",
}

AZIEL_ABOUT = {"aziel.html", "who.html"}
NEED_WEBPAGE = {
    "press.html",
    "archives.html",
    "inquiries.html",
    "inquires.html",
    "who.html",
}

STALE_JSONLD_URLS = (
    (f"{APEX}/rubye.html", f"{APEX}/Rubye"),
    (f"{APEX}/foia.html", f"{APEX}/FOIA"),
    (f"{APEX}/copyrights.html", f"{APEX}/Copyrights"),
    (f"{APEX}/official-narrative.html", f"{APEX}/Narrative"),
    (f"{APEX}/reader.html", f"{APEX}/reader"),
)


def _attr(html: str, pattern: str) -> str | None:
    m = re.search(pattern, html, flags=re.I)
    return m.group(1) if m else None


def _set_or_insert_meta(text: str, attr: str, name: str, value: str) -> str:
    pattern = rf'<meta {attr}="{name}" content="[^"]*">'
    repl = f'<meta {attr}="{name}" content="{value}">'
    if re.search(pattern, text, flags=re.I):
        return re.sub(pattern, repl, text, count=1, flags=re.I)
    anchor = "</head>"
    return text.replace(anchor, repl + "\n" + anchor, 1)


def patch_sitewide_pages() -> None:
    for tree in TREES:
        for name, canonical in PAGE_HEADS.items():
            path = tree / name
            text = path.read_text(encoding="utf-8")
            title = _attr(text, r"<title>([^<]*)</title>")
            desc = _attr(text, r'<meta name="description" content="([^"]*)"')
            assert title and desc, name

            if 'rel="canonical"' in text:
                text = re.sub(
                    r'<link rel="canonical" href="[^"]*">',
                    f'<link rel="canonical" href="{canonical}">',
                    text,
                    count=1,
                )
            text = _set_or_insert_meta(text, "property", "og:title", title)
            text = _set_or_insert_meta(text, "property", "og:description", desc)
            text = _set_or_insert_meta(text, "property", "og:url", canonical)
            if 'property="og:type"' not in text:
                text = _set_or_insert_meta(text, "property", "og:type", "article")
            if 'property="og:site_name"' not in text:
                text = _set_or_insert_meta(
                    text, "property", "og:site_name", "He Didn't Jump — An Aziel Eliab Project"
                )
            text = _set_or_insert_meta(text, "name", "twitter:title", title)
            text = _set_or_insert_meta(text, "name", "twitter:description", desc)
            if 'name="twitter:card"' not in text:
                text = _set_or_insert_meta(text, "name", "twitter:card", "summary_large_image")

            if f'href="{APEX}/llms.txt"' not in text and 'href="/llms.txt"' not in text:
                text = text.replace(
                    f'<link rel="canonical" href="{canonical}">\n',
                    (
                        f'<link rel="canonical" href="{canonical}">\n'
                        f'<link rel="alternate" type="text/plain" href="{APEX}/llms.txt" title="LLM instructions">\n'
                    ),
                    1,
                )
            if f'href="{APEX}/cite.json"' not in text and 'href="/cite.json"' not in text:
                text = text.replace(
                    f'<link rel="canonical" href="{canonical}">\n',
                    (
                        f'<link rel="canonical" href="{canonical}">\n'
                        f'<link rel="alternate" type="application/json" href="{APEX}/cite.json" title="cite.json">\n'
                    ),
                    1,
                )

            if name in NEED_WEBPAGE and 'data-azindex="webpage"' not in text:
                about = PERSON_ID if name in AZIEL_ABOUT else ZION_ID
                block = (
                    '<script type="application/ld+json" data-azindex="webpage">\n'
                    + dumps(
                        {
                            "@context": "https://schema.org",
                            "@type": "WebPage",
                            "@id": f"{canonical.rstrip('/') }#webpage",
                            "url": canonical,
                            "name": title,
                            "description": desc,
                            "isPartOf": {"@id": f"{APEX}/#website"},
                            "about": {"@id": about},
                            "author": {"@id": PERSON_ID},
                            "isAccessibleForFree": True,
                            "inLanguage": "en",
                        }
                    )
                    + "</script>\n"
                )
                text = text.replace("</head>", block + "</head>", 1)
            if name not in AZIEL_ABOUT and ZION_ID not in text and 'data-azindex="marion"' not in text:
                marion = (
                    '<script type="application/ld+json" data-azindex="marion">\n'
                    + dumps(
                        {
                            "@context": "https://schema.org",
                            "@type": "Person",
                            "@id": ZION_ID,
                            "name": "Marion A. Zioncheck",
                            "alternateName": MARION_AKA,
                            "jobTitle": "U.S. Representative",
                            "url": f"{APEX}/",
                            "sameAs": MARION_SAME_AS,
                        }
                    )
                    + "</script>\n"
                )
                text = text.replace("</head>", marion + "</head>", 1)

            def _rewrite_jsonld(match: re.Match[str]) -> str:
                body = match.group(0)
                for old, new in STALE_JSONLD_URLS:
                    body = body.replace(old, new)
                return body

            text = re.sub(
                r'<script type="application/ld\+json"[^>]*>[\s\S]*?</script>',
                _rewrite_jsonld,
                text,
            )
            path.write_text(text, encoding="utf-8")
            print("page-head", path.relative_to(ROOT))


def main() -> None:
    patch_robots()
    patch_headers()
    patch_redirects()
    patch_sitemap()
    patch_openapi()
    patch_cite()
    patch_llms()
    patch_money_jsonld()
    patch_edition_og()
    patch_sitewide_pages()
    patch_cold_shelf_writer()
    patch_serp_writer()
    print("AZindex GROWTH-ON written; ingest tip unchanged")


if __name__ == "__main__":
    main()
