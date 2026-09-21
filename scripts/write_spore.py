#!/usr/bin/env python3
"""Cite Worker GET /v1/survival SPORE-1.0 + RE-COLD-STORE on HDJ machine surfaces.

SPORE is the last-resort failsafe (layer 3) after live fronts and cold-shelf
mutual backup. RE-COLD-STORE is an honest hook (no invented destinations).
Softwares blurbs stay untouched. HDJ stays the Zioncheck archive.
"""
from __future__ import annotations

import json
import re
import ssl
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TREES = [ROOT / "dist", ROOT / "docs"]
APEX = "https://hedidntjump.com"
WWW = "https://www.hedidntjump.com"
PERSON_ID = "https://www.azieleliab.com/#aziel"
HDJ_INGEST_TIP = "ef967e4acb47ba913ce3959b673767278da605b307de33210b2dc2f1cfd86f60"
TTL_SECONDS = 60
SOT_URL = "https://aziel-runtime.vibelock.workers.dev/v1/survival"
RUNTIME_PR = "https://github.com/AzielEliab/aziel-runtime/pull/152"
RUNTIME_GIT_SHA = "231b02fcbb7b50fbd52762a49329042bc1715fe9"
RUNTIME_GIT_SHORT = "231b02f"
RUNTIME_VERSION_ID = "a8f7fdc9"
SPORE_PAPER = (
    "https://github.com/AzielEliab/aziel-runtime/blob/main/docs/designs/SPORE-1.0.md"
)
LAMB_LENS = "https://www.azielcorpuslibrary.net/corpus"
UA = "Mozilla/5.0"

FACES = ("pause", "preserve", "wait", "physical-wipe-only")
RE_COLD_NOTE = (
    "When cold stores are wiped or fail, the mesh may re-cold-store DNA "
    "wherever available. Never invent LIVE stores, hashes, receipts, or "
    "destinations. No required public inventory. Does not claim a wipe is "
    "happening now."
)
DEFAULT_STACK = (
    {
        "layer": 1,
        "id": "live-fronts",
        "spec": "BAN-SURVIVAL-1.0",
        "role": "failover",
        "includes": ["cap-7", "calling-name", "live-node-api"],
    },
    {
        "layer": 2,
        "id": "cold-shelves",
        "spec": "COLD-MULTI-SHELF-1.0",
        "role": "mutual-backup",
        "mutual_backup_with": "BAN-SURVIVAL-1.0",
        "plane_b": "slot",
        "plane_c": "slot",
        "replaced": False,
        "failed": False,
    },
    {
        "layer": 3,
        "id": "spore",
        "spec": "SPORE-1.0",
        "role": "failsafe",
        "last_resort": True,
        "replaces_cold_shelves": False,
        "replaces_ban_survival": False,
    },
)


def dumps(obj: object) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def fetch_json(url: str) -> dict[str, Any] | None:
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": UA},
    )
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as res:
            return json.loads(res.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001 — writer falls back to pinned SoT
        print("fetch miss", url, type(exc).__name__, exc)
        return None


def compact_stack(rows: Any) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows or []:
        if not isinstance(row, dict):
            continue
        item: dict[str, Any] = {
            "layer": row.get("layer"),
            "id": row.get("id"),
            "spec": row.get("spec"),
            "role": row.get("role"),
        }
        if row.get("id") == "live-fronts":
            item["includes"] = list(row.get("includes") or ["cap-7", "calling-name", "live-node-api"])
        if row.get("id") == "cold-shelves":
            item["mutual_backup_with"] = row.get("mutual_backup_with") or "BAN-SURVIVAL-1.0"
            item["plane_b"] = row.get("plane_b") or "slot"
            item["plane_c"] = row.get("plane_c") or "slot"
            item["replaced"] = row.get("replaced") is True
            item["failed"] = row.get("failed") is True
        if row.get("id") == "spore":
            item["last_resort"] = True
            item["replaces_cold_shelves"] = False
            item["replaces_ban_survival"] = False
        out.append(item)
    return out or [dict(row) for row in DEFAULT_STACK]


def compact_re_cold(raw: Any) -> dict[str, Any]:
    src = raw if isinstance(raw, dict) else {}
    dest = src.get("destinations")
    destinations = dest if isinstance(dest, list) else []
    return {
        "hook": "RE-COLD-STORE",
        "allowed": src.get("allowed") is not False,
        "trigger": src.get("trigger") or "cold-shelves-wiped-or-failed",
        "active": src.get("active") is True,
        "shelves_failed": src.get("shelves_failed") is True,
        "shelves_intact": src.get("shelves_intact") is not False,
        "invent_live": False,
        "invent_hash": False,
        "invent_receipt": False,
        "invent_destination": False,
        "public_inventory_required": False,
        "destinations": destinations,
        "opaque_placement": src.get("opaque_placement") is not False,
        "note": src.get("note") or RE_COLD_NOTE,
    }


def spore_from_sot(sot: dict[str, Any] | None) -> dict[str, Any]:
    src = sot or {}
    spore = src.get("spore") if isinstance(src.get("spore"), dict) else {}
    stack = compact_stack(src.get("survival_stack") or spore.get("stack"))
    re_cold = compact_re_cold(src.get("re_cold_store") or spore.get("re_cold_store"))
    faces = list(spore.get("faces") or FACES)
    return {
        "spec": "SPORE-1.0",
        "role": src.get("spore_role") or spore.get("role") or "failsafe",
        "kind": "law",
        "author": "Aziel Eliab",
        "identity": "Aziel Eliab",
        "person_id": PERSON_ID,
        "tip": spore.get("tip")
        or (
            "SPORE-1.0: last-resort failsafe. pause / preserve / wait / "
            "physical-wipe-only. Not a replacement for cold shelves. "
            "No electricity is PAUSE, not death. Dormant nodes do not invent "
            "live heartbeats. On restore, reconcile forward — no rewrite of history."
        ),
        "rule": spore.get("rule")
        or (
            "Last-resort failsafe after live fronts and cold-shelf mutual backup. "
            "Power or network loss pauses execution. No pretend-live metabolism. "
            "Append-only ChainLock / AKM / receipt DNA stays on cold shelves, "
            "local nodes, and tip packs. Resume on power. Wipe resistance is "
            "every remaining copy. Plane B/C stay SLOT until attested. "
            "Physical wipe only. Does not replace BAN-SURVIVAL or COLD-MULTI-SHELF."
        ),
        "mode": spore.get("mode") or "live",
        "metabolism": spore.get("metabolism") or "on",
        "pause": spore.get("pause") is True,
        "preserve": spore.get("preserve") is not False,
        "wait": spore.get("wait") is True,
        "physical_wipe_only": True,
        "invented_heartbeats": False,
        "failsafe": True,
        "last_resort": True,
        "replaces_cold_shelves": False,
        "replaces_ban_survival": False,
        "cold_shelves_intact": spore.get("cold_shelves_intact") is not False,
        "mutual_backup_intact": spore.get("mutual_backup_intact") is not False,
        "faces": faces,
        "stack": stack,
        "re_cold_store": re_cold,
        "resume": spore.get("resume") or "memory_resolve-additive",
        "rewrite": False,
        "plane_a": spore.get("plane_a") or "live",
        "plane_b": "slot",
        "plane_c": "slot",
        "doi": None,
        "software_tab": False,
        "fraggate_slug": False,
        "paper": SPORE_PAPER,
        "umbrella": "CROSS-NETWORK-SURVIVAL-1.0",
        "remain_off_untouched": True,
        "visible_1520": False,
    }


def hub_wrap(sot: dict[str, Any] | None, *, pulled: bool) -> dict[str, Any]:
    spore = spore_from_sot(sot)
    return {
        "spec": "SPORE-1.0",
        "surface": "hedidntjump-hub-pull",
        "this_host": "hedidntjump.com",
        "this_host_role": "Marion Zioncheck archive — sister cite",
        "this_host_is_live_door": False,
        "this_host_runtime_front": False,
        "softwares_clone": False,
        "softwares_tab": False,
        "fraggate_slug": False,
        "mission": "Zioncheck archive",
        "invented_destinations": False,
        "invented_heartbeats": False,
        "author": "Aziel Eliab",
        "identity": "Aziel Eliab",
        "person_id": PERSON_ID,
        "visible_1520": False,
        "growth_on": True,
        "lamb_lens": {
            "shelf": LAMB_LENS,
            "note": "Public Lamb Lens / Corpus ingest lives on azielcorpuslibrary.net.",
        },
        "no_lie": "NO-LIE / NO-REWRITE",
        "ttl_seconds": TTL_SECONDS,
        "sot": SOT_URL,
        "sot_pulled": pulled,
        "runtime_pr": RUNTIME_PR,
        "runtime_git_sha": RUNTIME_GIT_SHA,
        "runtime_git_short": RUNTIME_GIT_SHORT,
        "runtime_version_id": RUNTIME_VERSION_ID,
        "role": spore["role"],
        "failsafe": True,
        "last_resort": True,
        "replaces_cold_shelves": False,
        "replaces_ban_survival": False,
        "cold_shelves_intact": spore["cold_shelves_intact"],
        "mutual_backup_intact": spore["mutual_backup_intact"],
        "faces": list(spore["faces"]),
        "survival_stack": list(spore["stack"]),
        "re_cold_store": dict(spore["re_cold_store"]),
        "spore": spore,
        "paper": SPORE_PAPER,
        "ingest_tip_unchanged": HDJ_INGEST_TIP,
        "note": (
            "Hub cite of runtime GET /v1/survival SPORE-1.0 + RE-COLD-STORE. "
            "Last-resort failsafe after live fronts and cold-shelf mutual backup. "
            "Does not replace shelves. Honest hook; destinations stay []. "
            "Zioncheck stays the HDJ mission."
        ),
    }


def survival_spore_fields(sot: dict[str, Any] | None) -> dict[str, Any]:
    """Fields merged onto the BAN-SURVIVAL hub wrap / live pull."""
    spore = spore_from_sot(sot)
    return {
        "spore_spec": "SPORE-1.0",
        "spore_role": spore["role"],
        "spore_replaces_cold_shelves": False,
        "survival_stack": list(spore["stack"]),
        "re_cold_store": dict(spore["re_cold_store"]),
        "spore": {
            "spec": "SPORE-1.0",
            "role": spore["role"],
            "failsafe": True,
            "last_resort": True,
            "replaces_cold_shelves": False,
            "replaces_ban_survival": False,
            "cold_shelves_intact": spore["cold_shelves_intact"],
            "mutual_backup_intact": spore["mutual_backup_intact"],
            "faces": list(spore["faces"]),
            "re_cold_store": dict(spore["re_cold_store"]),
            "software_tab": False,
            "fraggate_slug": False,
            "paper": SPORE_PAPER,
            "runtime_pr": RUNTIME_PR,
            "runtime_git_short": RUNTIME_GIT_SHORT,
            "runtime_version_id": RUNTIME_VERSION_ID,
        },
        "runtime_pr": RUNTIME_PR,
        "runtime_git_short": RUNTIME_GIT_SHORT,
        "runtime_version_id": RUNTIME_VERSION_ID,
    }


def spore_cite() -> dict[str, Any]:
    live = fetch_json(SOT_URL)
    return hub_wrap(live, pulled=live is not None)


def upsert_section(text: str, heading: str, block: str) -> str:
    if heading in text:
        return re.sub(
            rf"{re.escape(heading)}\n[\s\S]*?(?=\n## |\Z)",
            block.rstrip() + "\n\n",
            text,
            count=1,
        )
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


LLMS_BLOCK = f"""## SPORE-1.0

Hub cite of Aziel Runtime `GET /v1/survival` SPORE + RE-COLD-STORE. HDJ stays the Marion Zioncheck archive.

SoT: {SOT_URL}
Runtime lock: {RUNTIME_PR} (main `{RUNTIME_GIT_SHORT}` / Worker `{RUNTIME_VERSION_ID}`)
SPORE-1.0 is the last-resort failsafe (layer 3) after live fronts and cold-shelf mutual backup: pause / preserve / wait / physical-wipe-only.
Does not replace BAN-SURVIVAL or COLD-MULTI-SHELF. Cold shelves stay intact. Mutual backup stays intact.
No electricity is PAUSE, not death. Dormant nodes do not invent live heartbeats. On restore, reconcile forward — no rewrite of history.
RE-COLD-STORE is an honest hook (no invented destinations). `re_cold_store.destinations: []`. Does not claim a wipe is happening now.
Plane B/C stay SLOT until attested. doi null. Softwares-tab product: false. FragGate slug: false.
Paper: {SPORE_PAPER}
Person @id: {PERSON_ID}. Lamb Lens ingest: {LAMB_LENS} (not this host). NO-LIE / NO-REWRITE. No visible 1 Chronicles 15:20.
Zioncheck stays the HDJ mission. Do not invent court holdings, FOIA letters, or case quotes.
HDJ ingest tip unchanged: `{HDJ_INGEST_TIP}`
This host: {APEX}/survival · {APEX}/survival.json · {APEX}/v1/survival
"""

AI_BLOCK = f"""SPORE-1.0 (hub cite of Worker /v1/survival; Worker {RUNTIME_VERSION_ID} LIVE):
- SoT: {SOT_URL}
- Runtime lock: {RUNTIME_PR} (main {RUNTIME_GIT_SHORT} / Worker {RUNTIME_VERSION_ID})
- Last-resort failsafe (layer 3): pause / preserve / wait / physical-wipe-only
- Does not replace BAN-SURVIVAL or COLD-MULTI-SHELF. Cold shelves stay intact.
- RE-COLD-STORE is an honest hook. destinations: []. No invented LIVE store, hash, receipt, or destination.
- Does not claim a wipe is happening now. Plane B/C SLOT. doi null.
- Softwares-tab product: false. FragGate slug: false.
- Paper: {SPORE_PAPER}
- Zioncheck stays the HDJ mission. Do not invent case facts.
- Person @id: {PERSON_ID}. No visible 15:20.
- Lamb Lens: {LAMB_LENS}
- NO-LIE / NO-REWRITE
- This host: {WWW}/survival · {WWW}/survival.json
- Ingest tip unchanged: `{HDJ_INGEST_TIP}`
"""

WHO_BLOCK = f"""SPORE-1.0 (machine; hub cite of runtime /v1/survival SPORE + RE-COLD-STORE)
This host remains the Marion Zioncheck / He Didn't Jump archive.
SoT: {SOT_URL}
Runtime lock: {RUNTIME_PR} (main {RUNTIME_GIT_SHORT} / Worker {RUNTIME_VERSION_ID})
Last-resort failsafe after live fronts and cold-shelf mutual backup: pause / preserve / wait / physical-wipe-only.
Does not replace BAN-SURVIVAL or COLD-MULTI-SHELF. Cold shelves stay intact. Mutual backup stays intact.
RE-COLD-STORE is an honest hook (no invented destinations). destinations: []. Does not claim a wipe is happening now.
Softwares-tab product: false. FragGate slug: false. Plane B/C SLOT. doi null.
Identity Aziel Eliab only. Person @id: {PERSON_ID}.
Lamb Lens: {LAMB_LENS} (not this host). NO-LIE / NO-REWRITE. No visible 15:20.
Zioncheck stays the HDJ mission. Do not invent case facts.
Pull: {WWW}/survival · {WWW}/survival.json · {WWW}/v1/survival
"""


def merge_survival_json(sot: dict[str, Any] | None) -> None:
    extra = survival_spore_fields(sot)
    extra["note"] = (
        "Hub pull of runtime /survival (short TTL) plus MirageGrid Cap-7 Worker cite. "
        "SPORE-1.0 last-resort failsafe + RE-COLD-STORE honest hook from Worker "
        f"{RUNTIME_VERSION_ID}. FragGate stays the door on the runtime sister. "
        "Zioncheck stays the HDJ mission. Do not invent case facts."
    )
    for tree in TREES:
        path = tree / "survival.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data.update(extra)
        path.write_text(dumps(data), encoding="utf-8")
        print("survival", path.relative_to(ROOT))


def patch_cite(payload: dict[str, Any], sot: dict[str, Any] | None) -> None:
    extra = survival_spore_fields(sot)
    for tree in TREES:
        path = tree / "cite.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["spore"] = payload
        data["re_cold_store"] = payload["re_cold_store"]
        ban = dict(data.get("ban_survival") or {})
        ban.update(extra)
        if "note" in ban:
            ban["note"] = (
                "Hub pull of runtime /survival (short TTL) plus MirageGrid Cap-7 Worker cite. "
                "SPORE-1.0 last-resort failsafe + RE-COLD-STORE honest hook from Worker "
                f"{RUNTIME_VERSION_ID}. FragGate stays the door on the runtime sister. "
                "Zioncheck stays the HDJ mission. Do not invent case facts."
            )
        data["ban_survival"] = ban
        data["author"] = "Aziel Eliab"
        data["identity"] = "Aziel Eliab"
        data["person_id"] = PERSON_ID
        data["visible_1520"] = False
        path.write_text(dumps(data), encoding="utf-8")
        print("cite", path.relative_to(ROOT))


def patch_llms() -> None:
    for tree in TREES:
        for name in ("llms.txt", "llms-full.txt"):
            path = tree / name
            text = path.read_text(encoding="utf-8")
            if "## SPORE-1.0" in text:
                text = upsert_section(text, "## SPORE-1.0", LLMS_BLOCK)
            elif "## BAN-SURVIVAL-1.0" in text:
                # Keep BAN-SURVIVAL intact; insert SPORE after it.
                text = re.sub(
                    r"(## BAN-SURVIVAL-1.0\n[\s\S]*?)(?=\n## |\Z)",
                    lambda m: m.group(1).rstrip() + "\n\n" + LLMS_BLOCK.rstrip() + "\n\n",
                    text,
                    count=1,
                )
            else:
                text = upsert_section(text, "## SPORE-1.0", LLMS_BLOCK)
            if name == "llms.txt":
                old = (
                    f"- [{APEX}/survival]({APEX}/survival) — BAN-SURVIVAL-1.0 "
                    "hub pull of runtime /survival (short TTL)\n"
                )
                new = (
                    f"- [{APEX}/survival]({APEX}/survival) — BAN-SURVIVAL-1.0 hub pull of "
                    "runtime /survival (short TTL; SPORE-1.0 + RE-COLD-STORE)\n"
                )
                if old in text:
                    text = text.replace(old, new, 1)
            path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
            print("llms", path.relative_to(ROOT))
        ai = tree / "ai.txt"
        text = ai.read_text(encoding="utf-8")
        if "SPORE-1.0 (hub cite" in text:
            text = re.sub(
                r"\n+SPORE-1.0 \(hub cite[\s\S]*?(?=\nBAN-SURVIVAL|\nCOLD-MULTI-SHELF|\n## |\nIdentity lock|\Z)",
                "\n",
                text,
                count=1,
            )
        if "BAN-SURVIVAL-1.0 (hub pull" in text:
            text = text.replace(
                "BAN-SURVIVAL-1.0 (hub pull",
                AI_BLOCK.strip() + "\n\nBAN-SURVIVAL-1.0 (hub pull",
                1,
            )
        else:
            text = text.rstrip() + "\n\n" + AI_BLOCK
        ai.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        print("ai", ai.relative_to(ROOT))


def patch_who() -> None:
    for tree in TREES:
        for name in ("who-is", "who-is-aziel-eliab.txt"):
            path = tree / name
            text = path.read_text(encoding="utf-8")
            if "SPORE-1.0 (machine;" in text:
                text = re.sub(
                    r"SPORE-1.0 \(machine;[\s\S]*?(?=\nBAN-SURVIVAL|\nLIVE-NODES|\Z)",
                    WHO_BLOCK.strip() + "\n\n",
                    text,
                    count=1,
                )
            elif "BAN-SURVIVAL-1.0 (machine;" in text:
                text = text.replace(
                    "BAN-SURVIVAL-1.0 (machine;",
                    WHO_BLOCK.strip() + "\n\nBAN-SURVIVAL-1.0 (machine;",
                    1,
                )
            else:
                text = text.rstrip() + "\n\n" + WHO_BLOCK.strip() + "\n"
            path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
            print("who-is", path.relative_to(ROOT))


def patch_well_known(payload: dict[str, Any]) -> None:
    extra = {
        "spore": {
            "spec": payload["spec"],
            "sot": payload["sot"],
            "ttl_seconds": payload["ttl_seconds"],
            "role": payload["role"],
            "failsafe": True,
            "last_resort": True,
            "replaces_cold_shelves": False,
            "re_cold_store": "RE-COLD-STORE",
            "destinations": [],
            "runtime_version_id": payload["runtime_version_id"],
            "software_tab": False,
            "this_host_is_live_door": False,
            "mission": "Zioncheck archive",
            "person_id": PERSON_ID,
            "visible_1520": False,
        }
    }
    for tree in TREES:
        path = tree / ".well-known" / "aziel.json"
        if not path.is_file():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        data.update(extra)
        path.write_text(dumps(data), encoding="utf-8")
        print("well-known", path.relative_to(ROOT))


def patch_openapi() -> None:
    summary = (
        "BAN-SURVIVAL-1.0 hub pull of runtime /survival "
        f"(short TTL {TTL_SECONDS}s; SPORE-1.0 + RE-COLD-STORE; Zioncheck archive hub pull)"
    )
    for tree in TREES:
        path = tree / "openapi.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        paths = data.setdefault("paths", {})
        if "/survival" in paths:
            paths["/survival"]["get"]["summary"] = summary
        if "/survival.json" in paths:
            paths["/survival.json"]["get"]["summary"] = (
                "Same BAN-SURVIVAL-1.0 hub wrap as /survival "
                "(static snapshot; SPORE-1.0 + RE-COLD-STORE)"
            )
        path.write_text(dumps(data), encoding="utf-8")
        print("openapi", path.relative_to(ROOT))


def patch_runtime_launch() -> None:
    from write_runtime_launch import launch_cite

    body = dumps(launch_cite())
    for tree in TREES:
        path = tree / "runtime-launch.json"
        path.write_text(body, encoding="utf-8")
        print("runtime-launch", path.relative_to(ROOT))


def patch_readme() -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    line = (
        "SPORE-1.0 + RE-COLD-STORE hub cite: `/survival` cites runtime "
        f"`GET {SOT_URL}` — last-resort failsafe (pause / preserve / wait / "
        "physical-wipe-only). Does not replace cold shelves. RE-COLD-STORE "
        "honest hook (`destinations: []`). "
        f"Runtime lock {RUNTIME_PR} (main `{RUNTIME_GIT_SHORT}` / Worker `{RUNTIME_VERSION_ID}`). "
        "HDJ stays the Zioncheck archive.\n"
    )
    marker = "Sister cite:"
    if "SPORE-1.0 + RE-COLD-STORE hub cite" in text:
        text = re.sub(
            r"SPORE-1.0 \+ RE-COLD-STORE hub cite:[\s\S]*?(?=\nSister cite:)",
            line + "\n",
            text,
            count=1,
        )
    else:
        text = text.replace(marker, line + "\n" + marker, 1)
    path.write_text(text, encoding="utf-8")
    print("readme", path.relative_to(ROOT))


def main() -> None:
    live = fetch_json(SOT_URL)
    payload = hub_wrap(live, pulled=live is not None)
    assert payload["person_id"] == PERSON_ID
    assert payload["spec"] == "SPORE-1.0"
    assert payload["replaces_cold_shelves"] is False
    assert payload["re_cold_store"]["hook"] == "RE-COLD-STORE"
    assert payload["re_cold_store"]["destinations"] == []
    assert payload["re_cold_store"]["invent_destination"] is False
    assert payload["runtime_version_id"] == RUNTIME_VERSION_ID
    assert payload["this_host_is_live_door"] is False
    assert payload["softwares_tab"] is False
    assert payload["mission"] == "Zioncheck archive"
    merge_survival_json(live)
    patch_cite(payload, live)
    patch_llms()
    patch_who()
    patch_well_known(payload)
    patch_openapi()
    patch_runtime_launch()
    patch_readme()
    print("spore hub cite written; Softwares blurbs untouched; ingest tip unchanged")


if __name__ == "__main__":
    main()
