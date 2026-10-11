"""Verified Aziel Eliab body of work, from scripts/data/aziel_works.json.

Only http-200 items with verified:true are emitted. Items with a caution
note are skipped. doi.org and zenodo.org URLs are never emitted. Forks that
are not his software are skipped. Listings stay in machine files only.
"""
from __future__ import annotations

import json
from pathlib import Path

from aziel_person import PERSON_ID

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "scripts" / "data" / "aziel_works.json"
WORKS_URL = "https://hedidntjump.com/works.json"

# Featured papers kept on the homepage / about Person (curated, not the full corpus).
CURATED_PAPER_IDS = (
    "AZDOC-E03E61D8E50B",  # PPIN
    "AZDOC-DD5912D05D6E",  # ABAD Copper Scroll
    "AZDOC-E00603883906",  # Blemmyes
    "AZDOC-F22AD0DCAA9D",  # Libro Method
    "AZDOC-E3ABDBF3A1EA",  # TemporalLock
    "AZDOC-0671040C36E6",  # ForgeReceipts
)

WEBSLINGER_ID = "AZDOC-AA8761FE16D0"
WEBSLINGER_NAME = "Webslinger (Wearable Dual-Tether Web-Sling System)"

# AZ triad: three sides of one system. Design relationship only.
TRIAD_ID = "https://www.azieleliab.com/#az-triad"
TRIAD_NAME = "AZ triad: AZ-OS, Aziel Runtime, The AZInterface"
TRIAD_DESCRIPTION = (
    "One system with three sides: the operating-system layer (AZ-OS), "
    "the MCP runtime (Aziel Runtime), and the UI software (The AZInterface). "
    "Design relationship only."
)
AZOS_URL = "https://github.com/AzielEliab/azos"
RUNTIME_URL = "https://github.com/AzielEliab/aziel-runtime"
RUNTIME_ENDPOINT = "https://aziel-runtime.vibelock.workers.dev/"
RUNTIME_GLAMA = "https://glama.ai/mcp/servers/AzielEliab/aziel-runtime"
INTERFACE_URL = "https://github.com/AzielEliab/azinterface"
INTERFACE_PAPER = "https://www.azielcorpuslibrary.net/record/AZDOC-EB7454682E74"


def _url_key(url: str) -> str:
    return (url or "").rstrip("/")


TRIAD_SIDE_NOTES = {
    _url_key(AZOS_URL): (
        "Operating-system side of the AZ triad: a local ethical overlay, not a kernel."
    ),
    _url_key(RUNTIME_URL): "MCP side of the AZ triad.",
    _url_key(RUNTIME_ENDPOINT): "MCP side of the AZ triad.",
    _url_key(INTERFACE_URL): "UI-software side of the AZ triad.",
}

CATEGORY_ORDER = (
    "software",
    "websites",
    "hardware",
    "archives",
    "philosophy",
    "research_papers",
    "listings",
)


def load_catalog() -> dict:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def _clean(text: str) -> str:
    out = text.replace("\r\n", "\n").replace("\r", "\n")
    return " ".join(out.split())


def display_name(item: dict) -> str:
    url = item.get("url") or ""
    name = item.get("name") or ""
    if WEBSLINGER_ID in url or name == "Wearable Dual-Tether Web-Sling System":
        return WEBSLINGER_NAME
    return name


def usable(item: dict, *, listings: bool) -> bool:
    if item.get("verified") is not True:
        return False
    if item.get("http_status") not in (200, "200"):
        return False
    if item.get("caution"):
        return False
    if item.get("own_software") is False or item.get("is_fork"):
        return False
    url = item.get("url") or ""
    if not url.startswith("https://"):
        return False
    lowered = url.lower()
    if "doi.org" in lowered or "zenodo.org" in lowered:
        return False
    if not listings and item.get("_category") == "listings":
        return False
    return True


def iter_items(catalog: dict):
    categories = catalog.get("categories") or {}
    for category in CATEGORY_ORDER:
        for item in categories.get(category) or []:
            if isinstance(item, dict):
                row = dict(item)
                row["_category"] = category
                yield row


def full_items(catalog: dict | None = None) -> list[dict]:
    """Every verified own work, plus listings. No caution, no Zenodo URLs."""
    catalog = catalog or load_catalog()
    rows = []
    seen: set[str] = set()
    for item in iter_items(catalog):
        if not usable(item, listings=True):
            continue
        url = item["url"]
        if url in seen:
            continue
        seen.add(url)
        rows.append(item)
    return rows


def curated_items(catalog: dict | None = None) -> list[dict]:
    """Featured software, sites, hardware, archives, philosophy, plus key papers.

    Stays in the ~30–60 band for homepage / about JSON-LD. Listings are excluded.
    """
    catalog = catalog or load_catalog()
    chosen: list[dict] = []
    seen: set[str] = set()

    def add(item: dict) -> None:
        url = item.get("url") or ""
        if not url or url in seen:
            return
        if not usable(item, listings=False):
            return
        seen.add(url)
        chosen.append(item)

    by_cat: dict[str, list[dict]] = {cat: [] for cat in CATEGORY_ORDER}
    for item in iter_items(catalog):
        by_cat.setdefault(item["_category"], []).append(item)

    for category in ("software", "websites", "hardware", "archives"):
        for item in by_cat.get(category) or []:
            if item.get("featured"):
                add(item)
    for item in by_cat.get("philosophy") or []:
        if item.get("featured"):
            add(item)
    for item in by_cat.get("research_papers") or []:
        url = item.get("url") or ""
        if any(record_id in url for record_id in CURATED_PAPER_IDS):
            add(item)
    if not (30 <= len(chosen) <= 60):
        raise SystemExit(f"curated works count {len(chosen)} is outside 30–60")
    return chosen


def triad_side_note(url: str) -> str:
    return TRIAD_SIDE_NOTES.get(_url_key(url), "")


def _author_ref() -> dict:
    return {"@id": PERSON_ID}


def triad_node() -> dict:
    """CreativeWork for the AZ triad. Author is an @id ref, not a nested Person."""
    return {
        "@type": "CreativeWork",
        "@id": TRIAD_ID,
        "name": TRIAD_NAME,
        "description": TRIAD_DESCRIPTION,
        "author": _author_ref(),
        "creator": _author_ref(),
        "hasPart": [
            {
                "@type": "SoftwareSourceCode",
                "@id": _url_key(AZOS_URL) + "#aziel-work",
                "name": "AZ-OS",
                "url": AZOS_URL,
                "applicationCategory": "operating-system side",
                "description": (
                    "Operating-system side of the AZ triad. "
                    "A local ethical overlay that is not a kernel."
                ),
            },
            {
                "@type": "SoftwareSourceCode",
                "@id": _url_key(RUNTIME_URL) + "#aziel-work",
                "name": "Aziel Runtime",
                "url": RUNTIME_URL,
                "applicationCategory": "MCP side",
                "description": (
                    "MCP side of the AZ triad. "
                    f"Public endpoint {RUNTIME_ENDPOINT} "
                    f"Glama {RUNTIME_GLAMA}"
                ),
            },
            {
                "@type": "SoftwareSourceCode",
                "@id": _url_key(INTERFACE_URL) + "#aziel-work",
                "name": "The AZInterface",
                "url": INTERFACE_URL,
                "applicationCategory": "UI-software side",
                "description": (
                    "UI-software side of the AZ triad. "
                    f"White paper {INTERFACE_PAPER}"
                ),
            },
        ],
    }


def triad_markdown() -> str:
    return "\n".join(
        [
            TRIAD_NAME,
            TRIAD_DESCRIPTION,
            f"@id {TRIAD_ID}",
            f"- AZ-OS (operating-system side; local ethical overlay, not a kernel) — {AZOS_URL}",
            f"- Aziel Runtime (MCP side) — {RUNTIME_URL}",
            f"  Public endpoint — {RUNTIME_ENDPOINT}",
            f"  Glama — {RUNTIME_GLAMA}",
            f"- The AZInterface (UI-software side) — {INTERFACE_URL}",
            f"  White paper — {INTERFACE_PAPER}",
        ]
    )


def _annotate_triad(node: dict, url: str) -> dict:
    note = triad_side_note(url)
    if not note:
        return node
    description = node.get("description") or ""
    if note not in description:
        node["description"] = (description + " " + note).strip()
    node["isPartOf"] = {"@id": TRIAD_ID}
    return node


def work_node(item: dict) -> dict:
    url = item["url"]
    node = {
        "@type": item.get("type") or "CreativeWork",
        "@id": url.rstrip("/") + "#aziel-work",
        "name": display_name(item),
        "url": url,
    }
    description = _clean(item.get("description") or "")
    if description:
        node["description"] = description
    return _annotate_triad(node, url)


def curated_nodes(catalog: dict | None = None) -> list[dict]:
    return [work_node(item) for item in curated_items(catalog)]


def person_works(catalog: dict | None = None) -> list[dict]:
    """Curated works plus the triad node, for Person workExample / subjectOf."""
    return [*curated_nodes(catalog), triad_node()]


def machine_record(item: dict) -> dict:
    record = {
        "name": display_name(item),
        "url": item["url"],
        "type": item.get("type") or "CreativeWork",
        "category": item.get("_category"),
        "featured": bool(item.get("featured")),
    }
    description = _clean(item.get("description") or "")
    if description:
        record["description"] = description
    return _annotate_triad(record, item["url"])


def full_records(catalog: dict | None = None) -> list[dict]:
    return [machine_record(item) for item in full_items(catalog)]


def works_document(catalog: dict | None = None) -> dict:
    catalog = catalog or load_catalog()
    return {
        "@context": "https://schema.org",
        "person_id": PERSON_ID,
        "name": "Aziel Eliab",
        "url": WORKS_URL,
        "description": (
            "Verified works of Aziel Eliab. URLs are http 200 from the "
            "2026-10-06 catalog. Caution items, forks that are not his "
            "software, and Zenodo DOI links are omitted."
        ),
        "works": full_records(catalog),
        "curated": curated_nodes(catalog),
        "az_triad": triad_node(),
    }
