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
        assert pub["name"] == "Aziel Eliab"
        assert "Elias Artista" in pub["alternateName"]
        assert "The Revealer of The Sealed" in pub["alternateName"]
        assert "Aziel Elroi Eliab" in pub["alternateName"]
        assert "Everblooming Flower" not in json.dumps(pub)
        assert "https://github.com/AzielEliab" in pub["sameAs"]
        assert "https://github.com/azieltherevealerofthesealed-arch" in pub["sameAs"]
        for hub in (
            "https://www.azieleliab.com/",
            "https://www.azielcorpuslibrary.net/",
            "https://godlock.uk/",
            "https://www.hedidntjump.com/",
        ):
            assert hub in pub["sameAs"], hub
        hebrew = (
            "Aziel Elroi Eliab (עזיאל אל ראי אליאב / עזיאל אלרועי אליאב): "
            "Aziel = God is my strength (עזיאל); Elroi = God who sees (אל ראי / אלרועי); "
            "Eliab = God is father (אליאב)."
        )
        assert hebrew in json.dumps(pub, ensure_ascii=False)
        assert "Publisher of this Marion Zioncheck archive" in idx
        assert "Aziel Eliab only" in idx
        assert "euaziel.site" in idx
        assert sitemap.count("<priority>1.0</priority>") == 1
        assert f"<loc>{APEX}/</loc>" in sitemap
        assert f"<loc>{APEX}/Case</loc>" in sitemap
        assert "https://www.hedidntjump.com/* https://hedidntjump.com/:splat 301" in redirects
        assert "https://hedidntjump.com/* https://www.hedidntjump.com/:splat 301" not in redirects
        assert llms.startswith("# He Didn't Jump — Marion A. Zioncheck archive")
        assert "NOT an ARG" not in llms
        assert "whistleblower" in llms.lower()
        assert "Marion A. Zioncheck" in llms
        # Machine surfaces (cite / llms / graph) — no HTML required for Marion FAQ
        cite = json.loads((ROOT / tree / "cite.json").read_text(encoding="utf-8"))
        assert cite["marion_person_id"] == f"{APEX}/#marion-zioncheck"
        assert cite["marion_person"]["name"] == "Marion A. Zioncheck"
        assert len(cite["zioncheck_faq"]) >= 5
        assert any(q["q"] == "Who was Marion A. Zioncheck?" for q in cite["zioncheck_faq"])
        assert all("ARG" not in q["q"] for q in cite["zioncheck_faq"])
        assert "NOT an ARG" not in cite["purpose"]
        assert "whistleblower" in cite["purpose"]
        assert "Aziel Eliab only" in cite.get("disambiguatingDescription", "") + json.dumps(cite)
        graph_doc = json.loads((ROOT / tree / "graph.jsonld").read_text(encoding="utf-8"))
        assert graph_doc["@graph"][0]["@id"] == f"{APEX}/#marion-zioncheck"
        assert any(n.get("@id") == "https://www.hedidntjump.com/#zioncheck-faq" for n in graph_doc["@graph"])
        assert any(n.get("@id") == "https://www.azieleliab.com/#aziel" for n in graph_doc["@graph"])
        assert "## Marion A. Zioncheck FAQ (machine)" in llms
        assert "Who was Congressman Zioncheck?" in llms
        # No second meter / stats rewrite in this lane.
        assert "views" in idx and "downloads" in idx
    print("zioncheck SERP lock OK")


if __name__ == "__main__":
    main()
