#!/usr/bin/env python3
"""Assert Marion Zioncheck money-page SERP lock (published facts only)."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TITLE = "Marion A. Zioncheck — Seattle Congressman (1933–1936) Archive | He Didn't Jump"
H1 = '<h1 class="headline">Marion A. Zioncheck, Seattle congressman</h1>'


def graph(html: str) -> dict:
    raw = re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>', html)
    assert raw, "missing JSON-LD"
    return json.loads(raw.group(1))


def main() -> None:
    for tree in ("docs", "dist"):
        idx = (ROOT / tree / "index.html").read_text(encoding="utf-8")
        case = (ROOT / tree / "case.html").read_text(encoding="utf-8")
        headers = (ROOT / tree / "_headers").read_text(encoding="utf-8")
        sitemap = (ROOT / tree / "sitemap.xml").read_text(encoding="utf-8")
        llms = (ROOT / tree / "llms.txt").read_text(encoding="utf-8")
        assert TITLE in idx and TITLE in case
        assert "U.S. Representative and Seattle congressman" in idx
        assert "Arctic Building" in idx and "7 August 1936" in idx
        assert "re-examines" in idx
        assert H1 in idx and H1 in case
        assert 'href="https://www.hedidntjump.com/"' in idx
        assert 'href="https://www.hedidntjump.com/Case"' in case
        assert "stale-while-revalidate=86400" in headers
        html_rules = headers.split("/style.css")[0]
        assert "Cache-Control: no-store" not in html_rules
        assert 'http-equiv="Cache-Control"' not in idx
        assert "Crazytown" not in idx and "Crazytown" not in case and "Crazytown" not in llms
        g = graph(idx)
        assert g["@graph"][0]["@id"] == "https://www.hedidntjump.com/#marion-zioncheck"
        assert g["@graph"][0]["name"] == "Marion A. Zioncheck"
        assert any(n.get("@type") == "FAQPage" for n in g["@graph"])
        pub = next(n for n in g["@graph"] if n.get("@id") == "https://www.azieleliab.com/#aziel")
        assert pub["jobTitle"] == "Publisher"
        assert "Not biblical Aziel or Eliab" in idx
        assert "not euaziel.site" in idx
        assert "not Aziel S." in idx
        assert sitemap.count("<priority>1.0</priority>") == 2
        assert "<loc>https://www.hedidntjump.com/</loc>" in sitemap
        assert "<loc>https://www.hedidntjump.com/Case</loc>" in sitemap
        assert "<loc>https://hedidntjump.com/</loc>" not in sitemap
        assert llms.startswith("# He Didn't Jump — Marion A. Zioncheck archive")
    print("zioncheck SERP lock OK")


if __name__ == "__main__":
    main()
