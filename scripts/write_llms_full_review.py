#!/usr/bin/env python3
"""Write subsurface LLM review files (llms-full, cite blocks, map pointers).

Machine files only. Does not rewrite newspaper HTML.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from archive_review import (
    ORIGIN,
    REVIEW_HEAD,
    build_review_body,
    cite_payload,
    extract_inquiries,
    extract_tabs,
    extract_two_arctics,
    extract_volumes,
    point_ai_txt,
    point_llms_txt,
    scrub_old_stack,
    scrub_payload,
    splice_review,
)

ROOT = Path(__file__).resolve().parents[1]
TREES = [ROOT / "dist", ROOT / "docs"]


def dumps(obj) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def patch_openapi(data: dict) -> dict:
    paths = data.setdefault("paths", {})
    full = paths.setdefault("/llms-full.txt", {"get": {}})
    get = full.setdefault("get", {})
    get["summary"] = (
        "Whole-project LLM review: Inquiries 1–23, Volumes I–V, and every public tab"
    )
    get.setdefault("responses", {}).setdefault("200", {})["description"] = (
        "text/plain extracted review surface (not a new historical argument)"
    )
    brief = paths.setdefault("/llms.txt", {"get": {}})
    brief.setdefault("get", {})["summary"] = (
        "LLM short map + whistleblower / investigative genre lock"
    )
    for n, roman, title in (
        (1, "I", "Primary Documents & Forensic Analysis"),
        (2, "II", "News Coverage & Family Battles"),
        (3, "III", "Personal Photographs & Research Materials"),
        (4, "IV", "The Physics Case"),
        (5, "V", "The Human & Institutional Evidence"),
    ):
        node = paths.setdefault(f"/volumes/volume-{n}.pdf", {"get": {}})
        node.setdefault("get", {})["summary"] = (
            f"Volume {roman} PDF — {title} (full facsimile; no invented OCR)"
        )
    return data


def patch_cite(data: dict, payload: dict) -> dict:
    data.update(payload)
    urls = list(data.get("query_urls") or [])
    review = f"{ORIGIN}/llms-full.txt"
    if review not in urls:
        # Keep the short map first; place the review surface beside it.
        if f"{ORIGIN}/llms.txt" in urls:
            idx = urls.index(f"{ORIGIN}/llms.txt") + 1
            urls.insert(idx, review)
        else:
            urls.append(review)
    data["query_urls"] = urls
    # Person @ids stay locked.
    data["person_id"] = data.get("person_id") or "https://www.azieleliab.com/#aziel"
    data["author_id"] = data.get("author_id") or "https://www.azieleliab.com/#aziel"
    return data


def write_trees() -> None:
    inquiries = extract_inquiries()
    volumes = extract_volumes()
    tabs = extract_tabs()
    two_arctics = extract_two_arctics()
    review = scrub_old_stack(build_review_body(inquiries, volumes, tabs, two_arctics))
    payload = scrub_payload(cite_payload(inquiries, volumes, tabs))

    for tree in TREES:
        full_path = tree / "llms-full.txt"
        full_path.write_text(
            splice_review(full_path.read_text(encoding="utf-8"), review),
            encoding="utf-8",
        )
        print("wrote", full_path.relative_to(ROOT), "bytes", full_path.stat().st_size)

        llms_path = tree / "llms.txt"
        llms_path.write_text(
            point_llms_txt(llms_path.read_text(encoding="utf-8")),
            encoding="utf-8",
        )
        print("pointed", llms_path.relative_to(ROOT))

        ai_path = tree / "ai.txt"
        ai_path.write_text(
            point_ai_txt(ai_path.read_text(encoding="utf-8")),
            encoding="utf-8",
        )
        print("pointed", ai_path.relative_to(ROOT))

        cite_path = tree / "cite.json"
        cite = json.loads(cite_path.read_text(encoding="utf-8"))
        cite_path.write_text(dumps(patch_cite(cite, payload)), encoding="utf-8")
        print("cite", cite_path.relative_to(ROOT))

        openapi_path = tree / "openapi.json"
        openapi = json.loads(openapi_path.read_text(encoding="utf-8"))
        openapi_path.write_text(dumps(patch_openapi(openapi)), encoding="utf-8")
        print("openapi", openapi_path.relative_to(ROOT))

    print("review head:", REVIEW_HEAD)
    print("inquiries:", len(inquiries), "volumes:", len(volumes), "tabs:", len(tabs))


if __name__ == "__main__":
    write_trees()
