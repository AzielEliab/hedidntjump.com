#!/usr/bin/env python3
"""Assert Aziel publisher name lattice + Hebrew + GitHub on machine surfaces."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from aziel_works import (
    AZOS_URL,
    INTERFACE_PAPER,
    INTERFACE_URL,
    RUNTIME_ENDPOINT,
    RUNTIME_GLAMA,
    RUNTIME_URL,
    TRIAD_DESCRIPTION,
    TRIAD_ID,
    TRIAD_NAME,
)
from aziel_person import (
    GITHUB_PRIMARY,
    GITHUB_REVEALER,
    HEBREW_ONELINER,
    HUB_SAME_AS,
    LOCKED_JOB_TITLES,
    PERSON_ID,
    PERSON_NAME,
    REQUIRED_AKA,
    assert_person_lock,
)

ROOT = Path(__file__).resolve().parents[1]
HTML = (
    "index.html",
    "case.html",
    "aziel.html",
    "who.html",
    "press.html",
    "inquiries.html",
    "inquires.html",
    "rubye.html",
    "archives.html",
    "foia.html",
    "volumes.html",
    "reader.html",
    "official-narrative.html",
    "copyrights.html",
)
MONEY = {"index.html", "case.html"}
MONEY_TITLE = "Marion A. Zioncheck — Seattle Congressman (1933–1936) Archive | He Didn't Jump"
MONEY_H1 = '<h1 class="headline">Marion A. Zioncheck, Seattle congressman</h1>'


def _person_from_html(html: str) -> dict:
    found = []
    for raw in re.findall(
        r'<script type="application/ld\+json">([\s\S]*?)</script>', html
    ):
        data = json.loads(raw)

        def walk(obj):
            if isinstance(obj, dict):
                if obj.get("@id") == PERSON_ID and obj.get("name") == PERSON_NAME:
                    found.append(obj)
                for v in obj.values():
                    walk(v)
            elif isinstance(obj, list):
                for v in obj:
                    walk(v)

        walk(data)
    assert found, "no Aziel Person node"
    return found[0]


def main() -> None:
    for tree in ("docs", "dist"):
        person = json.loads((ROOT / tree / "person.jsonld").read_text(encoding="utf-8"))
        identity = json.loads((ROOT / tree / "identity.jsonld").read_text(encoding="utf-8"))
        graph = json.loads((ROOT / tree / "graph.jsonld").read_text(encoding="utf-8"))
        well = json.loads((ROOT / tree / ".well-known/aziel.json").read_text(encoding="utf-8"))
        cite = json.loads((ROOT / tree / "cite.json").read_text(encoding="utf-8"))
        who = (ROOT / tree / "who-is-aziel-eliab.txt").read_text(encoding="utf-8")
        who_plain = (ROOT / tree / "who-is").read_text(encoding="utf-8")
        llms = (ROOT / tree / "llms.txt").read_text(encoding="utf-8")
        llms_full = (ROOT / tree / "llms-full.txt").read_text(encoding="utf-8")
        ai = (ROOT / tree / "ai.txt").read_text(encoding="utf-8")

        works_doc = json.loads((ROOT / tree / "works.json").read_text(encoding="utf-8"))
        assert works_doc["person_id"] == PERSON_ID
        assert works_doc["works"]
        triad = works_doc.get("az_triad") or {}
        assert triad.get("@id") == TRIAD_ID
        assert triad.get("name") == TRIAD_NAME
        assert triad.get("description") == TRIAD_DESCRIPTION
        assert triad.get("author") == {"@id": PERSON_ID}
        assert triad.get("creator") == {"@id": PERSON_ID}
        parts = {part.get("url"): part for part in triad.get("hasPart") or []}
        assert set(parts) == {AZOS_URL, RUNTIME_URL, INTERFACE_URL}
        assert "not a kernel" in parts[AZOS_URL]["description"]
        assert RUNTIME_ENDPOINT in parts[RUNTIME_URL]["description"]
        assert RUNTIME_GLAMA in parts[RUNTIME_URL]["description"]
        assert INTERFACE_PAPER in parts[INTERFACE_URL]["description"]
        triad_blob = json.dumps(triad).lower()
        assert "mesh-node" not in triad_blob
        assert "one-click" not in triad_blob
        assert "live" not in triad_blob
        sides = {
            work.get("url"): work
            for work in works_doc["works"]
            if isinstance(work, dict)
        }
        for url in (AZOS_URL, RUNTIME_URL, RUNTIME_ENDPOINT, INTERFACE_URL):
            work = sides[url.rstrip("/")] if url.rstrip("/") in sides else sides[url]
            assert work["isPartOf"]["@id"] == TRIAD_ID
            assert "side of the AZ triad" in work["description"]
        works_blob = json.dumps(works_doc)
        assert "doi.org" not in works_blob and "zenodo.org" not in works_blob
        assert "Webslinger (Wearable Dual-Tether Web-Sling System)" in works_blob
        cite_works = cite.get("works") or []
        assert len(cite_works) == len(works_doc["works"])
        assert cite.get("az_triad") == triad
        assert_person_lock(person)
        assert "works.json" in json.dumps(person) or any(
            isinstance(work, dict) and str(work.get("url", "")).startswith("https://")
            for work in person.get("workExample") or []
        )
        assert any(
            isinstance(work, dict) and "Webslinger" in (work.get("name") or "")
            for work in person.get("workExample") or []
        )
        assert any(
            isinstance(work, dict) and "AZDOC-E03E61D8E50B" in (work.get("url") or "")
            for work in person.get("workExample") or []
        )
        assert any(
            isinstance(work, dict) and work.get("@id") == TRIAD_ID
            for work in person.get("workExample") or []
        )
        blob = json.dumps(person)
        assert "doi.org" not in blob and "zenodo.org" not in blob
        ident_person = identity.get("person") if isinstance(identity.get("person"), dict) else identity
        if ident_person.get("@id") == PERSON_ID:
            assert_person_lock(ident_person)
        aziel = next(n for n in graph["@graph"] if n.get("@id") == PERSON_ID)
        assert_person_lock(aziel)
        assert well["person_id"] == PERSON_ID
        assert HEBREW_ONELINER in json.dumps(well, ensure_ascii=False)
        assert HEBREW_ONELINER in json.dumps(cite, ensure_ascii=False)
        assert cite.get("stats") == "https://www.hedidntjump.com/api/stats"
        for blob in (who, who_plain):
            assert "Marion Zioncheck" in blob
            assert "FOIA Binary Acknowledgement" in blob
            assert "official-narrative" in blob
            assert "five volumes" in blob or "Volumes I–V" in blob
            assert "An Aziel Eliab Project" in blob
            assert "living author of He Didn’t Jump" in blob or "living author of He Didn't Jump" in blob
            assert "https://www.hedidntjump.com/api/stats" in blob
        for blob in (llms, llms_full):
            assert TRIAD_ID in blob
            assert TRIAD_NAME in blob
            assert "Design relationship only." in blob
            assert "not a kernel" in blob
        for blob in (who, who_plain, llms, ai):
            assert PERSON_ID in blob
            assert "Elias Artista" in blob
            assert HEBREW_ONELINER in blob
            assert GITHUB_PRIMARY in blob
            assert GITHUB_REVEALER in blob
            assert "https://x.com/AzielEliab" in blob
            assert "@AzielEliab" in blob
            assert "https://glama.ai/mcp/servers/AzielEliab/aziel-runtime" in blob
            assert "Everblooming Flower" not in blob
            assert "euaziel.site" in blob or "Never sameAs euaziel" in blob

        idx = (ROOT / tree / "index.html").read_text(encoding="utf-8")
        case = (ROOT / tree / "case.html").read_text(encoding="utf-8")
        assert MONEY_TITLE in idx
        assert MONEY_H1 in idx and MONEY_H1 in case

        for name in HTML:
            html = (ROOT / tree / name).read_text(encoding="utf-8")
            node = _person_from_html(html)
            assert_person_lock(node)
            assert node["jobTitle"] == list(LOCKED_JOB_TITLES)
            if name in {"index.html", "aziel.html"}:
                examples = node.get("workExample") or []
                assert any(
                    isinstance(work, dict) and "Webslinger" in (work.get("name") or "")
                    for work in examples
                )
                assert any(
                    isinstance(work, dict) and work.get("@id") == TRIAD_ID
                    for work in examples
                )
                linked = {
                    str(work.get("url") or "").rstrip("/"): work
                    for work in examples
                    if isinstance(work, dict)
                }
                for url in (AZOS_URL, RUNTIME_URL, RUNTIME_ENDPOINT.rstrip("/")):
                    match = linked[url]
                    assert match["isPartOf"]["@id"] == TRIAD_ID
                    assert "side of the AZ triad" in (match.get("description") or "")
                assert "doi.org" not in json.dumps(node)
            else:
                assert not any(
                    isinstance(work, dict) and str(work.get("@id") or "").endswith("#aziel-work")
                    for work in node.get("workExample") or []
                )
                assert TRIAD_ID not in html
            if name in MONEY:
                assert "Publisher of this Marion Zioncheck archive" in html
            assert PERSON_ID in html
            for aka in REQUIRED_AKA:
                assert aka in html
            for hub in HUB_SAME_AS:
                assert hub in html

    print("aziel publisher lattice OK")


if __name__ == "__main__":
    main()
