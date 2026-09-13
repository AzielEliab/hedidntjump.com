#!/usr/bin/env python3
"""Assert Marion Zioncheck money-page SERP lock (published facts only)."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APEX = "https://hedidntjump.com"
TITLE = "Marion A. Zioncheck — Seattle Congressman (1933–1936) Archive | He Didn't Jump"
CASE_TITLE = "The Case — Marion A. Zioncheck, Seattle congressman | He Didn't Jump"
H1 = '<h1 class="headline">Marion A. Zioncheck, Seattle congressman</h1>'


def graph(html: str) -> dict:
    raw = re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>', html)
    assert raw, "missing JSON-LD"
    return json.loads(raw.group(1))


def main() -> None:
    for tree in ("docs", "dist"):
        idx = (ROOT / tree / "index.html").read_text(encoding="utf-8")
        case = (ROOT / tree / "case.html").read_text(encoding="utf-8")
        narrative = (ROOT / tree / "official-narrative.html").read_text(encoding="utf-8")
        headers = (ROOT / tree / "_headers").read_text(encoding="utf-8")
        sitemap = (ROOT / tree / "sitemap.xml").read_text(encoding="utf-8")
        redirects = (ROOT / tree / "_redirects").read_text(encoding="utf-8")
        llms = (ROOT / tree / "llms.txt").read_text(encoding="utf-8")
        assert TITLE in idx
        assert CASE_TITLE in case
        assert "U.S. Representative and Seattle congressman" in idx
        assert "Arctic Building" in idx and "7 August 1936" in idx
        assert "re-examines" in idx
        assert H1 in idx and H1 in case
        assert f'href="{APEX}/"' in idx
        assert f'href="{APEX}/Case"' in case
        assert f'href="{APEX}/Narrative"' in narrative
        assert "Official Narrative" in narrative or "official" in narrative.lower()
        assert TITLE not in narrative
        assert "stale-while-revalidate=86400" in headers
        html_rules = headers.split("/style.css")[0]
        assert "Cache-Control: no-store" not in html_rules
        assert 'http-equiv="Cache-Control"' not in idx
        assert "Crazytown" not in idx and "Crazytown" not in case and "Crazytown" not in llms
        g = graph(idx)
        assert g["@graph"][0]["@id"] == f"{APEX}/#marion-zioncheck"
        assert g["@graph"][0]["name"] == "Marion A. Zioncheck"
        assert any(n.get("@type") == "FAQPage" for n in g["@graph"])
        pub = next(n for n in g["@graph"] if n.get("@id") == "https://www.azieleliab.com/#aziel")
        assert pub["jobTitle"] == "Publisher"
        assert "Not biblical Aziel; not biblical Eliab" in idx
        assert "not euaziel.site" in idx
        assert "not Aziel S. (Flutter/portfolio)" in idx
        assert "not other engineers named Aziel" in idx
        assert sitemap.count("<priority>1.0</priority>") == 1
        assert f"<loc>{APEX}/</loc>" in sitemap
        assert f"<loc>{APEX}/Case</loc>" in sitemap
        assert "https://www.hedidntjump.com/* https://hedidntjump.com/:splat 301" in redirects
        assert "https://hedidntjump.com/* https://www.hedidntjump.com/:splat 301" not in redirects
        assert llms.startswith("# He Didn't Jump — Marion A. Zioncheck archive")
        # No second meter / stats rewrite in this lane.
        assert "views" in idx and "downloads" in idx
    print("zioncheck SERP lock OK")


if __name__ == "__main__":
    main()
