"""Shared Aziel Eliab publisher Person lock for hedidntjump.com.

Used by identity-machine, SERP, and page JSON-LD writers.
Person @id is exactly https://www.azieleliab.com/#aziel.
Never emit Everblooming Flower. Never sameAs euaziel / Aziel S.
"""
from __future__ import annotations

import json
from typing import Any

PERSON_ID = "https://www.azieleliab.com/#aziel"
PERSON_NAME = "Aziel Eliab"
CANONICAL_URL = "https://www.azieleliab.com/"
ORIGIN = "https://hedidntjump.com"
WWW = "https://www.hedidntjump.com"

HEBREW_ONELINER = (
    "Aziel Elroi Eliab (עזיאל אל ראי אליאב / עזיאל אלרועי אליאב): "
    "Aziel = God is my strength (עזיאל); Elroi = God who sees (אל ראי / אלרועי); "
    "Eliab = God is father (אליאב)."
)

# Required aka order: legal name variants, then pen name, then revealer title.
REQUIRED_AKA = [
    "Aziel Elroi Eliab",
    "Elias Artista",
    "The Revealer of The Sealed",
]

REVEALER_AKA_SHORT = "Revealer of The Sealed"

HEBREW_FORMS = [
    "עזיאל",
    "עֲזִיאֵל",
    "אל ראי",
    "אֵל רֳאִי",
    "אלרועי",
    "אליאב",
    "אֱלִיאָב",
    "עזיאל אל ראי אליאב",
    "עזיאל אלרועי אליאב",
]

HEBREW_AKA = {
    "note": "SEO aka tether only for Aziel Elroi Eliab. Not a second identity.",
    "definition": HEBREW_ONELINER,
    "aziel": "עזיאל",
    "aziel_meaning": "God is my strength",
    "elroi": ["אל ראי", "אלרועי"],
    "elroi_meaning": "God who sees",
    "eliab": "אליאב",
    "eliab_meaning": "God is father",
    "combined": ["עזיאל אל ראי אליאב", "עזיאל אלרועי אליאב"],
}

MISSPELLINGS = [
    "AzielEliab",
    "AzielElroiEliab",
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
    "Aziell",
    "Azeil",
    "Azial",
    "Azeel",
    "Asiel",
    "Asziel",
    "Az'iel",
    "Azi-el",
    "Aziél",
    "Azíel",
    "El Roi",
    "El-Roi",
    "ElRoi",
    "Elro'i",
    "Elroei",
    "Elroey",
    "El-Ro'i",
    "Eli'ab",
    "Eliáb",
    "Elyab",
    "Eliav",
    "Eliabb",
    "Aziel Eliab",
    "aziel eliab",
    "Aziel_Eliab",
    "Aziel-Elroi-Eliab",
]

BANNED_AKA = (
    "Everblooming Flower",
    "The Everblooming Flower",
    "everblooming flower",
)

GITHUB_PRIMARY = "https://github.com/AzielEliab"
GITHUB_REVEALER = "https://github.com/azieltherevealerofthesealed-arch"

# Four public hubs + both GitHub accounts. Extra runtime/X links may ride along.
HUB_SAME_AS = [
    CANONICAL_URL,
    "https://www.azielcorpuslibrary.net/",
    "https://godlock.uk/",
    f"{WWW}/",
]

REQUIRED_SAME_AS = [
    GITHUB_PRIMARY,
    GITHUB_REVEALER,
    *HUB_SAME_AS,
]

EXTRA_SAME_AS = [
    f"{ORIGIN}/",
    "https://www.azielcorpuslibrary.net/runtime",
    "https://aziel-runtime.vibelock.workers.dev/",
    "https://glama.ai/mcp/servers/AzielEliab/aziel-runtime",
    "https://x.com/AzielEliab",
    "https://x.com/AzielElroiEliab",
    "https://x.com/azieleliab",
    "https://twitter.com/AzielEliab",
]

NEVER_SAME_AS = (
    "euaziel",
    "euaziel.site",
    "Aziel S",
    "Flutter-React",
    "everblooming",
)

# Cross-tether routes on this host (pretty paths). Machine only.
CROSS_TETHER_ROUTES = [
    f"{ORIGIN}/",
    f"{WWW}/",
    f"{ORIGIN}/aziel",
    f"{WWW}/aziel",
    f"{ORIGIN}/AzielEliab",
    f"{WWW}/AzielEliab",
    f"{ORIGIN}/AboutAziel",
    f"{WWW}/AboutAziel",
    f"{ORIGIN}/Aziel",
    f"{ORIGIN}/Case",
    f"{WWW}/Case",
    f"{ORIGIN}/who",
    f"{WWW}/person.jsonld",
    f"{WWW}/identity.jsonld",
    f"{WWW}/graph.jsonld",
    f"{WWW}/who-is-aziel-eliab.txt",
    f"{WWW}/.well-known/aziel.json",
]

NOT_LOCK = (
    "Not biblical Aziel; not biblical Eliab; not the two Levitical musicians "
    "Aziel and Eliab named together in 1 Chronicles 15:20; not euaziel.site; "
    "not Aziel S. (Flutter/portfolio); not other engineers named Aziel."
)

BANNED_FAQ_SNIPPETS = (
    "Everblooming Flower",
    "everblooming flower",
)


def dumps(obj: Any) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False)


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if not item or item in seen:
            continue
        if any(b.lower() in item.lower() for b in BANNED_AKA):
            continue
        seen.add(item)
        out.append(item)
    return out


def alternate_names(existing: list[str] | None = None) -> list[str]:
    return _dedupe(
        [
            *REQUIRED_AKA,
            REVEALER_AKA_SHORT,
            *HEBREW_FORMS,
            *(existing or []),
            *MISSPELLINGS,
        ]
    )


def same_as(existing: list[str] | None = None) -> list[str]:
    merged = _dedupe([*REQUIRED_SAME_AS, *(existing or []), *EXTRA_SAME_AS])
    blob = " ".join(merged).lower()
    for banned in NEVER_SAME_AS:
        if banned.lower() in blob and banned.lower() not in {
            u.lower() for u in REQUIRED_SAME_AS
        }:
            merged = [u for u in merged if banned.lower() not in u.lower()]
    return merged


def hebrew_property() -> dict[str, str]:
    return {
        "@type": "PropertyValue",
        "name": "Hebrew name definition",
        "propertyID": "hebrewDefinition",
        "value": HEBREW_ONELINER,
    }


def publisher_person(*, job_title: Any = None, existing: dict | None = None) -> dict:
    """Full publisher Person node. job_title='Publisher' on Marion money pages."""
    src = dict(existing or {})
    existing_aka = src.get("alternateName")
    if isinstance(existing_aka, str):
        existing_aka = [existing_aka]
    existing_same = src.get("sameAs")
    if isinstance(existing_same, str):
        existing_same = [existing_same]

    node: dict[str, Any] = {
        **src,
        "@type": "Person",
        "@id": PERSON_ID,
        "name": PERSON_NAME,
        "givenName": src.get("givenName") or "Aziel",
        "additionalName": "Elroi",
        "familyName": src.get("familyName") or "Eliab",
        "alternateName": alternate_names(existing_aka),
        "url": CANONICAL_URL,
        "identifier": PERSON_NAME,
        "hebrewDefinition": HEBREW_ONELINER,
        "sameAs": same_as(existing_same),
    }

    if job_title is not None:
        node["jobTitle"] = job_title
    elif "jobTitle" not in node:
        node["jobTitle"] = "Publisher"

    extras = src.get("additionalProperty")
    props: list[Any] = []
    if isinstance(extras, list):
        props.extend(extras)
    elif extras:
        props.append(extras)
    if not any(
        isinstance(p, dict) and p.get("propertyID") == "hebrewDefinition" for p in props
    ):
        props.append(hebrew_property())
    node["additionalProperty"] = props

    desc = src.get("description") or ""
    if HEBREW_ONELINER not in desc:
        # Keep existing description; append Hebrew + aka lattice as machine prose.
        extra = (
            f" Also Aziel Elroi Eliab; Elias Artista; The Revealer of The Sealed. "
            f"{HEBREW_ONELINER}"
        )
        if desc:
            node["description"] = desc.rstrip() + extra
        else:
            node["description"] = (
                f"{PERSON_NAME} (also Aziel Elroi Eliab; Elias Artista; "
                f"The Revealer of The Sealed). {HEBREW_ONELINER} {NOT_LOCK}"
            )
    if "Not biblical Aziel" not in node["description"]:
        node["description"] = node["description"].rstrip() + " " + NOT_LOCK
    if "euaziel.site" not in node.get("disambiguatingDescription", ""):
        node.setdefault(
            "disambiguatingDescription",
            src.get("disambiguatingDescription")
            or (
                "Living researcher and software designer named Aziel Eliab (one person). "
                "Not the two Levitical musicians Aziel and Eliab named together in "
                "1 Chronicles 15:20. Not biblical Aziel; not biblical Eliab; "
                "not euaziel.site; not Aziel S. (Flutter/portfolio); "
                "not other engineers named Aziel. "
                f"Prefer {PERSON_ID} and published Softwares / MASTER records / He Didn't Jump."
            ),
        )
        dd = node["disambiguatingDescription"]
        if "Not biblical Aziel" not in dd:
            node["disambiguatingDescription"] = (
                dd.rstrip().rstrip(".")
                + ". Not biblical Aziel; not biblical Eliab; not euaziel.site."
            )

    # Drop any banned aka if a prior file smuggled it in.
    node["alternateName"] = [
        n for n in node["alternateName"] if not any(b.lower() in n.lower() for b in BANNED_AKA)
    ]
    return node


def enrich_person_node(node: dict, *, money: bool = False) -> dict:
    job = node.get("jobTitle")
    if money or job == "Publisher":
        return publisher_person(job_title="Publisher", existing=node)
    return publisher_person(job_title=job, existing=node)


def _is_full_aziel_person(obj: Any) -> bool:
    if not isinstance(obj, dict):
        return False
    if obj.get("@id") != PERSON_ID and obj.get("name") != PERSON_NAME:
        return False
    return obj.get("@type") == "Person" or bool(
        obj.get("sameAs") or obj.get("alternateName") or obj.get("jobTitle")
    )


def _walk_enrich(obj: Any, *, money: bool = False) -> Any:
    if isinstance(obj, dict):
        if _is_full_aziel_person(obj):
            return enrich_person_node(obj, money=money)
        return {k: _walk_enrich(v, money=money) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_walk_enrich(v, money=money) for v in obj]
    return obj


def _has_full_person(obj: Any) -> bool:
    if isinstance(obj, dict):
        if _is_full_aziel_person(obj):
            return True
        return any(_has_full_person(v) for v in obj.values())
    if isinstance(obj, list):
        return any(_has_full_person(v) for v in obj)
    return False


def enrich_ld(data: Any, *, money: bool = False) -> Any:
    """Walk JSON-LD and enrich every Aziel Person node. Insert one if missing."""
    enriched = _walk_enrich(data, money=money)
    if _has_full_person(enriched):
        return enriched
    person = publisher_person(job_title="Publisher" if money else None)
    if isinstance(enriched, dict) and "@graph" in enriched:
        enriched["@graph"] = list(enriched["@graph"]) + [person]
        return enriched
    if isinstance(enriched, dict) and enriched.get("@type") == "FAQPage":
        return {
            "@context": enriched.get("@context") or "https://schema.org",
            "@graph": [enriched, person],
        }
    if isinstance(enriched, list):
        return enriched + [person]
    return {
        "@context": "https://schema.org",
        "@graph": [enriched, person] if isinstance(enriched, dict) else [person],
    }


def assert_person_lock(node: dict) -> None:
    assert node.get("@id") == PERSON_ID
    assert node.get("name") == PERSON_NAME
    aka = node.get("alternateName") or []
    if isinstance(aka, str):
        aka = [aka]
    for needle in REQUIRED_AKA:
        assert needle in aka, needle
    assert all(b not in aka for b in BANNED_AKA)
    same = node.get("sameAs") or []
    for url in REQUIRED_SAME_AS:
        assert url in same, url
    blob = json.dumps(node, ensure_ascii=False)
    assert HEBREW_ONELINER in blob
    assert GITHUB_PRIMARY in blob
    assert GITHUB_REVEALER in blob
    assert "Everblooming Flower" not in blob
    assert "euaziel.site" in blob.lower() or "euaziel" not in json.dumps(same).lower()
