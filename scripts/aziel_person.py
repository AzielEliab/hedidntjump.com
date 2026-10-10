"""Shared Aziel Eliab publisher Person lock for hedidntjump.com.

Used by identity-machine, SERP, and page JSON-LD writers.
Person @id is exactly https://www.azieleliab.com/#aziel.
Never emit Everblooming Flower. Never sameAs euaziel / Aziel S.
"""
from __future__ import annotations

import json
from typing import Any

from aziel_living import JOB_TITLES as LOCKED_JOB_TITLES
from aziel_living import LIVING_STACK as LIVING_ROLE_STACK

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

# Monikers lead alternateName, in this order. Existing variants follow.
MONIKERS = [
    "Aziel Elroi Eliab",
    "AzielEliab",
    "azieleliab",
    "The Revealer of the Sealed",
    "Elias Artista",
]
REQUIRED_AKA = list(MONIKERS)

# Legitimate variants already in the archive. Not new misspellings.
KEPT_AKA = [
    "The Revealer of The Sealed",
    "Revealer of The Sealed",
]

REVEALER_AKA_SHORT = "Revealer of The Sealed"

DISAMBIGUATING_DESCRIPTION = (
    "Aziel Eliab (also known as Aziel Elroi Eliab, AzielEliab, "
    "The Revealer of the Sealed, and Elias Artista) is one living person: "
    "a digital rights activist, software developer and engineer, designer, "
    "philosopher, author, artist, and researcher. Not the two Levitical "
    "musicians Aziel and Eliab named together in 1 Chronicles 15:20."
)

# Domains the Person knows about because of the verified body of work.
KNOWS_ABOUT_DOMAINS = [
    "digital rights",
    "AI runtimes / MCP",
    "skilled-trades software",
    "operating systems philosophy",
    "open hardware",
    "neuroplasticity research",
    "historical archives/Marion Zioncheck",
]

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
    "https://x.com/AzielEliab",
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
    f"{ORIGIN}/case",
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


def occupations() -> list[dict[str, str]]:
    return [{"@type": "Occupation", "name": title} for title in LOCKED_JOB_TITLES]


def alternate_names(existing: list[str] | None = None) -> list[str]:
    return _dedupe(
        [
            *MONIKERS,
            *KEPT_AKA,
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


def _rewrite_role_prose(text: str) -> str:
    """Align retired Aziel role phrases to the locked living stack.

    Does not invent biography. Marion job titles are not passed through here.
    """
    if not text:
        return text
    replacements = (
        (
            "researcher, software developer, digital civil rights activist, and truthseeker",
            LIVING_ROLE_STACK,
        ),
        (
            "researcher, software developer, digital civil rights activist, truthseeker",
            LIVING_ROLE_STACK,
        ),
        (
            "is an independent researcher, software designer, developer, and historian",
            f"is a {LIVING_ROLE_STACK}",
        ),
        (
            "independent researcher, software designer, developer, and historian",
            LIVING_ROLE_STACK,
        ),
        (
            "independent researcher, software designer, developer, historian",
            LIVING_ROLE_STACK,
        ),
        (
            "Living researcher and software designer named Aziel Eliab",
            f"Living {LIVING_ROLE_STACK} named Aziel Eliab",
        ),
        (
            "living researcher and software designer named Aziel Eliab",
            f"living {LIVING_ROLE_STACK} named Aziel Eliab",
        ),
        (
            "Aziel Eliab is a living researcher and software designer",
            f"Aziel Eliab is a living {LIVING_ROLE_STACK}",
        ),
        (
            "Aziel Eliab is one living researcher and software designer",
            f"Aziel Eliab is one living {LIVING_ROLE_STACK}",
        ),
        (
            "one living researcher and software designer",
            f"one living {LIVING_ROLE_STACK}",
        ),
    )
    out = text
    for old, new in replacements:
        out = out.replace(old, new)
    bare = (
        f"{PERSON_NAME} (also Aziel Elroi Eliab; Elias Artista; "
        "The Revealer of The Sealed)."
    )
    role_lead = (
        f"{PERSON_NAME} (also Aziel Elroi Eliab; Elias Artista; "
        f"The Revealer of The Sealed) is a {LIVING_ROLE_STACK}."
    )
    if bare in out and LIVING_ROLE_STACK not in out:
        out = out.replace(bare, role_lead, 1)
    lead = "Publisher of this Marion Zioncheck archive."
    aligned = (
        f"{PERSON_NAME} is a {LIVING_ROLE_STACK}. "
        "Publisher of this Marion Zioncheck archive."
    )
    if lead in out and LIVING_ROLE_STACK not in out:
        out = out.replace(lead, aligned, 1)
    return out


def publisher_person(*, job_title: Any = None, existing: dict | None = None) -> dict:
    """Full publisher Person node. jobTitle is the locked living stack.

    job_title is accepted for callers that used to pass \"Publisher\" on
    Marion money pages. That fork is retired: one Person, one role stack.
    """
    del job_title
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
        "url": src.get("url") or CANONICAL_URL,
        "sameAs": same_as(existing_same),
    }
    if src.get("identifier") is not None:
        node["identifier"] = src["identifier"]
    else:
        node["identifier"] = PERSON_NAME

    node["jobTitle"] = list(LOCKED_JOB_TITLES)
    node["hasOccupation"] = occupations()
    node["disambiguatingDescription"] = DISAMBIGUATING_DESCRIPTION

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
    # hebrewDefinition is not a schema.org Person property. Keep it only
    # under additionalProperty.
    node.pop("hebrewDefinition", None)

    knows = node.get("knowsAbout")
    if isinstance(knows, str):
        knows = [knows]
    elif not isinstance(knows, list):
        knows = []
    for domain in KNOWS_ABOUT_DOMAINS:
        if domain not in knows:
            knows.append(domain)
    node["knowsAbout"] = knows

    desc = src.get("description") or ""
    if not desc:
        node["description"] = (
            f"{PERSON_NAME} (also Aziel Elroi Eliab; Elias Artista; "
            f"The Revealer of The Sealed). {HEBREW_ONELINER} {NOT_LOCK}"
        )
    elif "Not biblical Aziel" not in desc and "1 Chronicles 15:20" not in desc:
        node["description"] = desc.rstrip() + " " + NOT_LOCK

    # Drop any banned aka if a prior file smuggled it in.
    node["alternateName"] = [
        n for n in node["alternateName"] if not any(b.lower() in n.lower() for b in BANNED_AKA)
    ]
    if node.get("description"):
        node["description"] = _rewrite_role_prose(node["description"])
    node["disambiguatingDescription"] = DISAMBIGUATING_DESCRIPTION
    return node


def enrich_person_node(node: dict, *, money: bool = False) -> dict:
    # money=True used to fork jobTitle to "Publisher". One locked stack now.
    del money
    return publisher_person(existing=node)


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
    del money
    person = publisher_person()
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
    assert list(aka[: len(MONIKERS)]) == list(MONIKERS), aka[: len(MONIKERS)]
    for needle in (*REQUIRED_AKA, *KEPT_AKA, "AzielElroiEliab", "Aziel-Elroi-Eliab", "ElRoi"):
        assert needle in aka, needle
    assert node.get("jobTitle") == list(LOCKED_JOB_TITLES)
    occ = node.get("hasOccupation") or []
    assert [item.get("name") for item in occ] == list(LOCKED_JOB_TITLES)
    assert all(item.get("@type") == "Occupation" for item in occ)
    assert node.get("disambiguatingDescription") == DISAMBIGUATING_DESCRIPTION
    props = node.get("additionalProperty") or []
    if isinstance(props, dict):
        props = [props]
    if any(isinstance(p, dict) and p.get("propertyID") == "hebrewDefinition" for p in props):
        assert "hebrewDefinition" not in node
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
