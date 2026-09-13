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

from aziel_person import (
    GITHUB_PRIMARY,
    GITHUB_REVEALER,
    HEBREW_ONELINER,
    HUB_SAME_AS,
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
        ai = (ROOT / tree / "ai.txt").read_text(encoding="utf-8")

        assert_person_lock(person)
        ident_person = identity.get("person") if isinstance(identity.get("person"), dict) else identity
        if ident_person.get("@id") == PERSON_ID:
            assert_person_lock(ident_person)
        aziel = next(n for n in graph["@graph"] if n.get("@id") == PERSON_ID)
        assert_person_lock(aziel)
        assert well["person_id"] == PERSON_ID
        assert HEBREW_ONELINER in json.dumps(well, ensure_ascii=False)
        assert HEBREW_ONELINER in json.dumps(cite, ensure_ascii=False)
        for blob in (who, who_plain, llms, ai):
            assert PERSON_ID in blob
            assert "Elias Artista" in blob
            assert HEBREW_ONELINER in blob
            assert GITHUB_PRIMARY in blob
            assert GITHUB_REVEALER in blob
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
            if name in MONEY:
                assert node["jobTitle"] == "Publisher"
            assert PERSON_ID in html
            for aka in REQUIRED_AKA:
                assert aka in html
            for hub in HUB_SAME_AS:
                assert hub in html

    print("aziel publisher lattice OK")


if __name__ == "__main__":
    main()
