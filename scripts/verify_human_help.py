#!/usr/bin/env python3
"""Assert additive human help / addendum txt + sitemap."""
from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from aziel_living import HELP_PATHS, LLMS_LEAD, PERSON_ID

ROOT = Path(__file__).resolve().parents[1]
APEX = "https://hedidntjump.com"

SEO_SURFACES = (
    "llms.txt",
    "llms-full.txt",
    "ai.txt",
    "cite.json",
)

BANNED = (
    "THIS IS NOT",
    "What this is not",
    "does not really",
    "what not to say",
    "Not a courtroom verdict",
    "Not a Softwares card",
    "Not a Softwares clone",
    "Who is Aziel Eliab not?",
    "blocked from",
    "CNS-ZENODO-IP-BAN",
    "CNS-GITFLIC-EMAIL",
    "CNS-GITLAB-CF-LOOP",
    "NOT an ARG",
    "HDJ is not a Lamb Lens ingest host",
    "HDJ is not a live exec door",
    "HDJ is not a named live exec front",
    "this is not a Softwares / mesh fan-out",
    "",
    "durable",
    "survival",
    "",
    "",
    "never ",
    "",
)


def main() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for marker in (
        "not a live exec door",
        "not a Softwares clone",
        "blocked from",
        "CNS-ZENODO-IP-BAN",
        "",
        "survival",
        "durable",
        "",
    ):
        assert marker not in readme, f"README still has {marker}"
    assert "Zioncheck archive" in readme

    for tree_name in ("docs", "dist"):
        tree = ROOT / tree_name
        help_txt = (tree / "help.txt").read_text(encoding="utf-8")
        addendum = (tree / "addendum.txt").read_text(encoding="utf-8")
        how = (tree / "help" / "how-to-read.txt").read_text(encoding="utf-8")
        for blob, label in (
            (help_txt, "help.txt"),
            (addendum, "addendum.txt"),
            (how, "how-to-read.txt"),
        ):
            assert "Marion" in blob and "Zioncheck" in blob, label
            assert "Volume" in blob, label
            assert f"{APEX}/" in blob, label
            assert "whistleblower" in blob.lower() or "investigative" in blob.lower(), label
            assert "NOT an ARG" not in blob, label
            assert "blocked from" not in blob, label
            for marker in (
                "",
                "durable",
                "survival",
                "",
                "",
            ):
                assert marker not in blob.lower(), f"{label} still has {marker}"
        assert PERSON_ID in help_txt
        assert "The Record, Not the Verdict" in help_txt
        assert LLMS_LEAD.split(".")[0] in help_txt or "newspapers and five volumes" in help_txt
        assert f"{APEX}/volumes/volume-1.pdf" in help_txt
        assert f"{APEX}/reader?volume=1&page=1" in how
        assert "this is not freedom of information" in addendum

        sitemap = (tree / "sitemap.xml").read_text(encoding="utf-8")
        for loc in HELP_PATHS:
            assert f"<loc>{APEX}{loc}</loc>" in sitemap, loc

        robots = (tree / "robots.txt").read_text(encoding="utf-8")
        assert "Allow: /help.txt" in robots
        assert "this is not a Softwares / mesh fan-out" not in robots

        cite = json.loads((tree / "cite.json").read_text(encoding="utf-8"))
        for loc in HELP_PATHS:
            assert f"{APEX}{loc}" in cite["query_urls"], loc
        assert cite["human_help"]["help"] == f"{APEX}/help.txt"

        openapi = json.loads((tree / "openapi.json").read_text(encoding="utf-8"))
        for loc in HELP_PATHS:
            assert loc in openapi["paths"], loc

        for rel in SEO_SURFACES:
            text = (tree / rel).read_text(encoding="utf-8")
            for marker in BANNED:
                assert marker not in text, f"{tree_name}/{rel} still has {marker}"
            assert "Zioncheck" in text
            assert "whistleblower" in text.lower() or "investigative" in text.lower()

    print("human help / addendum OK")


if __name__ == "__main__":
    main()
