#!/usr/bin/env python3
"""Assert AZindex GROWTH-ON discovery lattice (no tip-hash change)."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APEX = "https://hedidntjump.com"
PERSON_ID = "https://www.azieleliab.com/#aziel"
ZION_ID = f"{APEX}/#marion-zioncheck"
HDJ_INGEST_TIP = "ef967e4acb47ba913ce3959b673767278da605b307de33210b2dc2f1cfd86f60"

ANTI_LOOP = (
    "/who /who.html 200",
    "/aziel /aziel.html 200",
    "/reader /reader.html 200",
    "/receipts /receipts.html 200",
)

PUBLIC_PAGES = (
    "/",
    "/Case",
    "/Press",
    "/Inquiries",
    "/Rubye",
    "/Archives",
    "/FOIA",
    "/Volumes",
    "/reader",
    "/Narrative",
    "/aziel",
    "/Copyrights",
    "/who",
    "/receipts",
)

AI_AGENTS = (
    "GPTBot",
    "ChatGPT-User",
    "OAI-SearchBot",
    "Google-Extended",
    "ClaudeBot",
    "Claude-Web",
    "Claude-User",
    "PerplexityBot",
    "Perplexity-User",
    "Google-CloudVertexBot",
    "YouBot",
    "MistralAI-User",
)


def visible_text(html: str) -> str:
    html = re.sub(r"<script\b[^>]*>[\s\S]*?</script>", " ", html, flags=re.I)
    html = re.sub(r"<style\b[^>]*>[\s\S]*?</style>", " ", html, flags=re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    return html


def main() -> None:
    ingest = (ROOT / "dist" / "ingest-as-receipt.json").read_bytes()
    assert hashlib.sha256(ingest).hexdigest() == HDJ_INGEST_TIP

    for tree_name in ("docs", "dist"):
        tree = ROOT / tree_name
        assert (tree / "ingest-as-receipt.json").read_bytes() == ingest

        robots = (tree / "robots.txt").read_text(encoding="utf-8")
        star = robots.split("User-agent: Googlebot")[0]
        assert "Growth-ON" in robots
        assert "Content-Signal: search=yes, ai-input=yes, ai-train=yes" in star
        assert "Allow: /" in star
        assert "Disallow: /api/" in star
        assert "Disallow: GPTBot" not in robots
        assert "Disallow: Claude" not in robots
        for agent in AI_AGENTS:
            assert f"User-agent: {agent}" in robots, agent
            idx = robots.find(f"User-agent: {agent}")
            chunk = robots[idx : idx + 80]
            assert "Allow: /" in chunk, agent

        headers = (tree / "_headers").read_text(encoding="utf-8")
        assert "Content-Signal: search=yes, ai-input=yes, ai-train=yes" in headers
        assert 'rel="describedby"' in headers
        assert "/llms.txt" in headers
        assert "/cite.json" in headers
        assert "/.well-known/llms.txt" in headers
        assert "/volumes.json" in headers
        html_rules = headers.split("/style.css")[0]
        assert "Cache-Control: no-store" not in html_rules

        redirects = (tree / "_redirects").read_text(encoding="utf-8")
        assert "/.well-known/llms.txt /llms.txt 200" in redirects
        for banned in ANTI_LOOP:
            assert banned not in redirects, banned

        sitemap = (tree / "sitemap.xml").read_text(encoding="utf-8")
        assert sitemap.count("<priority>1.0</priority>") == 1
        for loc in PUBLIC_PAGES + (
            "/cite.json",
            "/llms.txt",
            "/openapi.json",
            "/.well-known/llms.txt",
            "/runtime-launch.json",
            "/shelves",
            "/help.txt",
            "/addendum.txt",
            "/help/how-to-read.txt",
        ):
            assert f"<loc>{APEX}{loc}</loc>" in sitemap, loc

        openapi = json.loads((tree / "openapi.json").read_text(encoding="utf-8"))
        for loc in (
            "/who-is",
            "/graph.jsonld",
            "/identity.jsonld",
            "/mcp.json",
            "/.well-known/mcp.json",
            "/.well-known/aziel.json",
            "/.well-known/llms.txt",
            "/sitemap-index.xml",
            "/volumes.json",
            "/runtime-launch.json",
            "/shelves",
            "/help.txt",
            "/addendum.txt",
            "/help/how-to-read.txt",
        ):
            assert loc in openapi["paths"], loc
        assert "No local MCP" in openapi["info"]["description"]

        cite = json.loads((tree / "cite.json").read_text(encoding="utf-8"))
        assert cite["person_id"] == PERSON_ID
        assert cite["marion_person_id"] == ZION_ID
        assert cite["growth_on"] is True
        assert cite["mcp_local"] is False
        assert cite["ingest_as_receipt"]["tip"] == HDJ_INGEST_TIP
        assert cite["lamb_lens"]["order"] == "Service → Clarity → Peace"
        assert cite["zenodo_tip_pack"]["doi"] is None
        for u in PUBLIC_PAGES:
            assert f"{APEX}{u}" in cite["query_urls"] or (
                u == "/" and f"{APEX}/" in cite["query_urls"]
            ), u
        for url in (
            "https://www.historylink.org/File/5528",
            "https://id.loc.gov/authorities/names/n87891358",
        ):
            assert url in cite["marion_person"]["sameAs"]
        assert "Congressman Zioncheck" in cite["marion_person"]["alternateName"]

        llms = (tree / "llms.txt").read_text(encoding="utf-8")
        lead = llms.split("## Marion")[0]
        assert "NOT an ARG" not in lead
        assert "whistleblower" in lead.lower()
        for loc in ("/Press", "/Rubye", "/Archives", "/FOIA", "/Copyrights", "/reader", "/who"):
            assert f"{APEX}{loc}" in lead, loc
        assert "Service → Clarity → Peace" in llms
        assert HDJ_INGEST_TIP in llms

        ai = (tree / "ai.txt").read_text(encoding="utf-8")
        assert "Service → Clarity → Peace" in ai
        assert "aziel-runtime" in ai.lower() or "glama" in ai.lower()
        assert "NOT an ARG" not in ai
        assert "whistleblower" in ai.lower()

        idx = (tree / "index.html").read_text(encoding="utf-8")
        case = (tree / "case.html").read_text(encoding="utf-8")
        for html in (idx, case):
            marion = re.search(
                r'"@id": "https://hedidntjump.com/#marion-zioncheck",[\s\S]*?"alternateName": \[([\s\S]*?)\]',
                html,
            )
            assert marion, "missing Marion Person alternateName"
            assert "Congressman Marion A. Zioncheck" in marion.group(1)
            assert "Congressman Zioncheck" in marion.group(1)
            assert ZION_ID in html
            assert PERSON_ID in html
            assert 'href="https://hedidntjump.com/cite.json"' in html
            assert 'href="https://hedidntjump.com/ai.txt"' in html

        press = (tree / "press.html").read_text(encoding="utf-8")
        archives = (tree / "archives.html").read_text(encoding="utf-8")
        assert 'og:title" content="Press · Investigative Sources — He Didn\'t Jump"' in press
        assert "Inquiries of the Record" not in press.split("<body", 1)[0]
        assert 'og:title" content="Archives — He Didn\'t Jump"' in archives
        assert "inquires.html" not in press
        assert "inquires.html" not in archives

        pages = {
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
        for name, canonical in pages.items():
            html = (tree / name).read_text(encoding="utf-8")
            title = re.search(r"<title>([^<]*)</title>", html).group(1)
            desc = re.search(r'<meta name="description" content="([^"]*)"', html).group(1)
            assert f'href="{canonical}"' in html
            assert f'og:title" content="{title}"' in html
            assert f'og:description" content="{desc}"' in html
            assert f'og:url" content="{canonical}"' in html
            assert f'twitter:title" content="{title}"' in html
            assert f'twitter:description" content="{desc}"' in html
            assert "application/ld+json" in html
            if name in {
                "press.html",
                "archives.html",
                "inquiries.html",
                "inquires.html",
                "who.html",
            }:
                assert 'data-azindex="webpage"' in html
            if name not in {"aziel.html", "who.html"}:
                assert ZION_ID in html or "marion-zioncheck" in html
            assert PERSON_ID in html

        mcp = json.loads((tree / "mcp.json").read_text(encoding="utf-8"))
        assert "no local MCP" in mcp["mcpServers"]["aziel-runtime"]["note"]

        for name in (
            "index.html",
            "case.html",
            "press.html",
            "archives.html",
            "receipts.html",
        ):
            html = (tree / name).read_text(encoding="utf-8")
            visible = visible_text(html)
            assert "lock-1520" not in html
            if name != "who.html":
                assert "15:20" not in visible
            nav = re.search(r'<nav class="paper-tabs"[\s\S]*?</nav>', html)
            if nav:
                assert "Receipts" not in nav.group(0)
                assert "Pg. 11" not in nav.group(0)

    print("AZindex GROWTH-ON OK")
    print("ingest_tip", HDJ_INGEST_TIP)


if __name__ == "__main__":
    main()
