/**
 * HDJ Live Nodes hub pull — short TTL wrap of runtime GET /v1/mesh.
 *
 * Live Nodes = human mesh users + cited human uses. Softwares ≠ Live Nodes.
 * software_nodes is the {slug}-worker roster and never feeds the pill.
 * This archive cites; it does not host mesh radios or Softwares.
 * Zioncheck stays the mission. Do not invent users.
 */
const SOT = "https://aziel-runtime.vibelock.workers.dev/v1/mesh";
const PERSON_ID = "https://www.azieleliab.com/#aziel";
const TTL = 60;
const UA = "Mozilla/5.0";
const LIVE_NODES_PLANE = "human-mesh-users-uses";
const SOFTWARE_NODES_PLANE = "software-worker-fanout";
const LIVE_NODES_NOTE =
  "Public Live Nodes (live_nodes / rollup.mesh) count human mesh users (join/heartbeat/presence with human bearers) plus the cited human uses signal (USES / human_uses). Isolated humans stay on isolated_nodes. Not Softwares catalog length. Not downloaded Softwares instances. Not software_nodes. software_nodes is the {slug}-worker roster and never feeds this pill. Uses are interaction counters, not unique people — incomplete or unbound telemetry is reported honestly (0 + complete=false). Live Nodes does not invent users. Zero is honest when no humans are present and uses are 0/unbound.";
const SOFTWARE_NODES_NOTE =
  "software_nodes / rollup.software count Softwares product Workers ({slug}-worker) from suite-presence fan-out. They may appear in the mesh roster. They must never feed public Live Nodes.";
const HUMAN_NODES_NOTE =
  "human_nodes / rollup.human count humans who exist as mesh users (join/heartbeat/presence — human bearers or kind=human). Auto-minted mesh_* joins are human participants. Named downloaded Softwares instance ids stay instance_nodes.";
const HUMAN_USES_NOTE =
  "human_uses is the USES interaction counter (no PII), not a unique-user count. Incomplete or unbound telemetry is reported as 0 with complete=false. Live Nodes does not invent users from missing uses.";

const JSON_HEADERS = {
  "content-type": "application/json; charset=utf-8",
  "cache-control": `public, max-age=${TTL}, stale-while-revalidate=300`,
  "cdn-cache-control": `public, max-age=${TTL}, stale-while-revalidate=300`,
  "cloudflare-cdn-cache-control": `public, max-age=${TTL}`,
};

export function isHumanLiveNodesPlane(sot) {
  if (!sot || typeof sot !== "object") return false;
  if (sot.live_nodes_plane === LIVE_NODES_PLANE) return true;
  const components = sot.live_nodes_components;
  if (components && components.software_nodes_excluded === true) return true;
  return typeof sot.human_uses === "number" && typeof sot.human_mesh_users === "number";
}

function asCount(value) {
  const n = Number(value);
  return Number.isFinite(n) && n >= 0 ? n : 0;
}

export function wrapMesh(sot, extra) {
  const humanPlane = isHumanLiveNodesPlane(sot);
  const softwareNodes = sot ? asCount(sot.software_nodes) : 0;
  const workerLive = sot && sot.live_nodes != null ? asCount(sot.live_nodes) : 0;
  const liveNodes = humanPlane ? workerLive : 0;
  const humanMeshUsers = humanPlane ? asCount(sot.human_mesh_users) : 0;
  const humanUses = humanPlane ? asCount(sot.human_uses) : 0;
  const humanUsesComplete = humanPlane && sot.human_uses_complete === true;
  return {
    spec: "LIVE-NODES-HUB-CITE-1.0",
    surface: "hedidntjump-hub-pull",
    this_host: "hedidntjump.com",
    this_host_role: "Marion Zioncheck archive — sister cite",
    this_host_is_live_door: false,
    this_host_runtime_front: false,
    softwares_clone: false,
    softwares_tab: false,
    mission: "Zioncheck archive",
    invented_users: false,
    author: "Aziel Eliab",
    identity: "Aziel Eliab",
    person_id: PERSON_ID,
    visible_1520: false,
    lamb_lens: {
      shelf: "https://www.azielcorpuslibrary.net/corpus",
      note: "Public Lamb Lens / Corpus ingest lives on azielcorpuslibrary.net.",
    },
    no_lie: "NO-LIE / NO-REWRITE",
    ttl_seconds: TTL,
    sot: SOT,
    sot_aliases: [
      "https://aziel-runtime.vibelock.workers.dev/mesh",
      "https://aziel-runtime.vibelock.workers.dev/v1/mesh",
    ],
    runtime_pr: "https://github.com/AzielEliab/aziel-runtime/pull/151",
    live_nodes_plane: LIVE_NODES_PLANE,
    software_nodes_plane: SOFTWARE_NODES_PLANE,
    live_nodes: liveNodes,
    live_nodes_complete: humanPlane,
    human_mesh_users: humanMeshUsers,
    human_uses: humanUses,
    human_uses_complete: humanUsesComplete,
    human_uses_kv: humanPlane ? sot.human_uses_kv === true : false,
    human_uses_source: humanPlane ? sot.human_uses_source || "uses.total" : "worker-legacy-plane-refused",
    software_nodes: softwareNodes,
    software_nodes_excluded: true,
    instance_nodes_excluded: true,
    invent_users: false,
    worker_human_plane: humanPlane,
    worker_live_nodes_plane: sot && sot.live_nodes_plane ? sot.live_nodes_plane : "legacy-mesh-size",
    worker_live_nodes_legacy: humanPlane ? 0 : workerLive,
    live_nodes_note: LIVE_NODES_NOTE,
    software_nodes_note: SOFTWARE_NODES_NOTE,
    human_nodes_note: HUMAN_NODES_NOTE,
    human_uses_note: sot && sot.human_uses_note ? sot.human_uses_note : HUMAN_USES_NOTE,
    live_nodes_components: {
      human_mesh_users: humanMeshUsers,
      human_uses: humanUses,
      software_nodes_excluded: true,
      instance_nodes_excluded: true,
      invent_users: false,
    },
    note: humanPlane
      ? "Hub pull of runtime GET /v1/mesh (short TTL). Live Nodes = human mesh users + cited human uses. Softwares stay on software_nodes and do not feed this pill. Zioncheck stays the HDJ mission."
      : "Hub pull of runtime GET /v1/mesh (short TTL). Worker still reports the legacy mesh-size plane (Softwares roster). HDJ does not display that roster as Live Nodes. live_nodes stays 0 + complete=false until the Worker human-mesh-users-uses plane is live. Zioncheck stays the HDJ mission.",
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

export async function pullMesh(request) {
  const origin = new URL(request.url).origin;
  let sot = null;
  let sotReach = false;
  try {
    sot = await getJson(SOT);
    sotReach = true;
  } catch (_err) {
    sot = null;
  }

  if (!sotReach) {
    try {
      const snap = await getJson(new URL("/mesh.json", origin).href);
      const body = {
        ...snap,
        degraded: true,
        sot_reach: false,
        pulled_at: new Date().toISOString(),
      };
      return new Response(JSON.stringify(body, null, 2) + "\n", {
        status: 200,
        headers: { ...JSON_HEADERS, "x-hdj-mesh": "snapshot-fallback" },
      });
    } catch (_err) {
      const body = wrapMesh(null, {
        degraded: true,
        sot_reach: false,
        pulled_at: new Date().toISOString(),
        note: "Runtime /v1/mesh unreachable. No invented Live Nodes.",
      });
      return new Response(JSON.stringify(body, null, 2) + "\n", {
        status: 503,
        headers: { ...JSON_HEADERS, "x-hdj-mesh": "degraded" },
      });
    }
  }

  const body = wrapMesh(sot, {
    degraded: false,
    sot_reach: true,
    pulled_at: new Date().toISOString(),
  });
  return new Response(JSON.stringify(body, null, 2) + "\n", {
    status: 200,
    headers: { ...JSON_HEADERS, "x-hdj-mesh": "live-pull" },
  });
}
