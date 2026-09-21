#!/usr/bin/env python3
"""Assert HDJ SPORE-1.0 + RE-COLD-STORE hub cite stays honest and archive-focused."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from aziel_living import SOFTWARES_LIST  # noqa: E402
from write_spore import (  # noqa: E402
    APEX,
    FACES,
    HDJ_INGEST_TIP,
    LAMB_LENS,
    PERSON_ID,
    RUNTIME_GIT_SHORT,
    RUNTIME_PR,
    RUNTIME_VERSION_ID,
    SOT_URL,
    SPORE_PAPER,
    TTL_SECONDS,
    WWW,
)

PAPER_HTML = (
    "index.html",
    "case.html",
    "press.html",
    "inquiries.html",
    "inquires.html",
    "rubye.html",
    "archives.html",
    "foia.html",
    "volumes.html",
    "reader.html",
    "official-narrative.html",
    "copyrights.html",
    "aziel.html",
    "receipts.html",
    "who.html",
)

FORGED = (
    "Crazytown",
    "https://framagit.org/AzielEliab/aziel-lockset-tip",
    ": true",
    '"": true',
    '"resolves_to_hub": true',
    "this_host_is_live_door\": true",
    "Pg. 11",
)


def visible_text(html: str) -> str:
    html = re.sub(r"<script\b[^>]*>[\s\S]*?</script>", " ", html, flags=re.I)
    html = re.sub(r"<style\b[^>]*>[\s\S]*?</style>", " ", html, flags=re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    return html


def check_re_cold(payload: dict, label: str) -> None:
    cold = payload["re_cold_store"]
    assert cold["hook"] == "RE-COLD-STORE", label
    assert cold["allowed"] is True, label
    assert cold["active"] is False, label
    assert cold["shelves_failed"] is False, label
    assert cold["shelves_intact"] is True, label
    assert cold["invent_live"] is False, label
    assert cold["invent_hash"] is False, label
    assert cold["invent_receipt"] is False, label
    assert cold["invent_destination"] is False, label
    assert cold["public_inventory_required"] is False, label
    assert cold["destinations"] == [], label
    assert cold["opaque_placement"] is True, label
    assert "wipe is happening now" in cold["note"], label


def check_wrap(payload: dict, label: str) -> None:
    assert payload["spec"] == "SPORE-1.0", label
    assert payload["author"] == "Aziel Eliab", label
    assert payload["identity"] == "Aziel Eliab", label
    assert payload["person_id"] == PERSON_ID, label
    assert payload["visible_1520"] is False, label
    assert payload["softwares_clone"] is False, label
    assert payload["softwares_tab"] is False, label
    assert payload["fraggate_slug"] is False, label
    assert payload["this_host_is_live_door"] is False, label
    assert payload["this_host_runtime_front"] is False, label
    assert payload["mission"] == "Zioncheck archive", label
    assert payload["invented_destinations"] is False, label
    assert payload["invented_heartbeats"] is False, label
    assert payload["failsafe"] is True, label
    assert payload["last_resort"] is True, label
    assert payload["replaces_cold_shelves"] is False, label
    assert payload["replaces_ban_survival"] is False, label
    assert payload["cold_shelves_intact"] is True, label
    assert payload["mutual_backup_intact"] is True, label
    assert payload["ttl_seconds"] == TTL_SECONDS, label
    assert payload["sot"] == SOT_URL, label
    assert payload["runtime_pr"] == RUNTIME_PR, label
    assert payload["runtime_git_short"] == RUNTIME_GIT_SHORT, label
    assert payload["runtime_version_id"] == RUNTIME_VERSION_ID, label
    assert payload["paper"] == SPORE_PAPER, label
    assert payload["no_lie"].startswith("NO-LIE"), label
    assert payload["lamb_lens"]["shelf"] == LAMB_LENS, label
    assert list(payload["faces"]) == list(FACES), label
    ids = [row["id"] for row in payload["survival_stack"]]
    assert ids == ["live-fronts", "cold-shelves", "spore"], ids
    assert payload["survival_stack"][1]["replaced"] is False, label
    assert payload["survival_stack"][1]["failed"] is False, label
    check_re_cold(payload, label)
    spore = payload["spore"]
    assert spore["spec"] == "SPORE-1.0", label
    assert spore["replaces_cold_shelves"] is False, label
    assert spore["software_tab"] is False, label
    assert spore["doi"] is None, label
    assert spore["plane_b"] == "slot", label
    assert spore["plane_c"] == "slot", label
    assert payload["ingest_tip_unchanged"] == HDJ_INGEST_TIP, label


def check_survival_fields(payload: dict, label: str) -> None:
    assert payload["spore_spec"] == "SPORE-1.0", label
    assert payload["spore_role"] == "failsafe", label
    assert payload["spore_replaces_cold_shelves"] is False, label
    assert payload["runtime_version_id"] == RUNTIME_VERSION_ID, label
    assert payload["runtime_pr"] == RUNTIME_PR, label
    ids = [row["id"] for row in payload["survival_stack"]]
    assert ids == ["live-fronts", "cold-shelves", "spore"], ids
    check_re_cold(payload, label)
    spore = payload["spore"]
    assert spore["spec"] == "SPORE-1.0", label
    assert spore["failsafe"] is True, label
    assert spore["replaces_cold_shelves"] is False, label
    assert spore["software_tab"] is False, label
    assert spore["runtime_version_id"] == RUNTIME_VERSION_ID, label


def main() -> None:
    ingest_expected = (ROOT / "docs" / "ingest-as-receipt.json").read_bytes()
    assert hashlib.sha256(ingest_expected).hexdigest() == HDJ_INGEST_TIP

    pull = (ROOT / "functions" / "_lib" / "survival-pull.js").read_text(encoding="utf-8")
    assert SOT_URL in pull
    assert "SPORE-1.0" in pull
    assert "RE-COLD-STORE" in pull
    assert "spore_replaces_cold_shelves: false" in pull
    assert "invent_destination: false" in pull
    assert "destinations:" in pull
    assert RUNTIME_VERSION_ID in pull

    for tree_name in ("docs", "dist"):
        tree = ROOT / tree_name
        raw = (tree / "survival.json").read_text(encoding="utf-8")
        survival = json.loads(raw)
        check_survival_fields(survival, f"{tree_name}/survival.json")
        assert raw.endswith("\n")

        cite = json.loads((tree / "cite.json").read_text(encoding="utf-8"))
        check_wrap(cite["spore"], f"{tree_name}/cite.spore")
        check_survival_fields(cite["ban_survival"], f"{tree_name}/cite.ban_survival")
        check_re_cold(cite, f"{tree_name}/cite.re_cold_store")
        assert cite["person_id"] == PERSON_ID
        assert cite["identity"] == "Aziel Eliab"
        assert cite["visible_1520"] is False
        assert cite["about"] == "Marion A. Zioncheck archive"
        assert cite["ingest_as_receipt"]["tip"] == HDJ_INGEST_TIP
        assert cite["softwares_list"] == list(SOFTWARES_LIST), f"{tree_name} Softwares blurbs drifted"

        ingest = (tree / "ingest-as-receipt.json").read_bytes()
        assert hashlib.sha256(ingest).hexdigest() == HDJ_INGEST_TIP

        llms = (tree / "llms.txt").read_text(encoding="utf-8")
        llms_full = (tree / "llms-full.txt").read_text(encoding="utf-8")
        ai = (tree / "ai.txt").read_text(encoding="utf-8")
        who = (tree / "who-is").read_text(encoding="utf-8")
        who_txt = (tree / "who-is-aziel-eliab.txt").read_text(encoding="utf-8")
        assert who == who_txt
        for blob, label in (
            (llms, "llms"),
            (llms_full, "llms-full"),
            (ai, "ai"),
            (who, "who-is"),
        ):
            assert "SPORE-1.0" in blob, label
            assert "RE-COLD-STORE" in blob, label
            assert SOT_URL in blob, label
            assert RUNTIME_PR in blob, label
            assert RUNTIME_VERSION_ID in blob, label
            assert RUNTIME_GIT_SHORT in blob, label
            assert "last-resort failsafe" in blob.lower(), label
            assert "pause / preserve / wait / physical-wipe-only" in blob, label
            assert "Does not replace" in blob or "does not replace" in blob, label
            assert "destinations" in blob.lower(), label
            assert PERSON_ID in blob, label
            assert "NO-LIE" in blob, label
            assert "Lamb Lens" in blob, label
            assert "Zioncheck" in blob, label
            assert "Softwares-tab product: false" in blob or "software_tab" in blob, label
            assert "Not a Softwares clone" not in blob, label
            for forged in FORGED:
                if forged in ("Pg. 11",):
                    continue
                assert forged not in blob, f"{label} invented {forged}"

        lead = llms.split("## Marion")[0]
        assert "SPORE-1.0 + RE-COLD-STORE" in lead

        openapi = json.loads((tree / "openapi.json").read_text(encoding="utf-8"))
        assert "SPORE-1.0 + RE-COLD-STORE" in openapi["paths"]["/survival"]["get"]["summary"]
        assert "SPORE-1.0 + RE-COLD-STORE" in openapi["paths"]["/survival.json"]["get"]["summary"]

        wk = json.loads((tree / ".well-known" / "aziel.json").read_text(encoding="utf-8"))
        assert wk["spore"]["spec"] == "SPORE-1.0"
        assert wk["spore"]["sot"] == SOT_URL
        assert wk["spore"]["runtime_version_id"] == RUNTIME_VERSION_ID
        assert wk["spore"]["replaces_cold_shelves"] is False
        assert wk["spore"]["re_cold_store"] == "RE-COLD-STORE"
        assert wk["spore"]["destinations"] == []
        assert wk["spore"]["software_tab"] is False
        assert wk["spore"]["this_host_is_live_door"] is False
        assert wk["spore"]["mission"] == "Zioncheck archive"
        assert wk["spore"]["person_id"] == PERSON_ID

        launch = json.loads((tree / "runtime-launch.json").read_text(encoding="utf-8"))
        assert launch["spore"]["spec"] == "SPORE-1.0"
        assert launch["spore"]["runtime_version_id"] == RUNTIME_VERSION_ID
        assert launch["spore"]["destinations"] == []
        assert launch["spore"]["replaces_cold_shelves"] is False
        assert "designed to route catalog Softwares" in launch["runtime_sot"]["one_line"]

        for name in PAPER_HTML:
            html = (tree / name).read_text(encoding="utf-8")
            nav = re.search(r'<nav class="paper-tabs"[\s\S]*?</nav>', html)
            if nav:
                assert "Receipts" not in nav.group(0), f"{tree_name}/{name} paper-tabs gained Receipts"
                assert "Softwares" not in nav.group(0)
            if name != "who.html":
                visible = visible_text(html)
                assert "15:20" not in visible, f"{tree_name}/{name} gained visible 15:20"
            assert "Crazytown" not in html
            assert "fielded_100" not in html

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "SPORE-1.0" in readme
    assert "RE-COLD-STORE" in readme
    assert SOT_URL in readme
    assert RUNTIME_VERSION_ID in readme
    assert RUNTIME_GIT_SHORT in readme
    assert "Zioncheck archive" in readme

    print("spore hub cite OK")
    print("sot", SOT_URL)
    print("worker", RUNTIME_VERSION_ID)
    print("git", RUNTIME_GIT_SHORT)
    print("ingest_tip", HDJ_INGEST_TIP)


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print("FAIL", exc, file=sys.stderr)
        raise
