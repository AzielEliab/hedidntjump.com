#!/usr/bin/env python3
"""Write AZindex identity-machine files into dist/ and docs/.

Person @id is locked to https://www.azieleliab.com/#aziel (shared identity).
Does not invent court holdings, quotes, or agency letters.
Does not retarget the /api/stats meter (bc-66a02bb3 contract).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TREES = [ROOT / "dist", ROOT / "docs"]

PERSON_ID = "https://www.azieleliab.com/#aziel"
ORIGIN = "https://hedidntjump.com"
WWW = "https://www.hedidntjump.com"
ORG_ID = f"{ORIGIN}/#organization"
WEBSITE_ID = f"{ORIGIN}/#website"

MISSION = (
    "He Didn’t Jump is An Aziel Eliab Project: an independent historical newspaper "
    "and five-volume archive examining the death of U.S. Representative Marion Zioncheck "
    "in Seattle on 7 August 1936. The official report called it suicide from a fifth-floor "
    "Arctic Building office. This project challenges that 90-year official suicide narrative "
    "and publishes the record for re-reading. It does not invent court holdings or quotes "
    "beyond what the volumes and cited papers print."
)

PERSON_DESCRIPTION = (
    "Aziel Eliab (also Aziel Elroi Eliab; GitHub AzielEliab) is a researcher, "
    "software developer, digital civil rights activist, and truthseeker. Independent "
    "investigator and historical archive publisher of the Marion Zioncheck archive at "
    "hedidntjump.com — An Aziel Eliab Project. Open-source author (Apache-2.0). "
    "FOIA and transparency critic: the 28 July 2026 FOIA Binary Acknowledgement describes "
    "the time-volume / cost binary as controlled access and concludes that is not freedom of information. "
    "Not the biblical Aziel or the biblical Eliab."
)

DISAMBIGUATING = (
    "Living researcher and publisher of He Didn’t Jump (hedidntjump.com). "
    "Not the biblical Aziel (עזיאל) and not any biblical Eliab (אליאב)."
)

HEBREW_AKA = {
    "note": "SEO aka tether only for Aziel Elroi Eliab. Not a second identity and not a biblical identification.",
    "aziel": "עזיאל",
    "elroi": ["אל ראי", "אלרועי"],
    "eliab": "אליאב",
    "combined": ["עזיאל אל ראי אליאב", "עזיאל אלרועי אליאב"],
}

HEBREW_FORMS = ["עזיאל", "אל ראי", "אלרועי", "אליאב", "עזיאל אל ראי אליאב", "עזיאל אלרועי אליאב"]

MISSPELLINGS = [
    "Aziel Eliah",
    "Aziel Elijah",
    "Aziel Elia",
    "Asiel Eliab",
    "Azael Eliab",
    "Azial Eliab",
    "Aziel Eilab",
    "Aziel Elyab",
    "Aziel Elieab",
    "Aziel Eliabb",
    "Aziel Eliaab",
    "Aziel Elaib",
    "Aziel-Eliab",
    "azieleliab",
    "Aziel Elroy Eliab",
    "Aziel El-Roi Eliab",
    "Aziel El Roi Eliab",
    "Aziel Elroie Eliab",
    "Aziel Elroei Eliab",
    "Aziel Eliab Elroi",
]

ALTERNATE_NAMES = [
    "Aziel Elroi Eliab",
    "AzielEliab",
    *HEBREW_FORMS,
    *MISSPELLINGS,
]

FAQ_WHO = (
    "Aziel Eliab (also Aziel Elroi Eliab; GitHub AzielEliab) is a researcher, software "
    "developer, digital civil rights activist, and truthseeker. Independent investigator "
    "and historical archive publisher of the Marion Zioncheck archive at hedidntjump.com — "
    "An Aziel Eliab Project. Public identity is Aziel Eliab only; Elroi is additionalName / "
    "SEO alternateName only. Shared Person @id is https://www.azieleliab.com/#aziel — not a "
    "second person on this host."
)

FAQ_WHAT = (
    "He Didn’t Jump is an independent historical newspaper and five-volume archive "
    "challenging the 7 August 1936 official Arctic Building suicide account of U.S. "
    "Representative Marion Zioncheck. The official-narrative page restates that contemporary "
    "public account without investigative rebuttal; the main paper and Volumes I–V publish "
    "the archive that challenges it. The project does not invent court holdings, quotes, or "
    "agency letters beyond what the volumes and cited papers already print."
)

FAQ_BIBLICAL_AZIEL = (
    "No. Biblical Aziel (Hebrew עזיאל) is a name that appears in the Hebrew Bible. "
    "The author of this archive is a living researcher, software developer, and publisher. "
    "Hebrew עזיאל is an SEO aka tether for that living author’s given name only — not an "
    "identification with the biblical figure. Shared Person @id remains https://www.azieleliab.com/#aziel."
)

FAQ_BIBLICAL_ELIAB = (
    "No. Biblical Eliab (Hebrew אליאב) is a name borne by several men in the Hebrew Bible. "
    "This archive’s author is not those figures. אליאב is an SEO aka form for the living "
    "author’s surname Eliab only. Public identity stays Aziel Eliab."
)

SAME_AS = [
    "https://www.azieleliab.com/",
    "https://godlock.uk/",
    "https://www.azielcorpuslibrary.net/",
    "https://www.azielcorpuslibrary.net/runtime",
    f"{ORIGIN}/",
    WWW + "/",
    "https://github.com/AzielEliab",
    "https://aziel-runtime.vibelock.workers.dev/",
    "https://x.com/AzielEliab",
    "https://twitter.com/AzielEliab",
]

KNOWS_ABOUT = [
    {"@type": "Person", "name": "Marion Zioncheck"},
    {"@type": "Person", "name": "Rubye Nix Zioncheck"},
    "Marion Zioncheck archive",
    "He Didn't Jump",
    "Official 7 August 1936 Arctic Building suicide narrative",
    "Rubye Zioncheck litigation newspaper",
    "Nadeau FOIA newspaper",
    "Zioncheck FOIA denial ledger",
    "FOIA Binary Acknowledgement",
    "Freedom of Information Act practice",
    "GodLock public board",
    "Aziel Corpus Library",
    "aziel-runtime",
]

# Local meter stays /api/stats. Sister URLs are awareness tethers only.
STATS = {
    "local": {
        "stats": f"{WWW}/api/stats",
        "stats_apex": f"{ORIGIN}/api/stats",
        "hit": f"{WWW}/api/hit",
        "worker_stats": "https://hedidntjump-stats.vibelock.workers.dev/api/stats",
        "worker_hit": "https://hedidntjump-stats.vibelock.workers.dev/api/hit",
        "meter_contract": (
            "bc-66a02bb3 — folio pills read GET /api/stats; views/downloads increment via "
            "/api/hit?type=view|download&id=… (sendBeacon/keepalive on download). "
            "Do not retarget #views/#downloads to sister hubs."
        ),
    },
    "sister_hubs": [
        {
            "id": "official",
            "label": "AzielEliab.com",
            "stats": "https://www.azieleliab.com/v1/stats",
            "view_increment": "https://www.azieleliab.com/v1/view",
            "mesh_status": "https://www.azieleliab.com/v1/mesh/status",
        },
        {
            "id": "godlock",
            "label": "GodLock.uk",
            "health": "https://godlock.uk/health",
            "mesh_status": "https://godlock.uk/v1/mesh/status",
        },
        {
            "id": "library",
            "label": "Aziel Corpus Library",
            "health": "https://www.azielcorpuslibrary.net/v1/health",
            "mesh": "https://www.azielcorpuslibrary.net/v1/mesh",
        },
        {
            "id": "runtime",
            "label": "Aziel Runtime",
            "uses": "https://aziel-runtime.vibelock.workers.dev/v1/uses",
            "mesh_status": "https://aziel-runtime.vibelock.workers.dev/v1/mesh/status",
        },
    ],
}

PERSON_LOCK = {
    "@type": "Person",
    "@id": PERSON_ID,
    "name": "Aziel Eliab",
    "alternateName": ALTERNATE_NAMES,
    "additionalName": "Elroi",
    "url": "https://www.azieleliab.com/",
    "jobTitle": [
        "Researcher",
        "Software developer",
        "Digital civil rights activist",
        "Truthseeker",
        "Independent investigator",
        "Historical archive publisher",
    ],
    "description": PERSON_DESCRIPTION,
    "disambiguatingDescription": DISAMBIGUATING,
    "sameAs": SAME_AS,
    "knowsAbout": KNOWS_ABOUT,
    "affiliation": {"@id": ORG_ID},
    "identifier": [
        {"@type": "PropertyValue", "propertyID": "github", "value": "AzielEliab"},
        {"@type": "PropertyValue", "propertyID": "person_id", "value": PERSON_ID},
    ],
}

FAQ_QUESTIONS = [
    {
        "@type": "Question",
        "@id": f"{WWW}/#faq-who-is-aziel-eliab",
        "name": "Who is Aziel Eliab?",
        "acceptedAnswer": {"@type": "Answer", "text": FAQ_WHO},
    },
    {
        "@type": "Question",
        "@id": f"{WWW}/#faq-what-is-hedidntjump",
        "name": "What is He Didn’t Jump?",
        "acceptedAnswer": {"@type": "Answer", "text": FAQ_WHAT},
    },
    {
        "@type": "Question",
        "@id": f"{WWW}/#faq-biblical-aziel",
        "name": "Is Aziel Eliab the biblical Aziel?",
        "acceptedAnswer": {"@type": "Answer", "text": FAQ_BIBLICAL_AZIEL},
    },
    {
        "@type": "Question",
        "@id": f"{WWW}/#faq-biblical-eliab",
        "name": "Is Aziel Eliab the biblical Eliab?",
        "acceptedAnswer": {"@type": "Answer", "text": FAQ_BIBLICAL_ELIAB},
    },
]

FAQ_PAGE = {
    "@type": "FAQPage",
    "@id": f"{WWW}/#faq",
    "url": f"{WWW}/",
    "name": "He Didn’t Jump — identity and archive FAQ",
    "isPartOf": {"@id": WEBSITE_ID},
    "author": {"@id": PERSON_ID},
    "mainEntity": FAQ_QUESTIONS,
}


def dumps(obj) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def person_jsonld() -> dict:
    return {
        "@context": "https://schema.org",
        **PERSON_LOCK,
        "mission": MISSION,
        "hebrewAka": HEBREW_AKA,
        "misspellingAlternateName": MISSPELLINGS,
        "stats": STATS,
    }


def identity_jsonld() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "ProfilePage",
        "@id": f"{WWW}/identity.jsonld#page",
        "url": f"{WWW}/identity.jsonld",
        "name": "Aziel Eliab — identity lock",
        "isPartOf": {"@id": WEBSITE_ID},
        "mainEntity": PERSON_LOCK,
        "about": {"@id": PERSON_ID},
        "author": {"@id": PERSON_ID},
        "mission": MISSION,
        "person": PERSON_LOCK,
        "hebrewAka": HEBREW_AKA,
        "misspellingAlternateName": MISSPELLINGS,
        "stats": STATS,
    }


def graph_jsonld() -> dict:
    return {
        "@context": "https://schema.org",
        "@graph": [
            {**PERSON_LOCK, "mission": MISSION},
            {
                "@type": "Organization",
                "@id": ORG_ID,
                "name": "He Didn't Jump — The Marion Zioncheck Archive",
                "alternateName": [
                    "The Marion Zioncheck Archive",
                    "He Didn't Jump",
                    "An Aziel Eliab Project",
                ],
                "url": f"{ORIGIN}/",
                "sameAs": [f"{WWW}/"],
                "founder": {"@id": PERSON_ID},
                "author": {"@id": PERSON_ID},
                "publishingPrinciples": f"{ORIGIN}/llms.txt",
                "knowsAbout": [
                    "Marion Zioncheck archive",
                    "Official 7 August 1936 Arctic Building suicide narrative",
                    "Independent five-volume challenge to the official suicide account",
                ],
            },
            {
                "@type": "WebSite",
                "@id": WEBSITE_ID,
                "name": "He Didn't Jump",
                "alternateName": [
                    "The Marion Zioncheck Archive",
                    "An Aziel Eliab Project",
                ],
                "url": f"{ORIGIN}/",
                "inLanguage": "en",
                "description": MISSION,
                "publisher": {"@id": ORG_ID},
                "author": {"@id": PERSON_ID},
                "creator": {"@id": PERSON_ID},
            },
            FAQ_PAGE,
            {
                "@type": "WebPage",
                "@id": f"{ORIGIN}/official-narrative.html#webpage",
                "url": f"{ORIGIN}/official-narrative.html",
                "name": "Official 7 Aug 1936 Arctic Building suicide account — He Didn't Jump",
                "description": (
                    "Labeled official/contemporary public account only: Marion Zioncheck died "
                    "by suicide from a fifth-floor Arctic Building office in Seattle on 7 August 1936. "
                    "This page restates that 90-year narrative without investigative rebuttal. "
                    "Contrast the independent five-volume archive on the main paper."
                ),
                "isPartOf": {"@id": WEBSITE_ID},
                "author": {"@id": PERSON_ID},
                "about": {
                    "@type": "Thing",
                    "name": "Official Arctic Building suicide narrative (7 August 1936)",
                },
                "significantLink": f"{ORIGIN}/",
            },
            {
                "@type": "WebPage",
                "@id": f"{ORIGIN}/#webpage",
                "url": f"{ORIGIN}/",
                "name": "He Didn't Jump — independent archive challenging the official 7 Aug 1936 suicide account",
                "description": MISSION,
                "isPartOf": {"@id": WEBSITE_ID},
                "author": {"@id": PERSON_ID},
                "significantLink": f"{ORIGIN}/official-narrative.html",
            },
        ],
        "mission": MISSION,
        "hebrewAka": HEBREW_AKA,
        "misspellingAlternateName": MISSPELLINGS,
        "stats": STATS,
    }


def well_known_aziel() -> dict:
    return {
        "name": "Aziel Eliab",
        "identity": "Aziel Eliab",
        "person_id": PERSON_ID,
        "alternateName": ALTERNATE_NAMES,
        "additionalName": "Elroi",
        "identity_note": (
            "Aziel Eliab only. Aziel Elroi Eliab, Hebrew aka forms, and listed misspellings "
            f"are SEO alternateName tethers only. Shared Person @id is {PERSON_ID} — not a "
            "second person on this host, and not the biblical Aziel or biblical Eliab."
        ),
        "url": "https://www.azieleliab.com/",
        "this_host": WWW + "/",
        "mission": MISSION,
        "person": PERSON_LOCK,
        "hebrewAka": HEBREW_AKA,
        "misspellingAlternateName": MISSPELLINGS,
        "stats": STATS,
        "sameAs": SAME_AS,
        "official_site": "https://www.azieleliab.com/",
        "library": "https://www.azielcorpuslibrary.net/",
        "godlock": "https://godlock.uk/",
        "github": "https://github.com/AzielEliab",
        "runtime": "https://aziel-runtime.vibelock.workers.dev/",
        "surfaces": {
            "person_jsonld": f"{WWW}/person.jsonld",
            "identity_jsonld": f"{WWW}/identity.jsonld",
            "graph_jsonld": f"{WWW}/graph.jsonld",
            "who_is": f"{WWW}/who-is-aziel-eliab.txt",
            "well_known": f"{WWW}/.well-known/aziel.json",
        },
    }


def who_is_txt() -> str:
    same = "\n".join(f"- {u}" for u in SAME_AS)
    hebrew = "\n".join(f"- {h}" for h in HEBREW_FORMS)
    miss = "\n".join(f"- {m}" for m in MISSPELLINGS)
    sisters = "\n".join(
        f"- {h['label']}: " + ", ".join(
            f"{k}={v}" for k, v in h.items() if k not in {"id", "label"}
        )
        for h in STATS["sister_hubs"]
    )
    return f"""Who is Aziel Eliab?

Person @id (shared identity lock): {PERSON_ID}
Name: Aziel Eliab
alternateName (SEO only): Aziel Elroi Eliab
additionalName: Elroi
GitHub: AzielEliab
Official site: https://www.azieleliab.com/

Identity note: public identity is Aziel Eliab only. Elroi, Hebrew aka forms, and listed misspellings are SEO alternateName tethers only. This host is An Aziel Eliab Project, not a second Person, and not the biblical Aziel or biblical Eliab.

Disambiguation: {DISAMBIGUATING}

{PERSON_DESCRIPTION}

Mission:
{MISSION}

Hebrew aka (SEO tether only)
{hebrew}

Misspelling alternateNames (SEO tether only)
{miss}

FAQ
Q: Who is Aziel Eliab?
A: {FAQ_WHO}

Q: What is He Didn’t Jump?
A: {FAQ_WHAT}

Q: Is Aziel Eliab the biblical Aziel?
A: {FAQ_BIBLICAL_AZIEL}

Q: Is Aziel Eliab the biblical Eliab?
A: {FAQ_BIBLICAL_ELIAB}

sameAs / reciprocal hubs
{same}

Local meter (do not retarget folio pills)
- {STATS['local']['stats']}
- {STATS['local']['hit']}
- {STATS['local']['worker_stats']}
- {STATS['local']['meter_contract']}

Sister-hub stats / social-status (awareness only)
{sisters}

Identity machine on this host
- {WWW}/person.jsonld
- {WWW}/identity.jsonld
- {WWW}/graph.jsonld
- {WWW}/who-is-aziel-eliab.txt
- {WWW}/.well-known/aziel.json

Official-narrative page (90-year public suicide account, labeled as such):
{WWW}/official-narrative.html

Independent archive (main paper + five volumes):
{WWW}/
"""


FAQ_SCRIPT = (
    '<script type="application/ld+json" id="azindex-faq">\n'
    + dumps({"@context": "https://schema.org", **FAQ_PAGE}).rstrip()
    + "\n</script>\n"
)

IDENTITY_LINKS = """<link rel="alternate" type="application/ld+json" href="/person.jsonld" title="Person JSON-LD">
<link rel="alternate" type="application/ld+json" href="/identity.jsonld" title="Identity JSON-LD">
<link rel="alternate" type="application/ld+json" href="/graph.jsonld" title="Identity graph JSON-LD">
<link rel="alternate" type="text/plain" href="/who-is-aziel-eliab.txt" title="Who is Aziel Eliab">
<link rel="alternate" type="application/json" href="/.well-known/aziel.json" title="Aziel well-known identity">
"""

OLD_ALT = '''      "alternateName": [
        "Aziel Elroi Eliab",
        "AzielEliab"
      ],
      "additionalName": "Elroi",'''

NEW_ALT = (
    '      "alternateName": '
    + json.dumps(ALTERNATE_NAMES, ensure_ascii=False, indent=8).replace("\n", "\n      ")
    + ',\n      "additionalName": "Elroi",\n'
    + '      "disambiguatingDescription": '
    + json.dumps(DISAMBIGUATING, ensure_ascii=False)
    + ","
)

INDEX_META = {
    "title": "He Didn't Jump — Independent Archive vs the Official 7 Aug 1936 Suicide Account",
    "description": (
        "An Aziel Eliab Project: five research volumes and newspaper inquiries challenging "
        "the official 7 August 1936 Arctic Building suicide account of U.S. Representative "
        "Marion Zioncheck. Publishes the record; does not invent court holdings, quotes, or agency letters."
    ),
}

NARRATIVE_META = {
    "title": "Official 7 Aug 1936 Arctic Building Suicide Account — He Didn't Jump",
    "description": (
        "Labeled official/contemporary account only: the 90-year public story that Marion "
        "Zioncheck died by suicide from a fifth-floor Arctic Building office on 7 August 1936. "
        "Contrast the independent five-volume archive on the main paper. Does not invent court holdings."
    ),
}


def write_identity_files() -> None:
    payloads = {
        "person.jsonld": dumps(person_jsonld()),
        "identity.jsonld": dumps(identity_jsonld()),
        "graph.jsonld": dumps(graph_jsonld()),
        "who-is-aziel-eliab.txt": who_is_txt(),
        ".well-known/aziel.json": dumps(well_known_aziel()),
    }
    for tree in TREES:
        (tree / ".well-known").mkdir(parents=True, exist_ok=True)
        for rel, body in payloads.items():
            path = tree / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
            print("wrote", path.relative_to(ROOT))


def _swap_meta(text: str, old_title: str, new_title: str, old_desc: str, new_desc: str) -> str:
    text = text.replace(f"<title>{old_title}</title>", f"<title>{new_title}</title>")
    text = text.replace(f'content="{old_desc}"', f'content="{new_desc}"')
    text = text.replace(f'content="{old_title}"', f'content="{new_title}"')
    return text


def patch_html_pages() -> None:
    html_names = (
        "index.html",
        "official-narrative.html",
        "rubye.html",
        "foia.html",
        "copyrights.html",
        "reader.html",
        "aziel.html",
        "volumes.html",
    )
    for tree in TREES:
        for name in html_names:
            path = tree / name
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            if OLD_ALT in text:
                text = text.replace(OLD_ALT, NEW_ALT)
            if 'id="azindex-faq"' not in text and name in {
                "index.html",
                "official-narrative.html",
                "aziel.html",
            }:
                text = text.replace("</head>", FAQ_SCRIPT + "</head>")
            if 'href="/person.jsonld"' not in text and name in {
                "index.html",
                "official-narrative.html",
                "aziel.html",
            }:
                text = text.replace(
                    '<link rel="alternate" type="text/plain" href="https://hedidntjump.com/llms.txt" title="LLM instructions">\n',
                    '<link rel="alternate" type="text/plain" href="https://hedidntjump.com/llms.txt" title="LLM instructions">\n'
                    + IDENTITY_LINKS,
                )
            if name == "index.html":
                text = _swap_meta(
                    text,
                    "He Didn't Jump — The Marion Zioncheck Archive",
                    INDEX_META["title"],
                    "An Aziel Eliab Project: independent newspaper archive on Marion Zioncheck’s 7 August 1936 death in Seattle. Five research volumes, contemporary plates, and 23 inquiries of the record.",
                    INDEX_META["description"],
                )
                text = text.replace(
                    '"name": "He Didn\'t Jump — The Marion Zioncheck Archive"',
                    '"name": "He Didn\'t Jump — independent archive challenging the official 7 Aug 1936 suicide account"',
                )
                text = text.replace(
                    "His death in Seattle on August 7, 1936 was reported as suicide following a fall from his fifth-floor office. This project challenges that account.",
                    "His death in Seattle on 7 August 1936 was reported as suicide from a fifth-floor Arctic Building office. This independent five-volume archive challenges that official account and does not invent court holdings.",
                )
            if name == "official-narrative.html":
                text = _swap_meta(
                    text,
                    "The Narrative — Official Account — He Didn't Jump",
                    NARRATIVE_META["title"],
                    "The official narrative of Marion Zioncheck’s 1936 death as the contemporary public account told it — with archive clippings side by side.",
                    NARRATIVE_META["description"],
                )
                text = text.replace(
                    "The Official Narrative — He Didn't Jump",
                    NARRATIVE_META["title"],
                )
                text = text.replace(
                    "Aziel Eliab edition: the contemporary official account of Marion Zioncheck’s last months — Washington apartment press, Gallinger, the train west, and the reported Arctic Building suicide.",
                    NARRATIVE_META["description"],
                )
                text = text.replace(
                    '"name": "The Official Narrative — He Didn\'t Jump"',
                    '"name": "Official 7 Aug 1936 Arctic Building suicide account — He Didn\'t Jump"',
                )
            path.write_text(text, encoding="utf-8")
            print("patched", path.relative_to(ROOT))


if __name__ == "__main__":
    write_identity_files()
    patch_html_pages()
