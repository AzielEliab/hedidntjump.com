#!/usr/bin/env python3
"""Assert whole-project subsurface LLM review coverage. No HTML required."""
from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from archive_review import REVIEW_END, REVIEW_HEAD, VOLUME_TITLES
from aziel_living import PERSON_ID, SEO_BAN_MARKERS

HDJ_INGEST_TIP = "ef967e4acb47ba913ce3959b673767278da605b307de33210b2dc2f1cfd86f60"

ROOT = Path(__file__).resolve().parents[1]

INQUIRY_QUESTIONS = (
    "Why was Marion sent from Washington, D.C. to Seattle, Washington?",
    "Why do archive records conflict with the official narrative online today?",
    "Why was Marion trying to stay in the media and spotlight?",
    "What can photographs establish?",
    "Why does Nadeau’s account not match the setup of Zioncheck’s office — and why did his account change?",
    "Where are records to his “Who’s Crazy Now” speech?",
    "Why did Marion dress up for a speech — then decide to “jump”?",
    "Why did his wife never give a statement as the most prolific witness?",
    "Why did Rubye hide testimony in her art for a later generation to find?",
    "Why did Rubye relentlessly sue the Nadeaus after? Was it spite, or was she silenced too?",
    "Why are the injuries inconsistent with a five-story fall?",
    "Why were so few witnesses named — and why was one of them the person who broke the story?",
    "Why was the janitor unnamed — and why would he have walked away during the event?",
    "How and why did the record get meshed between the old Arctic building at 501 3rd Avenue and the new Arctic building at 3rd Avenue and Cherry Street?",
    "Where are his dinner-party speech papers?",
    "Why does his “suicide note” read like part of a speech — and why was it folded if he had just written it?",
    "Why was cousin “Vic” in the area to witness at all if he worked in another building — and why do minimal records of Vic or his cigar shop exist today?",
    "Does Marion’s work and background — from Naval Intelligence to fighting the Alaskan Highway Bill and being backed to establish a third political party — play a role?",
    "Is it a coincidence that Illinois statesman John Bolton died suspiciously less than one month before?",
    "Why are most of Nadeau’s records missing? Was he naval intelligence too?",
    "Why are FOIA requests on Marion denied to this day?",
    "Why was Marion’s mother never informed of his death — and is this why she died of Involutional Melancholia?",
    "Was Marion Zioncheck a threat to the establishment that couldn’t be silenced?",
)

TAB_HEADS = (
    "## Homepage money-page framing",
    "## Case",
    "## Press",
    "## Inquiries of the Record (1–23)",
    "## Rubye",
    "## Archives",
    "## FOIA",
    "## Volumes I–V",
    "## Narrative",
    "## About Aziel",
    "## Copyrights",
    "## Receipts / ingest (machine)",
    "## Who",
    "## Reader",
)


def main() -> None:
    for tree_name in ("docs", "dist"):
        tree = ROOT / tree_name
        full = (tree / "llms-full.txt").read_text(encoding="utf-8")
        llms = (tree / "llms.txt").read_text(encoding="utf-8")
        ai = (tree / "ai.txt").read_text(encoding="utf-8")
        cite = json.loads((tree / "cite.json").read_text(encoding="utf-8"))
        openapi = json.loads((tree / "openapi.json").read_text(encoding="utf-8"))

        assert REVIEW_HEAD in full, tree_name
        assert REVIEW_END in full, tree_name
        assert "whistleblower" in full.lower(), tree_name
        assert "NOT an ARG" not in full, tree_name
        assert PERSON_ID in full, tree_name
        assert HDJ_INGEST_TIP in full, tree_name
        for marker in SEO_BAN_MARKERS:
            assert marker not in full, f"{tree_name} llms-full has {marker}"

        for n, question in enumerate(INQUIRY_QUESTIONS, 1):
            assert f"### Inquiry {n:02d} — {question}" in full, f"{tree_name} missing inquiry {n}"
            assert question in full, f"{tree_name} missing question text {n}"

        # Surrounding substance, not titles only.
        assert "Kenneth Romney" in full
        assert "William Nadeau" in full
        assert "Victor Anthony" in full or "Victor Anthony / Antoni Zajaczek" in full
        assert "Involutional Melancholia" in full
        assert "Request No. 1750194-000" in full
        assert "full facsimile at" in full.lower() or "Full facsimile at" in full

        for n, title in VOLUME_TITLES.items():
            roman = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}[n]
            assert f"### Volume {roman} — {title}" in full, title
            assert f"{ORIGIN_SAFE}/volumes/volume-{n}.pdf" in full

        for head in TAB_HEADS:
            assert head in full, f"{tree_name} missing {head}"

        assert "whole-project LLM review" in llms
        assert "whole-project LLM review" in ai

        rec = cite["inquiries_of_the_record"]
        assert len(rec) == 23, tree_name
        assert rec[0]["question"] == INQUIRY_QUESTIONS[0]
        assert rec[22]["n"] == 23
        assert cite["person_id"] == PERSON_ID
        assert cite["author_id"] == PERSON_ID
        assert cite["llm_review"]["inquiries_count"] == 23
        vols = cite["research_volumes"]
        assert len(vols) == 5
        assert vols[0]["pdf"].endswith("/volumes/volume-1.pdf")
        assert vols[3]["full_text"] is None
        assert "full facsimile" in vols[0]["full_text_note"].lower()
        tabs = cite["tab_substance"]
        for key in (
            "home",
            "case",
            "press",
            "inquiries",
            "rubye",
            "archives",
            "foia",
            "volumes",
            "narrative",
            "aziel",
            "copyrights",
            "receipts",
            "who",
            "reader",
        ):
            assert key in tabs, key
            assert tabs[key]["substance"], key

        summary = openapi["paths"]["/llms-full.txt"]["get"]["summary"]
        assert "Inquiries 1–23" in summary
        assert "Volumes I–V" in summary

        # Trees stay in sync.
        other = "dist" if tree_name == "docs" else "docs"
        other_full = (ROOT / other / "llms-full.txt").read_text(encoding="utf-8")
        assert full == other_full

    print("llms-full review coverage verified (docs + dist, 23 inquiries, 5 volumes, all tabs)")


ORIGIN_SAFE = "https://hedidntjump.com"

if __name__ == "__main__":
    main()
