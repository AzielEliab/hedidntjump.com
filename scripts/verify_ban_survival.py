#!/usr/bin/env python3
"""Assert HDJ BAN-SURVIVAL hub pull stays honest and archive-focused."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from write_ban_survival import (  # noqa: E402
    APEX,
    AZNET_SIDE,
    CAP7_URL,
    HDJ_INGEST_TIP,
    LAMB_LENS,
    LIVE_DOOR_IDS,
    MIRAGE_WORKER,
    PERSON_ID,
    PUBLIC_PAIR,
    SOT_URL,
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


def check_wrap(payload: dict, label: str) -> None:
    assert payload["spec"] == "BAN-SURVIVAL-1.0", label
    assert payload["author"] == "Aziel Eliab", label
    assert payload["identity"] == "Aziel Eliab", label
    assert payload["person_id"] == PERSON_ID, label
    assert payload["visible_1520"] is False, label
    assert payload["softwares_clone"] is False, label
    assert payload["softwares_tab"] is False, label
    assert payload["this_host_is_live_door"] is False, label
    assert payload["this_host_runtime_front"] is False, label
    assert payload["mission"] == "Zioncheck archive", label
    assert payload["invented_case_facts"] is False, label
    assert payload["mutual_backup"] is True, label
    assert payload["ttl_seconds"] == TTL_SECONDS, label
    assert payload["sot"] == SOT_URL, label
    assert payload["no_lie"].startswith("NO-LIE"), label
    assert payload["lamb_lens"]["shelf"] == LAMB_LENS, label
    assert "azielcorpuslibrary.net" in payload["lamb_lens"]["note"], label
    assert "not a Lamb Lens ingest host" not in payload["lamb_lens"]["note"], label
    ids = list(payload["live_door_ids"])
    assert tuple(ids) == LIVE_DOOR_IDS, ids
    assert "hedidntjump" not in "".join(ids), label
    assert payload["platforms"]["all_live"] is True, label
    assert payload["platforms"]["native_app_store"] is False, label
    calling = payload["calling_name"]
    assert calling["identity"] == "Aziel Eliab", label
    assert calling["identity_unchanged"] is True, label
    assert calling["calling_name"], label
    cap7 = payload["cap7_aznet"]
    assert cap7["resolves_to_hub"] is False, label
    assert cap7["public_icann"] is False, label
    assert cap7["factory"] == "miragegrid", label
    assert cap7["hosted_endpoints"] == "slot", label
    grid = payload["miragegrid_worker"]
    assert grid["url"] == MIRAGE_WORKER, label
    assert grid["bridge"] == CAP7_URL, label
    assert grid["resolves_to_hub"] is False, label
    assert grid["public_icann"] is False, label
    assert grid["hdj_design_site"] == "azshift", label
    assert list(grid["public_pair"]) == list(PUBLIC_PAIR), label
    assert list(grid["aznet_side"]) == list(AZNET_SIDE), label
    assert grid["azshift"]["resolves_to_hub"] is False, label
    assert grid["azshift"]["honesty_public"] == "SLOT", label
    assert "hedidntjump.com" in grid["azshift"]["design_of"], label
    assert payload["ingest_tip_unchanged"] == HDJ_INGEST_TIP, label
    assert payload["spore_spec"] == "SPORE-1.0", label
    assert payload["spore_replaces_cold_shelves"] is False, label
    assert payload["re_cold_store"]["hook"] == "RE-COLD-STORE", label
    assert payload["re_cold_store"]["destinations"] == [], label
    assert payload["re_cold_store"]["invent_destination"] is False, label
    assert payload["spore"]["spec"] == "SPORE-1.0", label
    assert payload["spore"]["software_tab"] is False, label
    ids = [row["id"] for row in payload["survival_stack"]]
    assert ids == ["live-fronts", "cold-shelves", "spore"], ids


def main() -> None:
    ingest_expected = (ROOT / "docs" / "ingest-as-receipt.json").read_bytes()
    assert hashlib.sha256(ingest_expected).hexdigest() == HDJ_INGEST_TIP

    pull = (ROOT / "functions" / "_lib" / "survival-pull.js").read_text(encoding="utf-8")
    assert SOT_URL in pull
    assert CAP7_URL in pull
    assert PERSON_ID in pull
    assert f"const TTL = {TTL_SECONDS}" in pull
    assert "max-age=${TTL}" in pull
    assert "this_host_is_live_door: false" in pull
    assert "Zioncheck stays the mission" in pull
    assert (ROOT / "functions" / "survival.js").is_file()
    assert (ROOT / "functions" / "v1" / "survival.js").is_file()

    for tree_name in ("docs", "dist"):
        tree = ROOT / tree_name
        raw = (tree / "survival.json").read_text(encoding="utf-8")
        payload = json.loads(raw)
        check_wrap(payload, f"{tree_name}/survival.json")
        assert raw.endswith("\n")

        cite = json.loads((tree / "cite.json").read_text(encoding="utf-8"))
        check_wrap(cite["ban_survival"], f"{tree_name}/cite.ban_survival")
        assert cite["person_id"] == PERSON_ID
        assert cite["identity"] == "Aziel Eliab"
        assert cite["visible_1520"] is False
        assert cite["about"] == "Marion A. Zioncheck archive"
        assert "Marion A. Zioncheck" in cite["purpose"]
        assert "does not invent" in cite["purpose"].lower() or "re-examines" in cite["purpose"]
        assert cite["ingest_as_receipt"]["tip"] == HDJ_INGEST_TIP
        for u in (f"{APEX}/survival", f"{APEX}/survival.json", f"{WWW}/survival"):
            assert u in cite["query_urls"], u

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
            assert "BAN-SURVIVAL-1.0" in blob, label
            assert SOT_URL in blob, label
            assert MIRAGE_WORKER in blob, label
            assert "mutual backup" in blob.lower() or "Mutual backup" in blob, label
            assert "Aziel Runtime" in blob, label
            assert "resolves_to_hub" in blob, label
            assert PERSON_ID in blob, label
            assert "NO-LIE" in blob, label
            assert "Lamb Lens" in blob, label
            assert "Zioncheck" in blob, label
            assert "Marion Zioncheck" in blob or "Zioncheck" in blob, label
            assert "Not a Softwares clone" not in blob, label
            assert "azshift" in blob, label
            for forged in FORGED:
                if forged in ("Pg. 11",):
                    continue
                assert forged not in blob, f"{label} invented {forged}"

        lead = llms.split("## Marion")[0]
        assert f"{APEX}/survival" in lead

        openapi = json.loads((tree / "openapi.json").read_text(encoding="utf-8"))
        assert "/survival" in openapi["paths"]
        assert "/survival.json" in openapi["paths"]
        assert "/v1/survival" in openapi["paths"]
        assert "Zioncheck archive hub pull" in openapi["paths"]["/survival"]["get"]["summary"]
        assert "not a live exec door" not in openapi["paths"]["/survival"]["get"]["summary"]

        headers = (tree / "_headers").read_text(encoding="utf-8")
        assert "/survival.json" in headers
        assert f"max-age={TTL_SECONDS}" in headers
        redirects = (tree / "_redirects").read_text(encoding="utf-8")
        assert "/survival /survival.json 200" in redirects
        assert "/v1/survival /survival.json 200" in redirects
        sitemap = (tree / "sitemap.xml").read_text(encoding="utf-8")
        assert f"{APEX}/survival</loc>" in sitemap
        assert f"{APEX}/survival.json</loc>" in sitemap
        robots = (tree / "robots.txt").read_text(encoding="utf-8")
        assert "Allow: /survival" in robots
        assert "Allow: /survival.json" in robots

        wk = json.loads((tree / ".well-known" / "aziel.json").read_text(encoding="utf-8"))
        assert wk["ban_survival"]["spec"] == "BAN-SURVIVAL-1.0"
        assert wk["ban_survival"]["mutual_backup"] is True
        assert wk["ban_survival"]["platforms_all_live"] is True
        assert wk["ban_survival"]["cap7_resolves_to_hub"] is False
        assert wk["ban_survival"]["this_host_is_live_door"] is False
        assert wk["ban_survival"]["mission"] == "Zioncheck archive"
        assert wk["ban_survival"]["person_id"] == PERSON_ID
        assert wk["person_id"] == PERSON_ID
        assert "Marion Zioncheck" in wk["mission"]

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
    assert "BAN-SURVIVAL-1.0" in readme
    assert SOT_URL in readme
    assert MIRAGE_WORKER in readme
    assert "Zioncheck archive" in readme

    print("ban-survival hub pull OK")
    print("sot", SOT_URL)
    print("cap7", MIRAGE_WORKER)
    print("ttl", TTL_SECONDS)
    print("ingest_tip", HDJ_INGEST_TIP)


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print("FAIL", exc, file=sys.stderr)
        raise
