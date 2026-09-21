/**
 * HDJ BAN-SURVIVAL pull — short TTL hub wrap.
 *
 * This archive is not a live FragGate door and not a Softwares clone.
 * Zioncheck stays the mission. Do not invent case facts or hosted Cap-7 /mcp.
 */
const SOT = "https://aziel-runtime.vibelock.workers.dev/v1/survival";
const CAP7 = "https://miragegrid.vibelock.workers.dev/bridge";
const PERSON_ID = "https://www.azieleliab.com/#aziel";
const TTL = 60;
const UA = "Mozilla/5.0";
const RUNTIME_PR = "https://github.com/AzielEliab/aziel-runtime/pull/152";
const RUNTIME_GIT_SHORT = "231b02f";
const RUNTIME_VERSION_ID = "a8f7fdc9";
const SPORE_PAPER =
  "https://github.com/AzielEliab/aziel-runtime/blob/main/docs/designs/SPORE-1.0.md";

const JSON_HEADERS = {
  "content-type": "application/json; charset=utf-8",
  "cache-control": `public, max-age=${TTL}, stale-while-revalidate=300`,
  "cdn-cache-control": `public, max-age=${TTL}, stale-while-revalidate=300`,
  "cloudflare-cdn-cache-control": `public, max-age=${TTL}`,
};

function defaultStack() {
  return [
    {
      layer: 1,
      id: "live-fronts",
      spec: "BAN-SURVIVAL-1.0",
      role: "failover",
      includes: ["cap-7", "calling-name", "live-node-api"],
    },
    {
      layer: 2,
      id: "cold-shelves",
      spec: "COLD-MULTI-SHELF-1.0",
      role: "mutual-backup",
      mutual_backup_with: "BAN-SURVIVAL-1.0",
      plane_b: "slot",
      plane_c: "slot",
      replaced: false,
      failed: false,
    },
    {
      layer: 3,
      id: "spore",
      spec: "SPORE-1.0",
      role: "failsafe",
      last_resort: true,
      replaces_cold_shelves: false,
      replaces_ban_survival: false,
    },
  ];
}

function compactStack(rows) {
  const src = Array.isArray(rows) && rows.length ? rows : defaultStack();
  return src.map((row) => {
    const item = {
      layer: row.layer,
      id: row.id,
      spec: row.spec,
      role: row.role,
    };
    if (row.id === "live-fronts") {
      item.includes = Array.isArray(row.includes)
        ? row.includes
        : ["cap-7", "calling-name", "live-node-api"];
    }
    if (row.id === "cold-shelves") {
      item.mutual_backup_with = row.mutual_backup_with || "BAN-SURVIVAL-1.0";
      item.plane_b = row.plane_b || "slot";
      item.plane_c = row.plane_c || "slot";
      item.replaced = row.replaced === true;
      item.failed = row.failed === true;
    }
    if (row.id === "spore") {
      item.last_resort = true;
      item.replaces_cold_shelves = false;
      item.replaces_ban_survival = false;
    }
    return item;
  });
}

function compactReCold(raw) {
  const src = raw && typeof raw === "object" ? raw : {};
  return {
    hook: "RE-COLD-STORE",
    allowed: src.allowed !== false,
    trigger: src.trigger || "cold-shelves-wiped-or-failed",
    active: src.active === true,
    shelves_failed: src.shelves_failed === true,
    shelves_intact: src.shelves_intact !== false,
    invent_live: false,
    invent_hash: false,
    invent_receipt: false,
    invent_destination: false,
    public_inventory_required: false,
    destinations: Array.isArray(src.destinations) ? src.destinations : [],
    opaque_placement: src.opaque_placement !== false,
    note:
      src.note ||
      "When cold stores are wiped or fail, the mesh may re-cold-store DNA wherever available. Never invent LIVE stores, hashes, receipts, or destinations. No required public inventory. Does not claim a wipe is happening now.",
  };
}

function wrap(sot, cap7, extra) {
  const liveDoors = Array.isArray(sot && sot.live_doors) ? sot.live_doors : [];
  const platforms = (sot && sot.platforms) || {};
  const calling = (sot && sot.calling_name) || {};
  const cap7az = (sot && sot.cap7_aznet) || {};
  const app = (cap7 && cap7.app_worker) || {};
  const honesty = (cap7 && cap7.honesty) || {};
  const sites = Array.isArray(cap7 && cap7.cap7) ? cap7.cap7 : [];
  const azshift = sites.find((row) => row && row.label === "azshift") || null;
  const spore = (sot && sot.spore) || {};
  const stack = compactStack((sot && sot.survival_stack) || spore.stack);
  const reCold = compactReCold((sot && sot.re_cold_store) || spore.re_cold_store);
  return {
    spec: "BAN-SURVIVAL-1.0",
    surface: "hedidntjump-hub-pull",
    this_host: "hedidntjump.com",
    this_host_role: "Marion Zioncheck archive — sister cite, not a Softwares hub",
    this_host_is_live_door: false,
    this_host_runtime_front: false,
    softwares_clone: false,
    softwares_tab: false,
    mission: "Zioncheck archive",
    invented_case_facts: false,
    author: "Aziel Eliab",
    identity: "Aziel Eliab",
    person_id: PERSON_ID,
    visible_1520: false,
    lamb_lens: {
      shelf: "https://www.azielcorpuslibrary.net/corpus",
      note: "Public Lamb Lens / Corpus ingest lives on azielcorpuslibrary.net. hedidntjump.com is not a Lamb Lens ingest host.",
    },
    no_lie: "NO-LIE / NO-REWRITE",
    ttl_seconds: TTL,
    sot: SOT,
    sot_aliases: [
      "https://aziel-runtime.vibelock.workers.dev/survival",
      "https://www.azielcorpuslibrary.net/runtime/survival",
      "https://www.azieleliab.com/runtime/survival",
      "https://godlock.uk/runtime/survival",
    ],
    mode: sot && sot.mode ? sot.mode : "LIVE",
    mutual_backup: sot ? sot.mutual_backup === true : false,
    live_doors: liveDoors.map((d) => ({
      id: d.id,
      origin: d.origin,
      via: d.via,
      status: d.status,
      independent: d.independent === true,
    })),
    live_door_ids: liveDoors.map((d) => d.id),
    platforms: {
      spec: platforms.spec || "BAN-PLATFORMS-1.0",
      all_live: platforms.all_live === true,
      native_app_store: platforms.native_app_store === true,
      calling_name: platforms.calling_name || calling.calling_name || null,
    },
    calling_name: {
      spec: calling.spec || "BAN-CALLING-NAME-1.0",
      rotated: calling.rotated === true,
      calling_name: calling.calling_name || null,
      calling_slug: calling.calling_slug || null,
      identity: calling.identity || "Aziel Eliab",
      identity_unchanged: calling.identity_unchanged !== false,
    },
    cap7_aznet: {
      factory: cap7az.factory || "miragegrid",
      resolves_to_hub: cap7az.resolves_to_hub === true,
      public_icann: cap7az.public_icann === true,
      cite_status: cap7az.cite && cap7az.cite.status,
      aznet_verify_status: cap7az.aznet_verify && cap7az.aznet_verify.status,
      hosted_endpoints: cap7az.hosted_endpoints && cap7az.hosted_endpoints.status,
      shuffle_layout: cap7az.shuffle && cap7az.shuffle.layout,
      public_worker_shuffle: cap7az.shuffle && cap7az.shuffle.public_worker_shuffle,
    },
    miragegrid_worker: {
      url: "https://miragegrid.vibelock.workers.dev",
      bridge: CAP7,
      status: app.status || honesty.app_worker || "LIVE",
      resolves_to_hub: cap7 ? cap7.resolves_to_hub === true : false,
      public_icann: cap7 ? cap7.public_icann === true : false,
      public_pair: cap7 && cap7.public_pair ? cap7.public_pair : ["azgrid", "azbooth"],
      aznet_side: cap7 && cap7.aznet_side ? cap7.aznet_side : ["azcloak", "azvault", "azshift", "azflag", "azstandby"],
      public_pair_https: honesty.public_pair_https || "LIVE",
      aznet_side_https: honesty.aznet_side_https || "SLOT",
      hdj_design_site: "azshift",
      azshift: azshift
        ? {
            label: azshift.label,
            design_of: azshift.design_of,
            resolves_to_hub: azshift.resolves_to_hub === true,
            honesty_public: azshift.honesty_public,
            reach: azshift.reach,
          }
        : {
            label: "azshift",
            design_of: "https://hedidntjump.com/",
            resolves_to_hub: false,
            honesty_public: "SLOT",
            reach: "aznet",
          },
    },
    spore_spec: "SPORE-1.0",
    spore_role: (sot && sot.spore_role) || spore.role || "failsafe",
    spore_replaces_cold_shelves: false,
    survival_stack: stack,
    re_cold_store: reCold,
    spore: {
      spec: "SPORE-1.0",
      role: (sot && sot.spore_role) || spore.role || "failsafe",
      failsafe: true,
      last_resort: true,
      replaces_cold_shelves: false,
      replaces_ban_survival: false,
      cold_shelves_intact: spore.cold_shelves_intact !== false,
      mutual_backup_intact: spore.mutual_backup_intact !== false,
      faces: Array.isArray(spore.faces)
        ? spore.faces
        : ["pause", "preserve", "wait", "physical-wipe-only"],
      re_cold_store: reCold,
      software_tab: false,
      fraggate_slug: false,
      paper: SPORE_PAPER,
      runtime_pr: RUNTIME_PR,
      runtime_git_short: RUNTIME_GIT_SHORT,
      runtime_version_id: RUNTIME_VERSION_ID,
    },
    runtime_pr: RUNTIME_PR,
    runtime_git_short: RUNTIME_GIT_SHORT,
    runtime_version_id: RUNTIME_VERSION_ID,
    note: "Hub pull of runtime /survival (short TTL) plus MirageGrid Cap-7 Worker cite. SPORE-1.0 last-resort failsafe + RE-COLD-STORE honest hook. HDJ is not a named live exec front. FragGate stays the door on the runtime sister.",
    ...extra,
  };
}

async function getJson(url) {
  const res = await fetch(url, {
    headers: { accept: "application/json", "user-agent": UA },
  });
  if (!res.ok) throw new Error(`sot ${res.status}`);
  return res.json();
}

export async function pullSurvival(request) {
  const origin = new URL(request.url).origin;
  let sot = null;
  let cap7 = null;
  let sotReach = false;
  let cap7Reach = false;
  try {
    sot = await getJson(SOT);
    sotReach = true;
  } catch (_err) {
    sot = null;
  }
  try {
    cap7 = await getJson(CAP7);
    cap7Reach = true;
  } catch (_err) {
    cap7 = null;
  }

  if (!sotReach) {
    try {
      const snap = await getJson(new URL("/survival.json", origin).href);
      const body = {
        ...snap,
        degraded: true,
        sot_reach: false,
        cap7_reach: cap7Reach,
        pulled_at: new Date().toISOString(),
      };
      return new Response(JSON.stringify(body, null, 2) + "\n", {
        status: 200,
        headers: { ...JSON_HEADERS, "x-hdj-survival": "snapshot-fallback" },
      });
    } catch (_err) {
      const body = wrap(null, cap7, {
        degraded: true,
        sot_reach: false,
        cap7_reach: cap7Reach,
        pulled_at: new Date().toISOString(),
        note: "Runtime /survival unreachable. No invented live door.",
      });
      return new Response(JSON.stringify(body, null, 2) + "\n", {
        status: 503,
        headers: { ...JSON_HEADERS, "x-hdj-survival": "degraded" },
      });
    }
  }

  const body = wrap(sot, cap7, {
    degraded: false,
    sot_reach: true,
    cap7_reach: cap7Reach,
    pulled_at: new Date().toISOString(),
  });
  return new Response(JSON.stringify(body, null, 2) + "\n", {
    status: 200,
    headers: { ...JSON_HEADERS, "x-hdj-survival": "live-pull" },
  });
}
