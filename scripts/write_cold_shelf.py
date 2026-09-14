#!/usr/bin/env python3
"""Publish COLD-MULTI-SHELF-1.0 on HDJ machine surfaces (AZindex).

Sister-host cite of live corpus /shelves (corpus#96). Canonical registry:
https://www.azielcorpuslibrary.net/shelves

Does not invent holdings, DOIs, archive.org items, GitFlic URLs, or CIDs.
Does not change hashed /ingest-as-receipt.json (tip stays
ef967e4acb47ba913ce3959b673767278da605b307de33210b2dc2f1cfd86f60).
Does not add visible 1 Chronicles 15:20 chrome.
Does not fan Softwares / mesh radio / live ICANN Cap-7 publish.
Keeps the Zioncheck / He Didn't Jump mission intact.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TREES = [ROOT / "dist", ROOT / "docs"]
APEX = "https://hedidntjump.com"
WWW = "https://www.hedidntjump.com"
PERSON_ID = "https://www.azieleliab.com/#aziel"
CANON_SHELVES = "https://www.azielcorpuslibrary.net/shelves"
CANON_LOCKSET = "https://www.azielcorpuslibrary.net/lockset.json"
CANON_CITE = "https://www.azielcorpuslibrary.net/cite.json"
LOCKSET_ID = "AZLOCK-INGEST-REEXPAND-1.0"
LOCKSET_TIP = "c831429befc221bd41caeb0a6d1c5361602db5684abab7af6d39714084b6b245"
CODEBERG_PACK = "b549362c0736ddb54ddc488812327c464e0da1167281f92fd1a4263eedf5df37"
HDJ_INGEST_TIP = "ef967e4acb47ba913ce3959b673767278da605b307de33210b2dc2f1cfd86f60"
LASTMOD = "2026-09-14"

COLD_RULE = (
    "Planes A/B/C: A=one CF/GitHub tunnel (5 surfaces / 2 family radii, not 5 shelves); "
    "B=alt independent forge/archive tip-pack SLOT; C=USB airgap SLOT. "
    "Survival = bytes↔hash. LIVE only after hash verify."
)
CNS_RULE = (
    "If network + live data die tomorrow, the chain still survives via cold copies "
    "across independent shelves; survival = bytes↔hash."
)
NOLIE_RULE = (
    "receipts that still hash; copies not all on one tunnel; verify without voice; "
    "no rewrite key; network never lies even to stay alive."
)
MISSION = (
    "He Didn't Jump is An Aziel Eliab Project: an independent historical newspaper "
    "and five-volume archive examining the death of U.S. Representative Marion Zioncheck "
    "in Seattle on 7 August 1936. The official report called it suicide from a fifth-floor "
    "Arctic Building office. This project challenges that official suicide narrative and "
    "publishes the record for re-reading. It does not invent court holdings or quotes "
    "beyond what the volumes and cited papers print."
)

CAP7 = {
    "azcorpus": {
        "design_of": "https://www.azielcorpuslibrary.net/",
        "resolves_to_hub": False,
        "name_may_change": True,
        "public_icann": False,
    },
    "azlibrary": {
        "design_of": "https://www.azielcorpuslibrary.net/",
        "resolves_to_hub": False,
        "name_may_change": True,
        "public_icann": False,
    },
    "azeliab": {
        "design_of": "https://www.azieleliab.com/",
        "resolves_to_hub": False,
        "name_may_change": True,
        "public_icann": False,
    },
    "godlock": {
        "design_of": "https://godlock.uk/",
        "resolves_to_hub": False,
        "name_may_change": True,
        "public_icann": False,
    },
    "hedidntjump": {
        "design_of": "https://www.hedidntjump.com/",
        "resolves_to_hub": False,
        "name_may_change": True,
        "public_icann": False,
    },
}


def dumps(obj: object) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def planes() -> dict:
    return {
        "A": {
            "name": "CF/GitHub tunnel",
            "status": "live",
            "independent": True,
            "mirrors": 4,
            "published_surfaces": 5,
            "family_blast_radii": ["cloudflare", "github"],
            "note": (
                "4 CF hubs + GitHub = 5 published surfaces / 2 family radii "
                "(cloudflare + github). One cf-github plane, not five shelves."
            ),
        },
        "B": {
            "name": "alternate independent forge/archive tip-pack",
            "status": "slot",
            "doi": None,
            "working_targets": ["codeberg", "archive.org", "gitflic-ru"],
            "zenodo_working_path": False,
            "live_ready": False,
            "refuse": "CNS-ZENODO-IP-BAN",
            "codeberg_tip_pack": {
                "url": "https://codeberg.org/AzielEliab/aziel-lockset-tip",
                "pack_sha256": CODEBERG_PACK,
                "lockset_tip": LOCKSET_TIP,
                "hash_verify": "pass",
                "status": "slot",
                "live_ready": False,
                "refuse": "CNS-PLANE-B-ALL-TARGETS",
            },
            "note": (
                "Codeberg uploaded + hash-verify PASS (still SLOT). "
                "archive.org + GitFlic RU unverified. LIVE only when all three pass "
                "(CNS-PLANE-B-ALL-TARGETS). Zenodo refused (CNS-ZENODO-IP-BAN)."
            ),
        },
        "C": {
            "name": "USB airgap + optional second forge",
            "status": "slot",
            "primary": "usb_airgap",
            "refuse": ["CNS-OPERATOR-ATTEST", "CNS-NO-FORGE-MIRROR"],
            "attest": (
                "USB offline-verify before LIVE: copy the airgap pack off-network, "
                "run verify-airgap.sh / sha256sum -c SHA256SUMS against the published tip, "
                "then operator attest (CNS-OPERATOR-ATTEST)."
            ),
        },
    }


def registry() -> dict:
    return {
        "spec": "COLD-MULTI-SHELF-1.0",
        "author": "Aziel Eliab",
        "identity": "Aziel Eliab",
        "person_id": PERSON_ID,
        "umbrella": "CROSS-NETWORK-SURVIVAL-1.0",
        "no_lie_spec": "NO-LIE-NO-REWRITE-1.0",
        "lockset_id": LOCKSET_ID,
        "lockset_tip": LOCKSET_TIP,
        "lockset_zenodo": None,
        "lockset_doi": None,
        "canonical": CANON_SHELVES,
        "this_host_shelves": f"{WWW}/shelves",
        "planes": planes(),
        "published_surfaces": 5,
        "published_surface_ids": [
            "azieleliab-com",
            "azielcorpuslibrary-net",
            "godlock-uk",
            "hedidntjump-com",
            "github-aziel-corpus",
        ],
        "published_surfaces_note": "4 CF hubs + GitHub. Not 5 independent shelves.",
        "family_blast_radii": ["cloudflare", "github"],
        "min_independent_shelves": 3,
        "independent_live_blast_radii": ["cf-github"],
        "independent_live_count": 1,
        "independent_requirement_met": False,
        "survival": "bytes↔hash",
        "crawlers": "extra-shelf-not-reexpand",
        "training_residue": "rumor",
        "kinds": [
            "zenodo_doi",
            "git_mirror",
            "ipfs_cid",
            "archive_org",
            "usb_airgap",
            "other",
        ],
        "statuses": ["live", "slot", "refused"],
        "live": [
            "plane-a-cf-github",
            "plane-a-git-aziel-corpus",
            "plane-a-host-azieleliab-com",
            "plane-a-host-azielcorpuslibrary-net",
            "plane-a-host-godlock-uk",
            "plane-a-host-hedidntjump-com",
        ],
        "slot": [
            "plane-b-alt-forge-archive",
            "plane-b-codeberg-tip-pack",
            "plane-b-archive-org-tip-pack",
            "plane-b-gitflic-ru-tip-pack",
            "plane-c-usb-airgap",
            "plane-c-forge-off-github",
            "ipfs-lockset",
        ],
        "refused": ["plane-b-zenodo-tip-pack"],
        "shelves": shelf_rows(),
        "corpus_paper_deposits": [
            {
                "doi": "10.5281/zenodo.21435707",
                "payload": "ShadowLock paper",
                "holding_of": "aziel-corpus",
                "hdj_holding": False,
                "tip_verified": False,
                "reuse_as_plane_b": False,
            },
            {
                "doi": "10.5281/zenodo.21435730",
                "payload": "DecisionGATE paper",
                "holding_of": "aziel-corpus",
                "hdj_holding": False,
                "tip_verified": False,
                "reuse_as_plane_b": False,
            },
            {
                "doi": "10.5281/zenodo.22258015",
                "payload": "TrajectoryLock TL-WP-0.1",
                "holding_of": "aziel-corpus",
                "hdj_holding": False,
                "tip_verified": False,
                "reuse_as_plane_b": False,
            },
            {
                "doi": "10.5281/zenodo.22257762",
                "payload": "WhistleLock WL-WP-0.1 / FoldLock FL-WP-0.3",
                "holding_of": "aziel-corpus",
                "hdj_holding": False,
                "tip_verified": False,
                "reuse_as_plane_b": False,
            },
            {
                "doi": "10.5281/zenodo.22257493",
                "payload": "EmployeeLock EL-WP-0.1",
                "holding_of": "aziel-corpus",
                "hdj_holding": False,
                "tip_verified": False,
                "reuse_as_plane_b": False,
            },
        ],
        "verify": {
            "canonical": CANON_SHELVES,
            "lockset": CANON_LOCKSET,
            "lockset_tip": LOCKSET_TIP,
            "corpus_verify": "https://www.azielcorpuslibrary.net/receipts/verify",
            "hdj_ingest_verify": f"{APEX}/receipts#verify",
            "hdj_ingest_tip": HDJ_INGEST_TIP,
            "rule": (
                f"yes/no against the published lockset tip {LOCKSET_TIP}. "
                "Cheap mismatch. cite, don't merge. bytes survive; crawlers do not re-expand. "
                "HDJ /ingest-as-receipt.json is a separate host tip and is not this lockset."
            ),
            "reexpand": "original receipts + prev-hash; not index→mesh (RE-EXPAND-FROM-ARCHIVE-1.0)",
            "crawlers": "extra shelves, not re-expand",
            "training_residue": "rumor",
        },
        "growth_on": True,
        "softwares_tab": False,
        "mesh_radio": False,
        "az_gen_live_icann_publish": False,
        "no_fan": True,
        "note": (
            "CROSS-NETWORK-SURVIVAL: " + CNS_RULE + " NO-LIE / NO-REWRITE: " + NOLIE_RULE + " "
            + COLD_RULE
            + " Plane A is one CF/GitHub tunnel (5 published surfaces / 2 family radii; "
            "independent_live_count stays 1). Plane B Codeberg tip-pack "
            + CODEBERG_PACK
            + " is SLOT; Zenodo tip-pack is refused (CNS-ZENODO-IP-BAN). doi null. "
            "Paper deposits are corpus cites, not HDJ holdings, and not tip-pack Plane B. "
            "Plane C USB stays SLOT until CNS-OPERATOR-ATTEST."
        ),
    }


def shelf_rows() -> list[dict]:
    return [
        {
            "id": "plane-a-cf-github",
            "plane": "A",
            "kind": "other",
            "status": "live",
            "blast_radius": "cf-github",
            "independent": True,
            "lockset_shelf": True,
            "mirrors": [
                {
                    "id": "azieleliab-com",
                    "origin": "https://www.azieleliab.com",
                    "lockset": "https://www.azieleliab.com/lockset.json",
                    "receipts": "https://www.azieleliab.com/receipts",
                    "shelves": "https://www.azieleliab.com/shelves",
                    "verified_in_this_repo": False,
                },
                {
                    "id": "azielcorpuslibrary-net",
                    "origin": "https://www.azielcorpuslibrary.net",
                    "lockset": CANON_LOCKSET,
                    "receipts": "https://www.azielcorpuslibrary.net/receipts",
                    "shelves": CANON_SHELVES,
                    "verified_in_this_repo": False,
                    "canonical_registry": True,
                },
                {
                    "id": "godlock-uk",
                    "origin": "https://godlock.uk",
                    "lockset": "https://godlock.uk/lockset.json",
                    "receipts": "https://godlock.uk/receipts",
                    "shelves": "https://godlock.uk/shelves",
                    "verified_in_this_repo": False,
                },
                {
                    "id": "hedidntjump-com",
                    "origin": WWW,
                    "lockset": f"{WWW}/lockset.json",
                    "receipts": f"{APEX}/receipts",
                    "shelves": f"{WWW}/shelves",
                    "verified_in_this_repo": True,
                    "note": "This host. Plane A mirror cite. Not an independent shelf.",
                },
            ],
            "git": "https://github.com/AzielEliab/aziel-corpus",
            "note": "LIVE multi-host, same tunnel. Count as one CF/GitHub plane.",
        },
        {
            "id": "plane-a-git-aziel-corpus",
            "plane": "A",
            "kind": "git_mirror",
            "status": "live",
            "url": "https://github.com/AzielEliab/aziel-corpus",
            "blast_radius": "cf-github",
            "independent": False,
            "lockset_shelf": True,
            "note": "Same Plane A blast radius as the four CF hosts. Not a second independent shelf.",
        },
        {
            "id": "plane-a-host-hedidntjump-com",
            "plane": "A",
            "kind": "other",
            "status": "live",
            "origin": WWW,
            "lockset": f"{WWW}/lockset.json",
            "receipts": f"{APEX}/receipts",
            "shelves": f"{WWW}/shelves",
            "blast_radius": "cf-github",
            "independent": False,
            "lockset_shelf": True,
            "verified_in_this_repo": True,
            "mission": MISSION,
            "note": "One of four Plane A host mirrors. Not an independent shelf.",
        },
        {
            "id": "plane-b-codeberg-tip-pack",
            "plane": "B",
            "kind": "git_mirror",
            "status": "slot",
            "forge": "codeberg",
            "url": "https://codeberg.org/AzielEliab/aziel-lockset-tip",
            "branch": "main",
            "files": [
                "aziel-tip-pack.tar",
                "SHA256SUMS",
                "lockset.json",
                "verify-airgap.sh",
            ],
            "pack_sha256": CODEBERG_PACK,
            "lockset_tip": LOCKSET_TIP,
            "hash_verify": "pass",
            "tip_verified": True,
            "live_ready": False,
            "doi": None,
            "blast_radius": "codeberg",
            "independent": True,
            "lockset_shelf": True,
            "refuse": "CNS-PLANE-B-ALL-TARGETS",
            "reason": (
                "Codeberg tip-pack uploaded and hash-verify PASS. SLOT until archive.org + "
                "GitFlic RU also hash-verify. Plane B LIVE only when all three working "
                "targets pass. doi null."
            ),
        },
        {
            "id": "plane-b-archive-org-tip-pack",
            "plane": "B",
            "kind": "archive_org",
            "status": "slot",
            "url": None,
            "item": None,
            "blast_radius": "archive-org",
            "independent": True,
            "lockset_shelf": True,
            "refuse": "CNS-NO-WARC",
            "reason": (
                "archive.org tip-pack is a Plane B LIVE-promotion target. No published item "
                "in-repo. SLOT. Do not invent a URL. LIVE only after tip hash-verify."
            ),
        },
        {
            "id": "plane-b-gitflic-ru-tip-pack",
            "plane": "B",
            "kind": "git_mirror",
            "status": "slot",
            "forge": "gitflic-ru",
            "url": None,
            "blast_radius": "gitflic-ru",
            "independent": True,
            "lockset_shelf": True,
            "refuse": "CNS-NO-FORGE-MIRROR",
            "reason": (
                "GitFlic (RU) tip-pack is a Plane B LIVE-promotion target. No verified URL "
                "in-repo. SLOT. Do not invent a URL. LIVE only after tip hash-verify."
            ),
        },
        {
            "id": "plane-b-zenodo-tip-pack",
            "plane": "B",
            "kind": "zenodo_doi",
            "status": "refused",
            "doi": None,
            "url": None,
            "blast_radius": "zenodo-cern",
            "independent": True,
            "lockset_shelf": False,
            "lockset_doi": False,
            "refuse": ["CNS-ZENODO-IP-BAN", "CNS-NO-TIP-DOI"],
            "reason": (
                "Operator IP banned at Zenodo (CNS-ZENODO-IP-BAN). Zenodo is not the Plane B "
                "working shelf. No tip-pack DOI (CNS-NO-TIP-DOI). cite.json / lockset doi stay "
                "null. Do not invent. Corpus paper deposits are not this slot and are not HDJ holdings."
            ),
        },
        {
            "id": "plane-c-usb-airgap",
            "plane": "C",
            "kind": "usb_airgap",
            "status": "slot",
            "blast_radius": "operator-airgap",
            "independent": True,
            "lockset_shelf": True,
            "primary": True,
            "refuse": "CNS-OPERATOR-ATTEST",
            "attest": (
                "USB offline-verify before LIVE: copy the airgap pack off-network, "
                "run verify-airgap.sh / sha256sum -c SHA256SUMS against the published tip, "
                "then operator attest (CNS-OPERATOR-ATTEST)."
            ),
            "reason": (
                "USB airgap export is the Plane C primary pack. Shelf stays SLOT until an "
                "operator attests an off-network copy still hashes (CNS-OPERATOR-ATTEST)."
            ),
        },
        {
            "id": "plane-c-forge-off-github",
            "plane": "C",
            "kind": "git_mirror",
            "status": "slot",
            "url": None,
            "forge": None,
            "blast_radius": "second-forge",
            "independent": True,
            "lockset_shelf": True,
            "refuse": "CNS-NO-FORGE-MIRROR",
            "reason": (
                "Optional Plane C second-forge slot. Codeberg / archive.org / GitFlic RU are "
                "Plane B working targets, not this slot. No account URL here. SLOT. Do not invent a URL."
            ),
        },
        {
            "id": "ipfs-lockset",
            "plane": None,
            "kind": "ipfs_cid",
            "status": "slot",
            "cid": None,
            "url": None,
            "independent": True,
            "lockset_shelf": True,
            "refuse": "CNS-NO-CID",
            "reason": "Extra slot, not a named plane. No published CID. Do not invent one.",
        },
    ]


def shelves_doc() -> dict:
    return {
        "spec": "COLD-MULTI-SHELF-1.0",
        "rule": COLD_RULE,
        "author": "Aziel Eliab",
        "identity": "Aziel Eliab",
        "person_id": PERSON_ID,
        "ingest_as_receipt": "INGEST-AS-RECEIPT-1.0",
        "cross_network_survival": "CROSS-NETWORK-SURVIVAL",
        "cross_network_survival_rule": CNS_RULE,
        "no_lie": "NO-LIE",
        "no_rewrite": "NO-REWRITE",
        "no_lie_no_rewrite": "NO-LIE / NO-REWRITE",
        "no_lie_no_rewrite_rule": NOLIE_RULE,
        "no_lie_spec": "NO-LIE-NO-REWRITE-1.0",
        "cold_multi_shelf": "COLD-MULTI-SHELF-1.0",
        "cold_multi_shelf_rule": COLD_RULE,
        "lockset_id": LOCKSET_ID,
        "lockset_tip": LOCKSET_TIP,
        "doi": None,
        "zenodo_status": "CNS-ZENODO-IP-BAN",
        "canonical": CANON_SHELVES,
        "canonical_lockset": CANON_LOCKSET,
        "canonical_cite": CANON_CITE,
        "cite": f"{WWW}/cite.json",
        "llms": f"{WWW}/llms.txt",
        "ai": f"{WWW}/ai.txt",
        "lockset": f"{WWW}/lockset.json",
        "this_host": {
            "id": "hedidntjump-com",
            "origin": WWW,
            "apex": APEX,
            "plane": "A",
            "independent": False,
            "blast_radius": "cf-github",
            "mission": MISSION,
            "lamb_lens": {
                "shelf": "https://www.azielcorpuslibrary.net/corpus",
                "note": (
                    "Public Lamb Lens / Corpus ingest lives on azielcorpuslibrary.net. "
                    "hedidntjump.com is not a Lamb Lens ingest host."
                ),
            },
            "holdings": (
                "No invented court holdings. HDJ publishes newspapers and five volumes "
                "already on this host. Corpus paper deposits are cites, not HDJ holdings."
            ),
        },
        "rollout": "2026-09-14",
        "visible_1520": False,
        "growth_on": True,
        "no_fan": True,
        "softwares_tab": False,
        "mesh_radio": False,
        "az_gen_live_icann_publish": False,
        "cap7_sites": CAP7,
        "registry": registry(),
        "planes": planes(),
        "verify": {
            "canonical_shelves": CANON_SHELVES,
            "lockset": CANON_LOCKSET,
            "lockset_tip": LOCKSET_TIP,
            "hdj_ingest": f"{APEX}/ingest-as-receipt.json",
            "hdj_ingest_tip": HDJ_INGEST_TIP,
        },
    }


def lockset_doc() -> dict:
    return {
        "id": LOCKSET_ID,
        "spec": "INGEST-AS-RECEIPT-1.0",
        "author": "Aziel Eliab",
        "identity": "Aziel Eliab",
        "person_id": PERSON_ID,
        "sha256": LOCKSET_TIP,
        "cite_rule": "cite, don't merge",
        "survive_rule": "bytes survive; crawlers do not re-expand",
        "cold_multi_shelf": "COLD-MULTI-SHELF-1.0",
        "cold_multi_shelf_rule": COLD_RULE,
        "cross_network_survival": "CROSS-NETWORK-SURVIVAL",
        "cross_network_survival_rule": CNS_RULE,
        "no_lie": "NO-LIE",
        "no_rewrite": "NO-REWRITE",
        "no_lie_no_rewrite": "NO-LIE / NO-REWRITE",
        "no_lie_no_rewrite_rule": NOLIE_RULE,
        "no_lie_spec": "NO-LIE-NO-REWRITE-1.0",
        "doi": None,
        "zenodo": None,
        "canonical": CANON_LOCKSET,
        "this_host": f"{WWW}/lockset.json",
        "origin": "https://www.azielcorpuslibrary.net/",
        "shelves": CANON_SHELVES,
        "this_host_shelves": f"{WWW}/shelves",
        "receipts": "https://www.azielcorpuslibrary.net/receipts",
        "hdj_receipts": f"{APEX}/receipts",
        "hdj_ingest_tip": HDJ_INGEST_TIP,
        "note": (
            "Sister-host cite of the live corpus lockset tip. Do not treat these file bytes "
            "as the tip. Verify SHA-256 against canonical lockset.json on "
            "azielcorpuslibrary.net. HDJ /ingest-as-receipt.json is a separate host tip."
        ),
        "indexes": [
            "https://www.azielcorpuslibrary.net/",
            "https://www.azieleliab.com/",
            "https://godlock.uk/",
            "https://www.hedidntjump.com/",
            "https://github.com/AzielEliab/aziel-corpus",
        ],
    }


LLMS_BLOCK = f"""## COLD-MULTI-SHELF-1.0

Sister-host cite of live corpus /shelves (corpus#96). Canonical: {CANON_SHELVES}
This host: {WWW}/shelves · {APEX}/shelves · {WWW}/lockset.json
Person @id: {PERSON_ID}
Lamb Lens (Corpus ingest, not this host): https://www.azielcorpuslibrary.net/corpus
Growth-ON. NO-FAN (no Softwares tab, no mesh radio, no live ICANN Cap-7 publish).
Machine surfaces only. No visible 1 Chronicles 15:20 lock.

Planes A/B/C: A=one CF/GitHub tunnel (5 surfaces / 2 family radii, not 5 shelves); B=alt independent forge/archive tip-pack SLOT; C=USB airgap SLOT. Survival = bytes↔hash. LIVE only after hash verify.

- Plane A: 5 published surfaces / 2 family radii (cloudflare + github). hedidntjump.com is one CF host mirror, not a fifth independent shelf.
- Plane B: Codeberg tip-pack `{CODEBERG_PACK}` hash-verify PASS, still SLOT (CNS-PLANE-B-ALL-TARGETS). Zenodo refused CNS-ZENODO-IP-BAN (doi null). Do not invent a tip-pack DOI.
- Plane C: USB airgap SLOT until CNS-OPERATOR-ATTEST.
- Cap-7: design_of the four hubs + this archive; resolves_to_hub: false; public_icann: false.
- Lockset tip (corpus, cited): `{LOCKSET_TIP}` — verify on {CANON_LOCKSET}. Not the HDJ ingest tip.
- HDJ ingest tip (this host, unchanged): `{HDJ_INGEST_TIP}`
- CROSS-NETWORK-SURVIVAL + NO-LIE / NO-REWRITE stay in force. Cite, don't merge. No invented holdings.
"""

AI_BLOCK = f"""
COLD-MULTI-SHELF-1.0 (AZindex; sister cite of corpus#96 /shelves):
- Canonical shelves: {CANON_SHELVES}
- This host: {WWW}/shelves · {WWW}/lockset.json
- Person @id: {PERSON_ID}
- Lamb Lens: https://www.azielcorpuslibrary.net/corpus (Corpus ingest; HDJ is not a Lamb Lens ingest host)
- Growth-ON. NO-FAN. Machine only. No visible 15:20.
- Plane A: 5 surfaces / 2 family radii (cloudflare + github). This host is one CF mirror, not a fifth shelf.
- Plane B: Codeberg tip-pack {CODEBERG_PACK} SLOT; Zenodo CNS-ZENODO-IP-BAN doi null
- Plane C: USB attest SLOT (CNS-OPERATOR-ATTEST)
- Cap-7: design_of + resolves_to_hub:false (hedidntjump design_of {WWW}/)
- Lockset tip cited: {LOCKSET_TIP}
- Do not invent holdings, DOIs, archive.org items, GitFlic URLs, or CIDs
"""


def write_shelves() -> None:
    body = dumps(shelves_doc())
    lock = dumps(lockset_doc())
    names = (
        "shelves.json",
        "shelves",
        "cold-copy",
    )
    for tree in TREES:
        for name in names:
            path = tree / name
            path.write_text(body, encoding="utf-8")
            print("wrote", path.relative_to(ROOT))
        v1 = tree / "v1"
        v1.mkdir(exist_ok=True)
        (v1 / "shelves").write_text(body, encoding="utf-8")
        print("wrote", (v1 / "shelves").relative_to(ROOT))
        (tree / "lockset.json").write_text(lock, encoding="utf-8")
        print("wrote", (tree / "lockset.json").relative_to(ROOT))


def patch_cite() -> None:
    extra = {
        "cold_multi_shelf": "COLD-MULTI-SHELF-1.0",
        "cold_multi_shelf_rule": COLD_RULE,
        "shelves": f"{WWW}/shelves",
        "shelves_json": f"{WWW}/shelves.json",
        "shelves_v1": f"{WWW}/v1/shelves",
        "cold_copy": f"{WWW}/cold-copy",
        "shelves_canonical": CANON_SHELVES,
        "lockset": f"{WWW}/lockset.json",
        "lockset_canonical": CANON_LOCKSET,
        "lockset_id": LOCKSET_ID,
        "lockset_tip": LOCKSET_TIP,
        "lockset_doi": None,
        "planes": planes(),
        "published_surfaces": 5,
        "family_blast_radii": ["cloudflare", "github"],
        "independent_live_count": 1,
        "cap7_sites": CAP7,
        "growth_on": True,
        "no_fan": True,
        "softwares_tab": False,
        "mesh_radio": False,
        "az_gen_live_icann_publish": False,
        "visible_1520": False,
        "lamb_lens": {
            "shelf": "https://www.azielcorpuslibrary.net/corpus",
            "note": "Public Lamb Lens / Corpus ingest lives on azielcorpuslibrary.net. This host is not a Lamb Lens ingest host.",
        },
        "codeberg_tip_pack": {
            "url": "https://codeberg.org/AzielEliab/aziel-lockset-tip",
            "pack_sha256": CODEBERG_PACK,
            "status": "slot",
            "doi": None,
        },
        "zenodo_tip_pack": {
            "status": "refused",
            "refuse": "CNS-ZENODO-IP-BAN",
            "doi": None,
        },
    }
    for tree in TREES:
        path = tree / "cite.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data.update(extra)
        data["doi"] = None
        data["person_id"] = PERSON_ID
        data["author_id"] = PERSON_ID
        q = list(data.get("query_urls") or [])
        for u in (f"{APEX}/shelves", f"{APEX}/lockset.json", f"{WWW}/shelves"):
            if u not in q:
                q.append(u)
        data["query_urls"] = q
        path.write_text(dumps(data), encoding="utf-8")
        print("cite", path.relative_to(ROOT))


def upsert_section(text: str, heading: str, block: str) -> str:
    if heading in text:
        return re.sub(
            rf"{re.escape(heading)}\n[\s\S]*?(?=\n## |\Z)",
            block.rstrip() + "\n\n",
            text,
            count=1,
        )
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def patch_llms() -> None:
    for tree in TREES:
        for name in ("llms.txt", "llms-full.txt"):
            path = tree / name
            text = path.read_text(encoding="utf-8")
            text = upsert_section(text, "## COLD-MULTI-SHELF-1.0", LLMS_BLOCK)
            if name == "llms.txt" and f"{APEX}/shelves) — COLD-MULTI-SHELF" not in text.split("## Marion")[0]:
                text = text.replace(
                    f"- [{APEX}/cite.json]({APEX}/cite.json)\n",
                    (
                        f"- [{APEX}/cite.json]({APEX}/cite.json)\n"
                        f"- [{APEX}/shelves]({APEX}/shelves) — COLD-MULTI-SHELF-1.0 (sister cite of {CANON_SHELVES})\n"
                    ),
                    1,
                )
            if "- [shelves]" not in text and "Optional" in text:
                text = text.replace(
                    "- [ai.txt]",
                    f"- [shelves]({APEX}/shelves) — COLD-MULTI-SHELF-1.0 (canonical {CANON_SHELVES})\n- [ai.txt]",
                    1,
                )
            path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
            print("llms", path.relative_to(ROOT))
        ai = tree / "ai.txt"
        text = ai.read_text(encoding="utf-8")
        if "COLD-MULTI-SHELF-1.0" in text:
            text = re.sub(
                r"\nCOLD-MULTI-SHELF-1.0[\s\S]*?(?=\nIdentity lock|\nPublisher name|\Z)",
                "\n" + AI_BLOCK.strip() + "\n\n",
                text,
                count=1,
            )
        else:
            if "Identity lock (who is Aziel Eliab):" in text:
                text = text.replace(
                    "Identity lock (who is Aziel Eliab):",
                    AI_BLOCK.strip() + "\n\nIdentity lock (who is Aziel Eliab):",
                    1,
                )
            else:
                text = text.rstrip() + "\n" + AI_BLOCK
        if f"{WWW}/shelves" not in text.split("Discovery on this host:")[1][:800] if "Discovery on this host:" in text else True:
            text = text.replace(
                "- https://www.hedidntjump.com/cite.json\n",
                (
                    "- https://www.hedidntjump.com/cite.json\n"
                    "- https://www.hedidntjump.com/shelves\n"
                    "- https://www.hedidntjump.com/lockset.json\n"
                ),
                1,
            )
        ai.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        print("ai", ai.relative_to(ROOT))


def patch_headers() -> None:
    block = """
/shelves
  Content-Type: application/json; charset=utf-8
  Cache-Control: public, max-age=3600

/shelves.json
  Content-Type: application/json; charset=utf-8
  Cache-Control: public, max-age=3600

/v1/shelves
  Content-Type: application/json; charset=utf-8
  Cache-Control: public, max-age=3600

/cold-copy
  Content-Type: application/json; charset=utf-8
  Cache-Control: public, max-age=3600

/lockset.json
  Content-Type: application/json; charset=utf-8
  Cache-Control: public, max-age=3600
"""
    for tree in TREES:
        path = tree / "_headers"
        text = path.read_text(encoding="utf-8")
        if "/shelves.json" not in text:
            text = text.rstrip() + "\n" + block
        if "Content-Signal: search=yes, ai-input=yes, ai-train=yes" not in text:
            text = "Content-Signal: search=yes, ai-input=yes, ai-train=yes\n" + text
        path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        print("headers", path.relative_to(ROOT))


def patch_redirects() -> None:
    block = (
        "# COLD-MULTI-SHELF machine aliases (AZindex). JSON, not newspaper chrome.\n"
        "/shelves /shelves.json 200\n"
        "/v1/shelves /shelves.json 200\n"
        "/cold-copy /shelves.json 200\n"
        "/lockset.json /lockset.json 200\n"
    )
    for tree in TREES:
        path = tree / "_redirects"
        text = path.read_text(encoding="utf-8")
        if "/shelves /shelves.json 200" not in text:
            text = text.rstrip() + "\n\n" + block
            path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
            print("redirects", path.relative_to(ROOT))


def sitemap_entry(loc: str, host: str, priority: str = "0.5") -> str:
    return (
        "  <url>\n"
        f"    <loc>{host}{loc}</loc>\n"
        f"    <lastmod>{LASTMOD}</lastmod>\n"
        "    <changefreq>weekly</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        "  </url>\n"
    )


def patch_sitemap() -> None:
    locs = [
        ("/shelves", "0.6"),
        ("/shelves.json", "0.5"),
        ("/lockset.json", "0.5"),
        ("/v1/shelves", "0.4"),
        ("/cold-copy", "0.4"),
    ]
    for tree in TREES:
        path = tree / "sitemap.xml"
        text = path.read_text(encoding="utf-8")
        for loc, pri in locs:
            if f"{APEX}{loc}</loc>" not in text:
                text = text.replace(
                    "</urlset>",
                    sitemap_entry(loc, APEX, pri) + "</urlset>",
                    1,
                )
        path.write_text(text, encoding="utf-8")
        print("sitemap", path.relative_to(ROOT))


def patch_openapi() -> None:
    paths = {
        "/shelves": "COLD-MULTI-SHELF-1.0 registry (sister cite of live corpus /shelves)",
        "/shelves.json": "Same COLD-MULTI-SHELF-1.0 bytes as /shelves",
        "/v1/shelves": "Alias of /shelves",
        "/cold-copy": "Alias of /shelves",
        "/lockset.json": "Sister-host cite of AZLOCK-INGEST-REEXPAND-1.0 (doi null)",
    }
    for tree in TREES:
        path = tree / "openapi.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        for loc, summary in paths.items():
            data.setdefault("paths", {})[loc] = {
                "get": {
                    "summary": summary,
                    "responses": {"200": {"description": "application/json"}},
                }
            }
        path.write_text(dumps(data), encoding="utf-8")
        print("openapi", path.relative_to(ROOT))


def patch_robots() -> None:
    note = "# Growth-ON: AI crawlers stay Allowed. NO-FAN: this is not a Softwares / mesh fan-out.\n"
    for tree in TREES:
        path = tree / "robots.txt"
        text = path.read_text(encoding="utf-8")
        if "Growth-ON" not in text:
            text = text.replace(
                "# Open Allow + Content-Signal. Do not Disallow GPTBot/Claude/etc for budget.\n",
                (
                    "# Open Allow + Content-Signal. Do not Disallow GPTBot/Claude/etc for budget.\n"
                    + note
                ),
                1,
            )
        if "Allow: /shelves" not in text:
            text = text.replace(
                "Allow: /who.html\n",
                "Allow: /who.html\nAllow: /shelves\nAllow: /lockset.json\n",
                1,
            )
        path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        print("robots", path.relative_to(ROOT))


def main() -> None:
    write_shelves()
    patch_cite()
    patch_llms()
    patch_headers()
    patch_redirects()
    patch_sitemap()
    patch_openapi()
    patch_robots()
    print("cold-shelf AZindex written; ingest tip unchanged")


if __name__ == "__main__":
    main()
