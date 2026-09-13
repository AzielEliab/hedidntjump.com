#!/usr/bin/env python3
"""Validate AZindex identity lock, hub disambiguation, and /aziel aliases."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_ID = "https://www.azieleliab.com/#aziel"
NEEDLES = (
    "עזיאל",
    "אל ראי",
    "אלרועי",
    "אליאב",
    "Aziel Eliah",
    "The Revealer of The Sealed",
    "Revealer of The Sealed",
)
FAQ_NOT_NAME = "Who is Aziel Eliab not?"
FAQ_NAMES = {
    "Who is Aziel Eliab?",
    "What is He Didn’t Jump?",
    FAQ_NOT_NAME,
    "What does “The Record, Not the Verdict” mean?",
    "Is He Didn’t Jump a shrine or a theory blog?",
    "What is the official jump line versus the published record?",
    "What is ZionPattern Solver’s 75% hard cap?",
    "What does “I am temporary. The truth is not.” mean?",
}
BANNED_FAQ = {
    "Is Aziel Eliab the biblical Aziel?",
    "Is Aziel Eliab the biblical Eliab?",
    "Is Aziel Eliab the biblical Aziel and biblical Eliab combined?",
    "Is Aziel Eliab the same person as Aziel S.?",
    "Is Aziel Eliab a 1 Chronicles 15:20 / concordance namesake?",
}
DISAMBIGUATING = (
    "Living author of He Didn’t Jump / Zioncheck archive. "
    "Not biblical Aziel; not biblical Eliab; not euaziel.site; not Aziel S. (Flutter/portfolio); not other engineers named Aziel."
)
NOT_LIST = [
    "biblical Aziel",
    "biblical Eliab",
    "euaziel.site",
    "Aziel S. (Flutter/portfolio engineer)",
    "other engineers named Aziel",
]
VERSE_SNIPPET = "1 Chronicles 15:20"
COMBO_SNIPPET = "biblical Aziel and biblical Eliab combined"
NEVER_SAME_AS = ("euaziel", "aziel s", "flutter-react", "flutter", "react")
STATS = "https://www.hedidntjump.com/api/stats"


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def assert_no_forbidden_same_as(same_as) -> None:
    blob = json.dumps(same_as).lower()
    for banned in NEVER_SAME_AS:
        assert banned not in blob, banned


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
        assert person["name"] == "Aziel Eliab"
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
        assert names.isdisjoint(BANNED_FAQ), names & BANNED_FAQ
        not_qs = [n for n in names if n == FAQ_NOT_NAME or "not?" in n.lower()]
        assert not_qs == [FAQ_NOT_NAME], not_qs
        verse_qs = [n for n in names if VERSE_SNIPPET in n or "concordance" in n.lower()]
        assert verse_qs == [], verse_qs
        assert graph["stats"] == STATS
        assert well["stats"] == STATS
        assert load(f"{tree}/cite.json")["stats"] == STATS
        assert STATS in who
        assert person["disambiguatingDescription"] == DISAMBIGUATING
        assert len(person["disambiguatingDescription"]) < 180
        assert "biblical Aziel" in person["disambiguatingDescription"]
        assert "biblical Eliab" in person["disambiguatingDescription"]
        assert "euaziel.site" in person["disambiguatingDescription"]
        assert "Aziel S." in person["disambiguatingDescription"]
        assert "other engineers named Aziel" in person["disambiguatingDescription"]
        assert VERSE_SNIPPET not in person["disambiguatingDescription"]
        assert "concordance" not in person["disambiguatingDescription"]
        assert VERSE_SNIPPET not in person["description"]
        assert "concordance" not in person["description"]
        assert "Living stack:" in person["description"]
        assert "He Didn’t Jump" in person["description"] or "He Didn't Jump" in person["description"]
        assert "Zioncheck" in person["description"]
        assert who.count("Disambiguation (single field):") == 1
        assert who.count(VERSE_SNIPPET) == 0
        assert COMBO_SNIPPET not in who
        assert "David’s brother" not in who
        assert "The Record, Not the Verdict" in person["description"]
        assert "75%" in person["description"]
        assert DISAMBIGUATING in llms
        assert DISAMBIGUATING in llms_full
        assert DISAMBIGUATING in ai
        assert COMBO_SNIPPET not in llms
        assert "Living stack:" in llms
        about = next(n for n in graph["@graph"] if n.get("@type") == "AboutPage")
        assert about["url"].rstrip("/").endswith("/aziel")
        assert "person.jsonld" in "".join(about["significantLink"])
        assert well["aboutPage"].endswith("/aziel")
        assert well["motto"] == "The Record, Not the Verdict."
        assert "I am temporary" in who
        assert "living author" in who.lower()
        assert person["givenName"] == "Aziel"
        assert person["familyName"] == "Eliab"
        assert_no_forbidden_same_as(person["sameAs"])
        assert_no_forbidden_same_as(well["sameAs"])
        cite = load(f"{tree}/cite.json")
        assert cite["living_author"] is True
        assert cite["person_id"] == PERSON_ID
        assert cite["disambiguation"] == DISAMBIGUATING
        assert VERSE_SNIPPET not in cite.get("identity_note", "")
        assert VERSE_SNIPPET not in json.dumps(cite)
        assert cite["about_page"] == "https://hedidntjump.com/aziel"
        assert cite["not"] == NOT_LIST
        assert "euaziel.site" in cite["disambiguation"]
        assert "Aziel S." in cite["disambiguation"]
        assert "other engineers named Aziel" in cite["disambiguation"]
        cite_faq_names = [item["q"] for item in cite["faq"]]
        assert FAQ_NOT_NAME in cite_faq_names
        assert cite_faq_names.count(FAQ_NOT_NAME) == 1
        assert "Is Aziel Eliab the same person as Aziel S.?" not in cite_faq_names
        assert well.get("not") == NOT_LIST
        assert well.get("disambiguatingDescription") == DISAMBIGUATING

        sitemap = (ROOT / tree / "sitemap.xml").read_text(encoding="utf-8")
        headers = (ROOT / tree / "_headers").read_text(encoding="utf-8")
        redirects = (ROOT / tree / "_redirects").read_text(encoding="utf-8")
        for path in (
            "person.jsonld",
            "identity.jsonld",
            "graph.jsonld",
            "who-is-aziel-eliab.txt",
            "/who-is",
            ".well-known/aziel.json",
            "/aziel",
            "/AzielEliab",
            "/AboutAziel",
        ):
            assert path in sitemap, path
        assert "/inquiry/" not in sitemap
        assert "hedidntjump.com/who-is</loc>" in sitemap
        assert "/who-is /who-is-aziel-eliab.txt 200" in redirects
        assert "ZionBot owns newspaper HTML" in redirects
        assert "/who-is\n  Content-Type: text/plain" in headers
        assert (ROOT / tree / "who-is").is_file()
        assert (ROOT / tree / "who-is").read_text(encoding="utf-8") == who
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
        assert "hedidntjump.com/aziel" in aziel
        assert PERSON_ID in aziel
        assert "#aziel-eliab" not in aziel
        assert DISAMBIGUATING in aziel
        assert COMBO_SNIPPET not in aziel
        meta = re.search(r'<meta name="description" content="([^"]*)"', aziel)
        assert meta, "aziel.html missing meta description"
        assert VERSE_SNIPPET not in meta.group(1)
        assert "concordance" not in meta.group(1)
        assert "He Didn’t Jump" in meta.group(1) or "He Didn't Jump" in meta.group(1)
        assert "software developer" in meta.group(1)
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
