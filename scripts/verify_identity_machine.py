#!/usr/bin/env python3
"""Validate AZindex identity lock, hub disambiguation, and /aziel aliases."""
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
    "Is Aziel Eliab the same person as Aziel S.?",
    "What does “The Record, Not the Verdict” mean?",
    "Is He Didn’t Jump a shrine or a theory blog?",
    "What is the official jump line versus the published record?",
    "What is ZionPattern Solver’s 75% hard cap?",
    "What does “I am temporary. The truth is not.” mean?",
}
DISAMBIGUATING = (
    "Living author of He Didn’t Jump / Zioncheck archive; not a biblical namesake and not Aziel S. (Flutter)."
)
HUB_NEEDLES = (
    "not a biblical namesake",
    "Aziel S.",
    "Flutter",
)
VERSE_SNIPPET = "1 Chronicles 15:20"
COMBO_SNIPPET = "biblical Aziel and biblical Eliab combined"


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def main() -> None:
    for tree in ("docs", "dist"):
        person = load(f"{tree}/person.jsonld")
        identity = load(f"{tree}/identity.jsonld")
        graph = load(f"{tree}/graph.jsonld")
        well = load(f"{tree}/.well-known/aziel.json")
        who = (ROOT / tree / "who-is-aziel-eliab.txt").read_text(encoding="utf-8")
        llms = (ROOT / tree / "llms.txt").read_text(encoding="utf-8")
        llms_full = (ROOT / tree / "llms-full.txt").read_text(encoding="utf-8")
        ai = (ROOT / tree / "ai.txt").read_text(encoding="utf-8")

        assert person["@id"] == PERSON_ID
        assert identity["person"]["@id"] == PERSON_ID
        assert well["person_id"] == PERSON_ID
        assert PERSON_ID in who
        assert "#aziel-eliab" not in json.dumps(person)
        assert "#aziel-eliab" not in who
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
        assert person["disambiguatingDescription"] == DISAMBIGUATING
        assert len(person["disambiguatingDescription"]) < 180
        for needle in HUB_NEEDLES:
            assert needle in who, needle
            assert needle in person["disambiguatingDescription"], needle
        assert who.count("Disambiguation (single field):") == 1
        assert VERSE_SNIPPET not in person["description"]
        assert VERSE_SNIPPET not in who
        assert COMBO_SNIPPET not in who
        assert "David’s brother" not in who
        assert "The Record, Not the Verdict" in person["description"]
        assert "75%" in person["description"]
        assert DISAMBIGUATING in llms
        assert VERSE_SNIPPET not in llms
        assert COMBO_SNIPPET not in llms
        assert DISAMBIGUATING in llms_full
        assert VERSE_SNIPPET not in llms_full
        assert DISAMBIGUATING in ai
        assert VERSE_SNIPPET not in ai
        about = next(n for n in graph["@graph"] if n.get("@type") == "AboutPage")
        assert about["url"].rstrip("/").endswith("/aziel")
        assert "person.jsonld" in "".join(about["significantLink"])
        assert well["aboutPage"].endswith("/aziel")
        assert well["motto"] == "The Record, Not the Verdict."
        assert "I am temporary" in who
        assert "living author" in who.lower()
        assert person["givenName"] == "Aziel"
        assert person["familyName"] == "Eliab"
        cite = load(f"{tree}/cite.json")
        assert cite["living_author"] is True
        assert cite["person_id"] == PERSON_ID
        assert cite["disambiguation"] == DISAMBIGUATING
        assert VERSE_SNIPPET not in cite["disambiguation"]
        assert VERSE_SNIPPET not in cite.get("identity_note", "")
        assert "Aziel S." in cite["disambiguation"]
        assert cite["about_page"] == "https://hedidntjump.com/aziel"

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
            "/AboutAziel",
        ):
            assert path in sitemap, path
        assert "/inquiry/" not in sitemap
        assert "/aziel /aziel.html 200" not in redirects
        assert "Do not add /aziel" in redirects
        assert "/Aziel /aziel.html 200" in redirects
        assert "/AboutAziel /aziel.html 200" in redirects
        assert "/AzielEliab /aziel.html 200" in redirects
        assert "/reader /reader.html 200" not in redirects
        assert "/Volumes/read /reader.html" not in redirects
        assert "/Volumes/read /volumes" not in redirects
        assert (ROOT / tree / "aziel.html").is_file()
        assert not (ROOT / tree / "AzielEliab.html").exists()
        assert not (ROOT / tree / "inquiry").exists()
        aziel = (ROOT / tree / "aziel.html").read_text(encoding="utf-8")
        assert "https://hedidntjump.com/aziel" in aziel
        assert PERSON_ID in aziel
        assert "#aziel-eliab" not in aziel
        assert DISAMBIGUATING in aziel
        assert "Aziel S." in aziel
        assert VERSE_SNIPPET not in aziel
        assert COMBO_SNIPPET not in aziel
        assert "Researcher. Builder. Just a man." in aziel
        assert "application/ld+json" in headers

        # Edition JSON-LD must share the hub Person @id.
        for name in (
            "index.html",
            "foia.html",
            "rubye.html",
            "copyrights.html",
            "official-narrative.html",
            "reader.html",
            "volumes.html",
        ):
            html = (ROOT / tree / name).read_text(encoding="utf-8")
            if "#aziel-eliab" in html:
                raise AssertionError(f"{tree}/{name} still has local #aziel-eliab")

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
