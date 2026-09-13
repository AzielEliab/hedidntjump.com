#!/usr/bin/env python3
"""Validate AZindex identity lock, FAQ, Hebrew/misspelling tethers, and /api/stats meter."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_ID = "https://www.azieleliab.com/#aziel"
NEEDLES = ("עזיאל", "אל ראי", "אלרועי", "אליאב", "Aziel Eliah")
FAQ_NAMES = {
    "Who is Aziel Eliab?",
    "What is He Didn’t Jump?",
    "Is Aziel Eliab the biblical Aziel?",
    "Is Aziel Eliab the biblical Eliab?",
}


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def main() -> None:
    for tree in ("docs", "dist"):
        person = load(f"{tree}/person.jsonld")
        identity = load(f"{tree}/identity.jsonld")
        graph = load(f"{tree}/graph.jsonld")
        well = load(f"{tree}/.well-known/aziel.json")
        cite = load(f"{tree}/cite.json")
        who = (ROOT / tree / "who-is-aziel-eliab.txt").read_text(encoding="utf-8")

        assert person["@id"] == PERSON_ID
        assert identity["person"]["@id"] == PERSON_ID
        assert well["person_id"] == PERSON_ID
        assert cite["person_id"] == PERSON_ID
        assert PERSON_ID in who
        for needle in NEEDLES:
            assert needle in person["alternateName"], needle
            assert needle in who
        faq = next(n for n in graph["@graph"] if n.get("@type") == "FAQPage")
        names = {q["name"] for q in faq["mainEntity"]}
        assert FAQ_NAMES <= names, names
        assert cite["stats"]["local"]["stats"].endswith("/api/stats")
        assert graph["stats"]["local"]["stats"].endswith("/api/stats")
        assert well["stats"]["local"]["stats"].endswith("/api/stats")
        sisters = {h["id"] for h in cite["stats"]["sister_hubs"]}
        assert sisters == {"official", "godlock", "library", "runtime"}
        assert "biblical Aziel" in who
        assert "biblical Eliab" in who

        for name in ("index.html", "official-narrative.html"):
            html = (ROOT / tree / name).read_text(encoding="utf-8")
            assert PERSON_ID in html
            assert 'id="azindex-faq"' in html
            for block in re.findall(
                r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S
            ):
                json.loads(block)
            assert "#aziel-eliab" not in html

        robots = (ROOT / tree / "robots.txt").read_text(encoding="utf-8")
        for path in (
            "/person.jsonld",
            "/identity.jsonld",
            "/graph.jsonld",
            "/who-is-aziel-eliab.txt",
            "/.well-known/aziel.json",
        ):
            assert f"Allow: {path}" in robots
        sitemap = (ROOT / tree / "sitemap.xml").read_text(encoding="utf-8")
        assert "person.jsonld" in sitemap
        assert "official-narrative.html" in sitemap
        headers = (ROOT / tree / "_headers").read_text(encoding="utf-8")
        assert "application/ld+json" in headers

    # Meter files must stay untouched by this identity ship.
    for rel in (
        "docs/stats.js",
        "dist/stats.js",
        "functions/api/stats.js",
        "functions/api/hit.js",
        "workers/hedidntjump-stats/src/index.js",
    ):
        assert (ROOT / rel).is_file()

    print("identity machine OK")


if __name__ == "__main__":
    main()
