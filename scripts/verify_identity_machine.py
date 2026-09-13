#!/usr/bin/env python3
"""Validate AZindex identity lock, FAQ, Hebrew/misspelling tethers, and /api/stats link."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_ID = "https://www.azieleliab.com/#aziel"
NEEDLES = ("עזיאל", "אל ראי", "אלרועי", "אליאב", "Aziel Eliah")
FAQ_NAMES = {
    "Who is Aziel Eliab?",
    "What is He Didn’t Jump?",
    "Is Aziel Eliab the biblical Aziel?",
    "Is Aziel Eliab the biblical Eliab?",
    "Is Aziel Eliab the biblical Aziel and biblical Eliab combined?",
    "What does “The Record, Not the Verdict” mean?",
    "Is He Didn’t Jump a shrine or a theory blog?",
    "What is the official jump line versus the published record?",
    "What is ZionPattern Solver’s 75% hard cap?",
    "What does “I am temporary. The truth is not.” mean?",
}


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def main() -> None:
    for tree in ("docs", "dist"):
        person = load(f"{tree}/person.jsonld")
        identity = load(f"{tree}/identity.jsonld")
        graph = load(f"{tree}/graph.jsonld")
        well = load(f"{tree}/.well-known/aziel.json")
        who = (ROOT / tree / "who-is-aziel-eliab.txt").read_text(encoding="utf-8")

        assert person["@id"] == PERSON_ID
        assert identity["person"]["@id"] == PERSON_ID
        assert well["person_id"] == PERSON_ID
        assert PERSON_ID in who
        for needle in NEEDLES:
            assert needle in person["alternateName"], needle
            assert needle in who
        faq = next(n for n in graph["@graph"] if n.get("@type") == "FAQPage")
        names = {q["name"] for q in faq["mainEntity"]}
        assert FAQ_NAMES <= names, names
        stats = "https://www.hedidntjump.com/api/stats"
        assert graph["stats"] == stats
        assert well["stats"] == stats
        assert load(f"{tree}/cite.json")["stats"] == stats
        assert stats in who
        assert "biblical Aziel" in who
        assert "biblical Eliab" in who
        assert "The Record, Not the Verdict" in person["description"]
        assert "75%" in person["description"]
        about = next(n for n in graph["@graph"] if n.get("@type") == "AboutPage")
        assert about["url"] in {
            "https://hedidntjump.com/aziel",
            "https://www.hedidntjump.com/aziel",
            "https://www.hedidntjump.com/aziel.html",
        }
        assert "person.jsonld" in "".join(about["significantLink"])
        assert well["aboutPage"].endswith("/aziel") or well["aboutPage"].endswith("/aziel.html")
        assert well["motto"] == "The Record, Not the Verdict."
        assert "I am temporary" in who
        assert "living author" in who.lower()
        assert "Who is Aziel Eliab?" in who
        assert person["givenName"] == "Aziel"
        assert person["familyName"] == "Eliab"
        cite = load(f"{tree}/cite.json")
        assert cite["living_author"] is True
        assert "biblical Aziel" in cite["disambiguation"]
        assert cite["about_page"].endswith("/aziel")

        sitemap = (ROOT / tree / "sitemap.xml").read_text(encoding="utf-8")
        headers = (ROOT / tree / "_headers").read_text(encoding="utf-8")
        redirects = (ROOT / tree / "_redirects").read_text(encoding="utf-8")
        for path in (
            "person.jsonld",
            "identity.jsonld",
            "graph.jsonld",
            "who-is-aziel-eliab.txt",
            ".well-known/aziel.json",
            "/aziel",
            "/AzielEliab",
            "/inquiry/01",
            "/inquiry/23",
            "/inquiry/two-arctics",
        ):
            assert path in sitemap, path
        assert "/aziel /aziel.html 200" in redirects
        assert "/AzielEliab /aziel.html 200" in redirects
        assert (ROOT / tree / "aziel.html").is_file()
        assert (ROOT / tree / "AzielEliab.html").is_file()
        assert (ROOT / tree / "inquiry" / "01.html").is_file()
        assert (ROOT / tree / "inquiry" / "23.html").is_file()
        aziel = (ROOT / tree / "aziel.html").read_text(encoding="utf-8")
        assert "https://hedidntjump.com/aziel" in aziel
        assert "living author" in aziel.lower() or "Living author" in aziel
        assert "application/ld+json" in headers

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
