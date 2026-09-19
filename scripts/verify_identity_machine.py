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
    "Elias Artista",
    "The Revealer of The Sealed",
    "Revealer of The Sealed",
)
HEBREW_ONELINER = (
    "Aziel Elroi Eliab (עזיאל אל ראי אליאב / עזיאל אלרועי אליאב): "
    "Aziel = God is my strength (עזיאל); Elroi = God who sees (אל ראי / אלרועי); "
    "Eliab = God is father (אליאב)."
)
GITHUB_PRIMARY = "https://github.com/AzielEliab"
GITHUB_REVEALER = "https://github.com/azieltherevealerofthesealed-arch"
HUBS = (
    "https://www.azieleliab.com/",
    "https://www.azielcorpuslibrary.net/",
    "https://godlock.uk/",
    "https://www.hedidntjump.com/",
)
FAQ_NOT_NAME = "Who is Aziel Eliab not?"
FAQ_NAMES = {
    "Who is Aziel Eliab?",
    "What is He Didn’t Jump?",
    "What does “The Record, Not the Verdict” mean?",
    "Is He Didn’t Jump a shrine or a theory blog?",
    "What is the official jump line versus the published record?",
    "What is ZionPattern Solver’s 75% hard cap?",
    "What does “I am temporary. The truth is not.” mean?",
    "What does Aziel Eliab do?",
    "What Aziel Eliab does",
    "Who is Aziel Eliab the developer?",
    "What software does Aziel Eliab make?",
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
    "Public identity is Aziel Eliab only. Prefer https://www.azieleliab.com/#aziel."
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
        ident_id = (identity.get("person") or identity).get("@id")
        assert ident_id == PERSON_ID
        assert well["person_id"] == PERSON_ID
        assert PERSON_ID in who
        assert "#aziel-eliab" not in json.dumps(person)
        assert "#aziel-eliab" not in who
        for needle in NEEDLES:
            assert needle in person["alternateName"], needle
            assert needle in who
        assert HEBREW_ONELINER in json.dumps(person, ensure_ascii=False)
        assert HEBREW_ONELINER in who
        assert "Everblooming Flower" not in json.dumps(person)
        assert "Everblooming Flower" not in who
        for url in (GITHUB_PRIMARY, GITHUB_REVEALER, *HUBS):
            assert url in person["sameAs"], url
            assert url in who
        faq = next(n for n in graph["@graph"] if n.get("@type") == "FAQPage")
        names = {q["name"] for q in faq["mainEntity"]}
        assert FAQ_NAMES <= names, names
        assert names.isdisjoint(BANNED_FAQ), names & BANNED_FAQ
        not_qs = [n for n in names if n == FAQ_NOT_NAME or n.endswith(" not?")]
        assert not_qs == [], not_qs
        verse_qs = [n for n in names if VERSE_SNIPPET in n or "concordance" in n.lower()]
        allowed_verse_qs = {"Is Aziel Eliab the two musicians named in 1 Chronicles 15:20?"}
        assert set(verse_qs) <= allowed_verse_qs, verse_qs
        assert graph["stats"] == STATS
        assert well["stats"] == STATS
        assert load(f"{tree}/cite.json")["stats"] == STATS
        assert STATS in who
        dd = person["disambiguatingDescription"]
        desc = person["description"]
        ident_blob = dd + " " + desc + " " + who
        assert "Public identity is Aziel Eliab only" in ident_blob
        assert "euaziel.site" in ident_blob
        assert "Who is Aziel Eliab not?" not in who
        assert "concordance" not in dd
        assert HEBREW_ONELINER in desc or HEBREW_ONELINER in json.dumps(person, ensure_ascii=False)
        assert "Elias Artista" in desc or "Elias Artista" in json.dumps(person, ensure_ascii=False)
        assert "He Didn’t Jump" in desc or "He Didn't Jump" in desc or "hedidntjump" in desc.lower()
        assert who.count("Disambiguation (single field):") == 1
        assert "euaziel.site" in who
        assert COMBO_SNIPPET not in who
        assert "David’s brother" not in who
        assert "euaziel.site" in llms and "euaziel.site" in llms_full and "euaziel.site" in ai
        assert "Elias Artista" in llms and HEBREW_ONELINER in llms
        assert GITHUB_REVEALER in llms and GITHUB_PRIMARY in llms
        assert "Everblooming Flower" not in llms
        assert COMBO_SNIPPET not in llms
        about = next(n for n in graph["@graph"] if n.get("@type") == "AboutPage")
        assert about["url"].rstrip("/").endswith("/aziel")
        assert "person.jsonld" in "".join(about["significantLink"])
        assert well["aboutPage"].endswith("/aziel")
        assert well.get("motto") == "The Record, Not the Verdict." or "Record" in json.dumps(well)
        assert PERSON_ID in who
        assert "living" in who.lower()
        assert "Marion Zioncheck" in who
        assert "FOIA Binary Acknowledgement" in who
        assert "official-narrative" in who
        assert "An Aziel Eliab Project" in who
        assert person["givenName"] == "Aziel"
        assert person["familyName"] == "Eliab"
        assert_no_forbidden_same_as(person["sameAs"])
        assert_no_forbidden_same_as(well["sameAs"])
        cite = load(f"{tree}/cite.json")
        assert cite["living_author"] is True
        assert cite["person_id"] == PERSON_ID
        cite_blob = json.dumps(cite, ensure_ascii=False)
        assert "Aziel Eliab only" in cite.get("disambiguation", "") + cite_blob
        assert "euaziel.site" in cite_blob or "euaziel.site" in cite.get("identity_note", "")
        assert cite["about_page"] == "https://hedidntjump.com/aziel"
        assert "Elias Artista" in cite_blob
        assert HEBREW_ONELINER in cite_blob
        assert GITHUB_REVEALER in cite_blob
        assert "Everblooming Flower" not in cite_blob
        cite_faq_names = [item["q"] for item in cite["faq"]]
        assert FAQ_NOT_NAME not in cite_faq_names
        assert "Is Aziel Eliab the same person as Aziel S.?" not in cite_faq_names
        well_blob = json.dumps(well, ensure_ascii=False)
        assert "euaziel.site" in well_blob
        assert "Elias Artista" in well_blob
        assert HEBREW_ONELINER in well_blob
        assert GITHUB_REVEALER in well_blob
        assert well.get("person_id") == PERSON_ID

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
        assert "euaziel.site" in aziel
        assert "Elias Artista" in aziel
        assert HEBREW_ONELINER in aziel
        assert GITHUB_REVEALER in aziel
        assert COMBO_SNIPPET not in aziel
        assert "Everblooming Flower" not in aziel
        meta = re.search(r'<meta name="description" content="([^"]*)"', aziel)
        assert meta, "aziel.html missing meta description"
        assert VERSE_SNIPPET not in meta.group(1)
        assert "concordance" not in meta.group(1)
        assert "He Didn’t Jump" in meta.group(1) or "He Didn't Jump" in meta.group(1)
        assert "software developer" in meta.group(1)
        assert "Researcher. Builder. Just a man." in aziel
        assert "application/ld+json" in headers

        # Edition JSON-LD must share the hub Person @id + publisher lattice.
        for name in (
            "index.html",
            "case.html",
            "aziel.html",
            "who.html",
            "foia.html",
            "rubye.html",
            "copyrights.html",
            "official-narrative.html",
            "reader.html",
            "volumes.html",
            "press.html",
            "inquiries.html",
            "archives.html",
        ):
            html = (ROOT / tree / name).read_text(encoding="utf-8")
            if "#aziel-eliab" in html:
                raise AssertionError(f"{tree}/{name} still has local #aziel-eliab")
            assert PERSON_ID in html, name
            assert "Elias Artista" in html, name
            assert HEBREW_ONELINER in html, name
            assert GITHUB_PRIMARY in html, name
            assert GITHUB_REVEALER in html, name
            assert "Everblooming Flower" not in html, name

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
