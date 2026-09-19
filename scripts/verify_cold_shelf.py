#!/usr/bin/env python3
"""Assert HDJ COLD-MULTI-SHELF-1.0 AZindex parity with live corpus /shelves."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from write_cold_shelf import (
    ARCHIVE_ORG_202609_DOWNLOAD,
    ARCHIVE_ORG_202609_IDENTIFIER,
    ARCHIVE_ORG_202609_ITEM,
    ARCHIVE_ORG_202609_URL,
    ARCHIVE_ORG_202609_ZIP,
    ARCHIVE_ORG_202609_ZIP_ALT,
    ARCHIVE_ORG_DOWNLOAD,
    ARCHIVE_ORG_IDENTIFIER,
    ARCHIVE_ORG_ITEM,
    ARCHIVE_ORG_URL,
    CANON_SHELVES,
    CAP7,
    CODEBERG_PACK,
    FOLDLOCK_DIGEST,
    FOLDLOCK_REDLINE,
    HDJ_INGEST_TIP,
    LOCKSET_TIP,
    PERSON_ID,
    PLANE_B_TARGETS,
    dumps,
    foldlock_cite,
    lockset_doc,
    redline_cite,
    shelves_doc,
)
from write_ingest_as_receipt import FILENAME, PAYLOAD, dumps as ingest_dumps

APEX = "https://hedidntjump.com"
WWW = "https://www.hedidntjump.com"
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


FORGED = {
    "working_targets_gitflic": ["codeberg", "archive.org", "gitflic-ru"],
    "framagit_url": "https://framagit.org/AzielEliab/aziel-lockset-tip",
    "gitflic_url": "https://gitflic.ru/project/azieeliab/aziel-lockset-tip",
    "gitlab_url": "https://gitlab.com/AzielEliab/aziel-lockset-tip",
    "zenodo_doi": "10.5281/zenodo.99999999",
    "plane_b_live": "live",
    "cap7_hub": True,
    "fold_tip": True,
}


def walk_urls(obj) -> list[str]:
    found = []
    if isinstance(obj, dict):
        for value in obj.values():
            found.extend(walk_urls(value))
    elif isinstance(obj, list):
        for value in obj:
            found.extend(walk_urls(value))
    elif isinstance(obj, str) and obj.startswith("http"):
        found.append(obj)
    return found


def attack_sim(shelves: dict, cite: dict, redline: dict, lockset: dict) -> None:
    """Attack-sim: forged promotions and invented holdings must not land."""
    plane_b = shelves["planes"]["B"]
    assert plane_b["working_targets"] == PLANE_B_TARGETS
    assert plane_b["working_targets"] != FORGED["working_targets_gitflic"]
    assert "gitflic-ru" not in plane_b["working_targets"]
    assert "gitlab" not in plane_b["working_targets"]
    assert plane_b["status"] == "slot"
    assert plane_b["status"] != FORGED["plane_b_live"]
    assert plane_b["live_ready"] is False
    assert plane_b["third_target"]["forge"] == "framagit"
    assert plane_b["third_target"]["url"] is None
    assert plane_b["third_target"]["url"] != FORGED["framagit_url"]
    assert plane_b["framagit_tip_pack"]["url"] is None
    assert plane_b["archive_org_tip_pack_202609"]["independent"] is False
    assert plane_b["archive_org_tip_pack_202609"]["status"] == "slot"
    assert plane_b["archive_org_tip_pack_202609"]["live_ready"] is False
    assert plane_b["working_targets"].count("archive.org") == 1
    assert plane_b["gitflic"]["refuse"] == "CNS-GITFLIC-EMAIL"
    assert plane_b["gitflic"]["url"] is None
    assert plane_b["gitflic"]["status"] == "refused"
    assert plane_b["gitlab"]["refuse"] == "CNS-GITLAB-CF-LOOP"
    assert plane_b["gitlab"]["url"] is None
    assert plane_b["gitlab"]["required_for_plane_b_live"] is False

    rows = {row["id"]: row for row in shelves["registry"]["shelves"]}
    archive_202609 = rows["plane-b-archive-org-tip-pack-202609"]
    assert archive_202609["url"] == ARCHIVE_ORG_202609_URL
    assert archive_202609["independent"] is False
    assert archive_202609["status"] == "slot"
    assert archive_202609["live_ready"] is False
    assert archive_202609["doi"] is None
    assert archive_202609["pack_sha256"] == CODEBERG_PACK
    framagit = rows["plane-b-framagit-tip-pack"]
    assert framagit["url"] is None
    assert framagit["url"] != FORGED["framagit_url"]
    assert framagit["status"] == "slot"
    assert framagit["live_ready"] is False
    assert framagit["required_for_plane_b_live"] is True
    gitflic = rows["plane-b-gitflic-ru-tip-pack"]
    assert gitflic["status"] == "refused"
    assert gitflic["status"] != "slot"
    assert gitflic["url"] is None
    assert gitflic["url"] != FORGED["gitflic_url"]
    assert gitflic["refuse"] == "CNS-GITFLIC-EMAIL"
    gitlab = rows["plane-g-gitlab-tip-pack"]
    assert gitlab["url"] is None
    assert gitlab["url"] != FORGED["gitlab_url"]
    assert gitlab["refuse"] == "CNS-GITLAB-CF-LOOP"
    assert gitlab["required_for_plane_b_live"] is False
    zenodo = rows["plane-b-zenodo-tip-pack"]
    assert zenodo["status"] == "refused"
    assert zenodo["doi"] is None
    assert zenodo["doi"] != FORGED["zenodo_doi"]

    assert "plane-b-framagit-tip-pack" in shelves["registry"]["slot"]
    assert "plane-b-gitflic-ru-tip-pack" in shelves["registry"]["refused"]
    assert "plane-b-gitflic-ru-tip-pack" not in shelves["registry"]["slot"]
    assert "plane-b-zenodo-tip-pack" in shelves["registry"]["refused"]

    for site, row in shelves["cap7_sites"].items():
        assert row["resolves_to_hub"] is False
        assert row["resolves_to_hub"] != FORGED["cap7_hub"]
        assert row["design_of"]
        assert CAP7[site]["design_of"] == row["design_of"]
        assert row["public_icann"] is False

    fold = shelves["foldlock"]
    assert fold["tip_folded"] is False
    assert fold["tip_folded"] != FORGED["fold_tip"]
    assert fold["engine_bound"] is False
    assert fold["hdj_holding"] is False
    assert fold["zip"] is False
    assert fold["encryption"] is False
    assert fold["digest"] == FOLDLOCK_DIGEST
    assert fold["redline"] == FOLDLOCK_REDLINE
    assert fold["refuse"]["TIP_FOLD"] == "FL-TIP-FOLD-REFUSE"
    assert lockset["foldlock"]["tip_folded"] is False
    assert lockset["sha256"] == LOCKSET_TIP
    assert "FL-TIP-FOLD-REFUSE" in lockset["note"]

    assert redline["door"] == "fraggate"
    assert redline["doors"]["fraggate_single_door"] is True
    assert redline["doors"]["domains_are_doors"] is False
    assert redline["doors"]["this_host_mcp"] is False
    assert redline["refuse"]["GITFLIC"] == "CNS-GITFLIC-EMAIL"
    assert redline["refuse"]["GITLAB"] == "CNS-GITLAB-CF-LOOP"
    assert redline["refuse"]["ZENODO"] == "CNS-ZENODO-IP-BAN"
    assert redline["refuse"]["TIP_FOLD"] == "FL-TIP-FOLD-REFUSE"
    assert redline["plane_b"]["working_targets"] == PLANE_B_TARGETS
    assert redline["plane_b"]["framagit_url"] is None
    assert redline["invented_holdings"] is False
    assert redline["growth_on"] is True
    assert redline["cap7"]["resolves_to_hub"] is False

    assert cite["planes"]["B"]["working_targets"] == PLANE_B_TARGETS
    assert cite["framagit_tip_pack"]["url"] is None
    assert "refuse" not in cite.get("gitflic_tip_pack", {})
    assert "refuse" not in cite.get("gitlab_tip_pack", {})
    assert cite["zenodo_tip_pack"]["doi"] is None
    assert cite["redline"]["door"] == "fraggate"
    assert cite["foldlock"]["tip_folded"] is False

    banned_hosts = (
        "framagit.org",
        "gitflic.ru",
        "gitlab.com",
        "gitlab.org",
    )
    for url in walk_urls(shelves) + walk_urls(cite) + walk_urls(redline):
        assert not any(host in url for host in banned_hosts), url
        assert FORGED["zenodo_doi"] not in url

    for dep in shelves["registry"]["corpus_paper_deposits"]:
        assert dep["hdj_holding"] is False
        assert dep["reuse_as_plane_b"] is False

    assert shelves["invented_framagit_url"] is False
    assert shelves["invented_gitflic_url"] is False
    assert shelves["invented_gitlab_url"] is False
    assert shelves["invented_zenodo_doi"] is False
    assert shelves["no_invented_holdings"] is True


def visible_text(html: str) -> str:
    html = re.sub(r"<script\b[^>]*>[\s\S]*?</script>", " ", html, flags=re.I)
    html = re.sub(r"<style\b[^>]*>[\s\S]*?</style>", " ", html, flags=re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    return html


def main() -> None:
    expected_shelves = dumps(shelves_doc())
    expected_lockset = dumps(lockset_doc())
    ingest_expected = ingest_dumps(PAYLOAD)
    ingest_tip = hashlib.sha256(ingest_expected.encode("utf-8")).hexdigest()
    assert ingest_tip == HDJ_INGEST_TIP

    for tree_name in ("docs", "dist"):
        tree = ROOT / tree_name
        for name in ("shelves.json", "shelves", "cold-copy", "v1/shelves"):
            raw = (tree / name).read_text(encoding="utf-8")
            assert raw == expected_shelves, f"{tree_name}/{name} drifted from writer"

        lock = (tree / "lockset.json").read_text(encoding="utf-8")
        assert lock == expected_lockset
        lock_j = json.loads(lock)
        expected_redline = dumps(redline_cite())
        assert (tree / "redline.json").read_text(encoding="utf-8") == expected_redline
        assert (tree / "redline").read_text(encoding="utf-8") == expected_redline
        redline = json.loads(expected_redline)
        assert foldlock_cite()["digest"] == FOLDLOCK_DIGEST
        assert lock_j["doi"] is None
        assert lock_j["zenodo"] is None
        assert lock_j["sha256"] == LOCKSET_TIP
        assert lock_j["canonical"] == "https://www.azielcorpuslibrary.net/lockset.json"
        assert lock_j["person_id"] == PERSON_ID

        shelves = json.loads(expected_shelves)
        assert shelves["spec"] == "COLD-MULTI-SHELF-1.0"
        assert shelves["canonical"] == CANON_SHELVES
        assert shelves["person_id"] == PERSON_ID
        assert shelves["doi"] is None
        assert shelves["zenodo_status"] == "CNS-ZENODO-IP-BAN"
        assert shelves["visible_1520"] is False
        assert shelves["growth_on"] is True
        assert shelves["no_fan"] is True
        assert shelves["softwares_tab"] is False
        assert shelves["mesh_radio"] is False
        assert shelves["az_gen_live_icann_publish"] is False
        assert shelves["planes"]["A"]["published_surfaces"] == 5
        assert shelves["planes"]["A"]["family_blast_radii"] == ["cloudflare", "github"]
        assert shelves["planes"]["B"]["status"] == "slot"
        assert shelves["planes"]["B"]["doi"] is None
        assert shelves["planes"]["B"]["working_targets"] == PLANE_B_TARGETS
        assert shelves["planes"]["B"]["refuse"] == "CNS-ZENODO-IP-BAN"
        assert shelves["planes"]["B"]["codeberg_tip_pack"]["pack_sha256"] == CODEBERG_PACK
        assert shelves["planes"]["B"]["codeberg_tip_pack"]["hash_verify"] == "pass"
        assert shelves["planes"]["B"]["codeberg_tip_pack"]["status"] == "slot"
        assert shelves["planes"]["B"]["archive_org_tip_pack"]["url"] == ARCHIVE_ORG_URL
        assert shelves["planes"]["B"]["archive_org_tip_pack"]["identifier"] == ARCHIVE_ORG_IDENTIFIER
        assert shelves["planes"]["B"]["archive_org_tip_pack"]["item"] == ARCHIVE_ORG_ITEM
        assert shelves["planes"]["B"]["archive_org_tip_pack"]["download_base"] == ARCHIVE_ORG_DOWNLOAD
        assert shelves["planes"]["B"]["archive_org_tip_pack"]["pack_sha256"] == CODEBERG_PACK
        assert shelves["planes"]["B"]["archive_org_tip_pack"]["hash_verify"] == "pass"
        assert shelves["planes"]["B"]["archive_org_tip_pack"]["status"] == "slot"
        assert shelves["planes"]["B"]["archive_org_tip_pack"]["live_ready"] is False
        sec = shelves["planes"]["B"]["archive_org_tip_pack"]["secondary_items"]
        assert len(sec) == 1
        assert sec[0]["id"] == "plane-b-archive-org-tip-pack-202609"
        assert sec[0]["url"] == ARCHIVE_ORG_202609_URL
        assert sec[0]["identifier"] == ARCHIVE_ORG_202609_IDENTIFIER
        assert sec[0]["item"] == ARCHIVE_ORG_202609_ITEM
        assert sec[0]["download_base"] == ARCHIVE_ORG_202609_DOWNLOAD
        assert sec[0]["zip"] == ARCHIVE_ORG_202609_ZIP
        assert sec[0]["zip_alt"] == ARCHIVE_ORG_202609_ZIP_ALT
        assert sec[0]["wrap"] == "zip"
        assert sec[0]["ia_flat_sha256"] is None
        assert sec[0]["sha256sums_flat_check"] == "incomplete"
        assert sec[0]["inner_pack"] == "aziel-tip-pack.tar"
        assert sec[0]["pack_sha256"] == CODEBERG_PACK
        assert sec[0]["hash_verify"] == "pass"
        assert sec[0]["same_blast_radius"] == "archive-org"
        assert sec[0]["independent_shelf"] is False
        pack_202609 = shelves["planes"]["B"]["archive_org_tip_pack_202609"]
        assert pack_202609["url"] == ARCHIVE_ORG_202609_URL
        assert pack_202609["identifier"] == ARCHIVE_ORG_202609_IDENTIFIER
        assert pack_202609["pack_sha256"] == CODEBERG_PACK
        assert pack_202609["hash_verify"] == "pass"
        assert pack_202609["status"] == "slot"
        assert pack_202609["live_ready"] is False
        assert pack_202609["independent"] is False
        assert pack_202609["same_blast_radius"] == "archive-org"
        assert pack_202609["same_pack_as"] == "plane-b-archive-org-tip-pack"
        assert pack_202609["required_for_plane_b_live"] is False
        assert pack_202609["doi"] is None
        assert shelves["planes"]["B"]["working_targets"].count("archive.org") == 1
        assert "aziel-lockset-tip_202609" in shelves["planes"]["B"]["note"]
        assert "not a second independent shelf" in shelves["planes"]["B"]["note"]
        assert "archive.org + GitFlic" not in shelves["planes"]["B"]["note"]
        assert "GitFlic RU unverified" not in shelves["planes"]["B"]["note"]
        assert "framagit" in shelves["planes"]["B"]["working_targets"]
        assert "CNS-GITFLIC-EMAIL" in shelves["planes"]["B"]["note"]
        assert "CNS-GITLAB-CF-LOOP" in shelves["planes"]["B"]["note"]
        assert "Framagit" in shelves["planes"]["B"]["note"]
        assert shelves["planes"]["C"]["status"] == "slot"
        assert "CNS-OPERATOR-ATTEST" in shelves["planes"]["C"]["refuse"]
        assert shelves["this_host"]["mission"].startswith("He Didn't Jump")
        assert "does not invent court holdings" in shelves["this_host"]["mission"].lower()
        assert shelves["lamb_lens"]["shelf"] == "https://www.azielcorpuslibrary.net/corpus" if "lamb_lens" in shelves else True
        assert shelves["this_host"]["lamb_lens"]["shelf"] == "https://www.azielcorpuslibrary.net/corpus"
        assert shelves["registry"]["independent_live_count"] == 1
        assert not shelves["registry"]["independent_requirement_met"]
        assert "plane-b-archive-org-tip-pack-202609" in shelves["registry"]["slot"]
        assert "plane-b-archive-org-tip-pack-202609" not in shelves["registry"]["live"]
        assert ARCHIVE_ORG_202609_URL in shelves["registry"]["note"]
        assert "Not two independent shelves" in shelves["registry"]["note"]
        for dep in shelves["registry"]["corpus_paper_deposits"]:
            assert dep["hdj_holding"] is False
            assert dep["reuse_as_plane_b"] is False
        zenodo = next(s for s in shelves["registry"]["shelves"] if s["id"] == "plane-b-zenodo-tip-pack")
        assert zenodo["status"] == "refused"
        assert zenodo["doi"] is None
        codeberg = next(s for s in shelves["registry"]["shelves"] if s["id"] == "plane-b-codeberg-tip-pack")
        assert codeberg["pack_sha256"] == CODEBERG_PACK
        assert codeberg["status"] == "slot"
        assert codeberg["hash_verify"] == "pass"
        archive = next(s for s in shelves["registry"]["shelves"] if s["id"] == "plane-b-archive-org-tip-pack")
        assert archive["url"] == ARCHIVE_ORG_URL
        assert archive["identifier"] == ARCHIVE_ORG_IDENTIFIER
        assert archive["item"] == ARCHIVE_ORG_ITEM
        assert archive["download_base"] == ARCHIVE_ORG_DOWNLOAD
        assert archive["pack_sha256"] == CODEBERG_PACK
        assert archive["hash_verify"] == "pass"
        assert archive["status"] == "slot"
        assert archive["live_ready"] is False
        assert archive["doi"] is None
        assert archive["independent"] is True
        assert archive["refuse"] == "CNS-PLANE-B-ALL-TARGETS"
        assert archive.get("refuse") != "CNS-NO-WARC"
        assert archive["status"] != "live"
        assert archive["secondary_items"][0]["url"] == ARCHIVE_ORG_202609_URL
        assert archive["secondary_items"][0]["independent_shelf"] is False
        archive_202609 = next(
            s for s in shelves["registry"]["shelves"] if s["id"] == "plane-b-archive-org-tip-pack-202609"
        )
        assert archive_202609["url"] == ARCHIVE_ORG_202609_URL
        assert archive_202609["identifier"] == ARCHIVE_ORG_202609_IDENTIFIER
        assert archive_202609["item"] == ARCHIVE_ORG_202609_ITEM
        assert archive_202609["download_base"] == ARCHIVE_ORG_202609_DOWNLOAD
        assert archive_202609["zip"] == ARCHIVE_ORG_202609_ZIP
        assert archive_202609["zip_alt"] == ARCHIVE_ORG_202609_ZIP_ALT
        assert archive_202609["wrap"] == "zip"
        assert archive_202609["ia_flat_sha256"] is None
        assert archive_202609["sha256sums_flat_check"] == "incomplete"
        assert archive_202609["inner_pack"] == "aziel-tip-pack.tar"
        assert archive_202609["pack_sha256"] == CODEBERG_PACK
        assert archive_202609["hash_verify"] == "pass"
        assert archive_202609["status"] == "slot"
        assert archive_202609["live_ready"] is False
        assert archive_202609["independent"] is False
        assert archive_202609["blast_radius"] == "archive-org"
        assert archive_202609["same_pack_as"] == "plane-b-archive-org-tip-pack"
        assert archive_202609["required_for_plane_b_live"] is False
        assert archive_202609["doi"] is None
        assert archive_202609["refuse"] == "CNS-PLANE-B-ALL-TARGETS"
        assert archive_202609["status"] != "live"
        gitflic = next(s for s in shelves["registry"]["shelves"] if s["id"] == "plane-b-gitflic-ru-tip-pack")
        assert gitflic["url"] is None
        assert gitflic["status"] == "refused"
        assert gitflic["refuse"] == "CNS-GITFLIC-EMAIL"
        usb = next(s for s in shelves["registry"]["shelves"] if s["id"] == "plane-c-usb-airgap")
        assert usb["status"] == "slot"
        assert usb["refuse"] == "CNS-OPERATOR-ATTEST"

        for site, row in shelves["cap7_sites"].items():
            assert row["design_of"]
            assert row["resolves_to_hub"] is False
            assert CAP7[site]["design_of"] == row["design_of"]
        assert shelves["cap7_sites"]["hedidntjump"]["design_of"] == f"{WWW}/"

        cite = json.loads((tree / "cite.json").read_text(encoding="utf-8"))
        assert cite["person_id"] == PERSON_ID
        assert cite["author_id"] == PERSON_ID
        assert cite["cold_multi_shelf"] == "COLD-MULTI-SHELF-1.0"
        assert cite["shelves_canonical"] == CANON_SHELVES
        assert cite["lockset_tip"] == LOCKSET_TIP
        assert cite["lockset_doi"] is None
        assert cite["doi"] is None
        assert cite["growth_on"] is True
        assert cite["no_fan"] is True
        assert cite["visible_1520"] is False
        assert cite["published_surfaces"] == 5
        assert cite["family_blast_radii"] == ["cloudflare", "github"]
        assert cite["independent_live_count"] == 1
        assert cite["planes"]["B"]["codeberg_tip_pack"]["pack_sha256"] == CODEBERG_PACK
        assert cite["planes"]["B"]["archive_org_tip_pack"]["url"] == ARCHIVE_ORG_URL
        assert cite["planes"]["B"]["archive_org_tip_pack"]["identifier"] == ARCHIVE_ORG_IDENTIFIER
        assert cite["planes"]["B"]["archive_org_tip_pack"]["hash_verify"] == "pass"
        assert cite["planes"]["B"]["archive_org_tip_pack"]["status"] == "slot"
        assert cite["planes"]["B"]["archive_org_tip_pack"]["secondary_items"][0]["url"] == ARCHIVE_ORG_202609_URL
        assert cite["planes"]["B"]["archive_org_tip_pack_202609"]["url"] == ARCHIVE_ORG_202609_URL
        assert cite["planes"]["B"]["archive_org_tip_pack_202609"]["independent"] is False
        assert cite["planes"]["B"]["archive_org_tip_pack_202609"]["hash_verify"] == "pass"
        assert cite["planes"]["B"]["archive_org_tip_pack_202609"]["status"] == "slot"
        assert cite["planes"]["B"]["working_targets"].count("archive.org") == 1
        assert "aziel-lockset-tip_202609" in cite["planes"]["B"]["note"]
        assert "archive.org + GitFlic" not in cite["planes"]["B"]["note"]
        assert cite["planes"]["B"]["working_targets"] == PLANE_B_TARGETS
        assert "aziel-lockset-tip" in cite["planes"]["B"]["note"]
        assert "CNS-GITFLIC-EMAIL" not in cite["planes"]["B"]["note"]
        assert cite["framagit_tip_pack"]["url"] is None
        assert "refuse" not in cite.get("gitflic_tip_pack", {})
        assert "refuse" not in cite.get("gitlab_tip_pack", {})
        assert cite["archive_org_tip_pack"]["url"] == ARCHIVE_ORG_URL
        assert cite["archive_org_tip_pack"]["identifier"] == ARCHIVE_ORG_IDENTIFIER
        assert cite["archive_org_tip_pack"]["download_base"] == ARCHIVE_ORG_DOWNLOAD
        assert cite["archive_org_tip_pack"]["hash_verify"] == "pass"
        assert cite["archive_org_tip_pack"]["status"] == "slot"
        assert cite["archive_org_tip_pack"]["secondary_items"][0]["url"] == ARCHIVE_ORG_202609_URL
        assert cite["archive_org_tip_pack_202609"]["url"] == ARCHIVE_ORG_202609_URL
        assert cite["archive_org_tip_pack_202609"]["identifier"] == ARCHIVE_ORG_202609_IDENTIFIER
        assert cite["archive_org_tip_pack_202609"]["pack_sha256"] == CODEBERG_PACK
        assert cite["archive_org_tip_pack_202609"]["hash_verify"] == "pass"
        assert cite["archive_org_tip_pack_202609"]["status"] == "slot"
        assert cite["archive_org_tip_pack_202609"]["independent"] is False
        assert cite["archive_org_tip_pack_202609"]["doi"] is None
        assert cite["archive_org_tip_packs"] == [ARCHIVE_ORG_URL, ARCHIVE_ORG_202609_URL]
        assert "refuse" not in cite.get("zenodo_tip_pack", {})
        assert cite["zenodo_tip_pack"]["doi"] is None
        assert cite["cap7_sites"]["hedidntjump"]["resolves_to_hub"] is False
        assert cite["lamb_lens"]["shelf"] == "https://www.azielcorpuslibrary.net/corpus"
        assert cite["ingest_as_receipt"]["tip"] == HDJ_INGEST_TIP
        assert cite["purpose"].startswith("Marion A. Zioncheck archive")
        assert f"{APEX}/shelves" in cite["query_urls"]
        assert f"{APEX}/redline" in cite["query_urls"]
        assert "does not invent court holdings" in cite["purpose"].lower() or "re-examine" in cite["purpose"]
        attack_sim(shelves, cite, redline, lock_j)

        hashed = (tree / FILENAME).read_text(encoding="utf-8")
        assert hashed == ingest_expected
        assert "COLD-MULTI-SHELF" not in hashed
        assert hashlib.sha256(hashed.encode("utf-8")).hexdigest() == HDJ_INGEST_TIP

        llms = (tree / "llms.txt").read_text(encoding="utf-8")
        lead = llms.split("## Marion")[0]
        assert f"{APEX}/shelves" in lead
        llms_full = (tree / "llms-full.txt").read_text(encoding="utf-8")
        ai = (tree / "ai.txt").read_text(encoding="utf-8")
        for blob, label in ((llms, "llms"), (llms_full, "llms-full"), (ai, "ai")):
            assert "COLD-MULTI-SHELF-1.0" in blob, label
            assert CANON_SHELVES in blob, label
            assert PERSON_ID in blob, label
            assert CODEBERG_PACK in blob, label
            assert ARCHIVE_ORG_URL in blob, label
            assert ARCHIVE_ORG_202609_URL in blob, label
            assert "same blast_radius" in blob, label
            assert "archive.org + GitFlic" not in blob, label
            assert "GitFlic RU unverified" not in blob, label
            assert "Framagit" in blob, label
            assert "CNS-GITFLIC-EMAIL" not in blob, label
            assert "CNS-GITLAB-CF-LOOP" not in blob, label
            assert "ALL-TARGETS" in blob or "working_targets" in blob or "Framagit" in blob, label
            assert "CNS-ZENODO-IP-BAN" not in blob, label
            assert "doi null" in blob.lower() or "doi: null" in blob.lower() or "doi null" in blob, label
            assert "CNS-OPERATOR-ATTEST" in blob or "attest SLOT" in blob or "USB" in blob, label
            assert "5 surfaces" in blob or "5 published surfaces" in blob, label
            assert "2 family radii" in blob or "2 radii" in blob, label
            assert "Lamb Lens" in blob, label
            assert "Growth-ON" in blob or "growth_on" in blob, label
            assert "NO-FAN" in blob, label
            assert "Marion" in blob or "Zioncheck" in blob, label
            assert "holdings" in blob.lower(), label

        headers = (tree / "_headers").read_text(encoding="utf-8")
        for loc in (
            "/shelves",
            "/shelves.json",
            "/lockset.json",
            "/v1/shelves",
            "/cold-copy",
            "/redline",
            "/redline.json",
        ):
            assert loc in headers, loc
        redirects = (tree / "_redirects").read_text(encoding="utf-8")
        assert "/shelves /shelves.json 200" in redirects
        assert "/redline /redline.json 200" in redirects
        sitemap = (tree / "sitemap.xml").read_text(encoding="utf-8")
        assert f"{APEX}/shelves</loc>" in sitemap
        assert f"{APEX}/lockset.json</loc>" in sitemap
        assert f"{APEX}/redline</loc>" in sitemap
        openapi = json.loads((tree / "openapi.json").read_text(encoding="utf-8"))
        assert "/shelves" in openapi["paths"]
        assert "/lockset.json" in openapi["paths"]
        assert "/redline" in openapi["paths"]
        robots = (tree / "robots.txt").read_text(encoding="utf-8")
        assert "Growth-ON" in robots
        assert "Allow: /shelves" in robots
        assert "Allow: /redline" in robots
        assert "GPTBot" in robots and "Disallow: /api/" in robots

        for name in PAPER_HTML:
            html = (tree / name).read_text(encoding="utf-8")
            visible = visible_text(html)
            assert "lock-1520" not in html
            assert "visible-1520" not in html
            assert 'id="verse-lock"' not in html
            nav = re.search(r'<nav class="paper-tabs"[\s\S]*?</nav>', html)
            if nav:
                assert "Shelves" not in nav.group(0), f"{tree_name}/{name} paper-tabs gained Shelves"
                assert "15:20" not in nav.group(0)
                assert "Pg. 11" not in nav.group(0)
            if name != "who.html":
                assert "15:20" not in visible, f"{tree_name}/{name} gained visible 15:20"

    print("cold-shelf AZindex OK")
    print("lockset_tip", LOCKSET_TIP)
    print("codeberg_pack", CODEBERG_PACK)
    print("hdj_ingest_tip", HDJ_INGEST_TIP)


if __name__ == "__main__":
    main()
