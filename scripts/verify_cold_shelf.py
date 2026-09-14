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
    ARCHIVE_ORG_URL,
    CANON_SHELVES,
    CAP7,
    CODEBERG_PACK,
    HDJ_INGEST_TIP,
    LOCKSET_TIP,
    PERSON_ID,
    dumps,
    lockset_doc,
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
        assert shelves["planes"]["B"]["refuse"] == "CNS-ZENODO-IP-BAN"
        assert shelves["planes"]["B"]["codeberg_tip_pack"]["pack_sha256"] == CODEBERG_PACK
        assert shelves["planes"]["B"]["codeberg_tip_pack"]["hash_verify"] == "pass"
        assert shelves["planes"]["B"]["codeberg_tip_pack"]["status"] == "slot"
        assert shelves["planes"]["B"]["archive_org_tip_pack"]["url"] == ARCHIVE_ORG_URL
        assert shelves["planes"]["B"]["archive_org_tip_pack"]["pack_sha256"] == CODEBERG_PACK
        assert shelves["planes"]["B"]["archive_org_tip_pack"]["hash_verify"] == "pass"
        assert shelves["planes"]["B"]["archive_org_tip_pack"]["status"] == "slot"
        assert "archive.org + GitFlic" not in shelves["planes"]["B"]["note"]
        assert "GitFlic RU unverified" in shelves["planes"]["B"]["note"]
        assert shelves["planes"]["C"]["status"] == "slot"
        assert "CNS-OPERATOR-ATTEST" in shelves["planes"]["C"]["refuse"]
        assert shelves["this_host"]["mission"].startswith("He Didn't Jump")
        assert "does not invent court holdings" in shelves["this_host"]["mission"].lower()
        assert shelves["lamb_lens"]["shelf"] == "https://www.azielcorpuslibrary.net/corpus" if "lamb_lens" in shelves else True
        assert shelves["this_host"]["lamb_lens"]["shelf"] == "https://www.azielcorpuslibrary.net/corpus"
        assert shelves["registry"]["independent_live_count"] == 1
        assert not shelves["registry"]["independent_requirement_met"]
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
        assert archive["item"] == "aziel-lockset-tip"
        assert archive["pack_sha256"] == CODEBERG_PACK
        assert archive["hash_verify"] == "pass"
        assert archive["status"] == "slot"
        assert archive["doi"] is None
        assert archive["refuse"] == "CNS-PLANE-B-ALL-TARGETS"
        assert archive.get("refuse") != "CNS-NO-WARC"
        gitflic = next(s for s in shelves["registry"]["shelves"] if s["id"] == "plane-b-gitflic-ru-tip-pack")
        assert gitflic["url"] is None
        assert gitflic["status"] == "slot"
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
        assert cite["planes"]["B"]["archive_org_tip_pack"]["hash_verify"] == "pass"
        assert "archive.org + GitFlic" not in cite["planes"]["B"]["note"]
        assert cite["archive_org_tip_pack"]["url"] == ARCHIVE_ORG_URL
        assert cite["archive_org_tip_pack"]["hash_verify"] == "pass"
        assert cite["zenodo_tip_pack"]["refuse"] == "CNS-ZENODO-IP-BAN"
        assert cite["zenodo_tip_pack"]["doi"] is None
        assert cite["cap7_sites"]["hedidntjump"]["resolves_to_hub"] is False
        assert cite["lamb_lens"]["shelf"] == "https://www.azielcorpuslibrary.net/corpus"
        assert cite["ingest_as_receipt"]["tip"] == HDJ_INGEST_TIP
        assert cite["purpose"].startswith("Marion A. Zioncheck archive")
        assert f"{APEX}/shelves" in cite["query_urls"]
        assert "does not invent court holdings" in cite["purpose"].lower() or "re-examine" in cite["purpose"]

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
            assert "archive.org + GitFlic" not in blob, label
            assert "GitFlic" in blob, label
            assert "CNS-ZENODO-IP-BAN" in blob, label
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
        for loc in ("/shelves", "/shelves.json", "/lockset.json", "/v1/shelves", "/cold-copy"):
            assert loc in headers, loc
        redirects = (tree / "_redirects").read_text(encoding="utf-8")
        assert "/shelves /shelves.json 200" in redirects
        sitemap = (tree / "sitemap.xml").read_text(encoding="utf-8")
        assert f"{APEX}/shelves</loc>" in sitemap
        assert f"{APEX}/lockset.json</loc>" in sitemap
        openapi = json.loads((tree / "openapi.json").read_text(encoding="utf-8"))
        assert "/shelves" in openapi["paths"]
        assert "/lockset.json" in openapi["paths"]
        robots = (tree / "robots.txt").read_text(encoding="utf-8")
        assert "Growth-ON" in robots
        assert "Allow: /shelves" in robots
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
