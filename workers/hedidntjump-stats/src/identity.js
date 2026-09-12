/** Shared public identity + citation fields for /api/meta and JSON mirrors. */

export const ORIGIN = "https://hedidntjump.com";
export const COUNTERS_URL = "https://hedidntjump-stats.vibelock.workers.dev/api/stats";
export const META_URL = "https://hedidntjump-stats.vibelock.workers.dev/api/meta";

export const ENCOURAGEMENT =
  "Read the five volumes and compare the plates with the official narrative. Download a PDF when you need the original page. The archive is for review of the record, not a verdict to copy.";

export const SITE_DESCRIPTION =
  "An Aziel Eliab Project: independent historical newspaper and five-volume archive examining the death of U.S. Representative Marion Zioncheck in Seattle on 7 August 1936. The official report called it suicide from a fifth-floor Arctic Building office. This project publishes the record for re-reading. It does not invent court holdings, FOIA denial letters, or quotes beyond what the volumes and cited papers print.";

export const WHY =
  "A closed story that never quite closed. The official line said Zioncheck jumped. The physics, the note, the witnesses, and the timing never agreed with that line. The work stays public so a death cannot be owned by the first headline that printed it.";

export const AUTHOR = {
  "@type": "Person",
  "@id": `${ORIGIN}/#aziel-eliab`,
  name: "Aziel Eliab",
  alternateName: ["Aziel Elroi Eliab", "AzielEliab"],
  url: "https://www.azieleliab.com/",
  jobTitle: [
    "Researcher",
    "Software developer",
    "Digital civil rights activist",
    "Truthseeker",
  ],
  sameAs: [
    "https://www.azieleliab.com/",
    "https://godlock.uk/",
    "https://www.azielcorpuslibrary.net/",
    "https://github.com/AzielEliab",
    "https://aziel-runtime.vibelock.workers.dev/",
    "https://x.com/AzielEliab",
  ],
};

export const EDITIONS = [
  { id: "home", name: "Main paper", url: `${ORIGIN}/` },
  { id: "official-narrative", name: "Official narrative", url: `${ORIGIN}/official-narrative.html` },
  { id: "foia", name: "FOIA paper", url: `${ORIGIN}/foia.html` },
  { id: "rubye", name: "Rubye paper", url: `${ORIGIN}/rubye.html` },
  { id: "azieleliab", name: "AzielEliab", url: `${ORIGIN}/azieleliab.html` },
];

export const RECOMMENDED_CITATION =
  "Eliab, Aziel. He Didn't Jump: The Marion Zioncheck Archive. 2026. https://hedidntjump.com/.";

export function buildCite() {
  return {
    "@context": "https://schema.org",
    "@type": "Dataset",
    name: "He Didn't Jump — The Marion Zioncheck Archive",
    url: `${ORIGIN}/`,
    description: SITE_DESCRIPTION,
    author: AUTHOR,
    creator: AUTHOR,
    publisher: {
      "@type": "Organization",
      "@id": `${ORIGIN}/#organization`,
      name: "He Didn't Jump — An Aziel Eliab Project",
      url: `${ORIGIN}/`,
    },
    license: "https://www.apache.org/licenses/LICENSE-2.0",
    licenseNote:
      "Site code is Apache-2.0. Original rights in collected photographs and clippings remain with their holders.",
    howToCite:
      "Cite the site and the edition you used. Quote only what the volumes and plates print. Do not invent dockets, holdings, or FOIA denial text.",
    recommendedCitation: RECOMMENDED_CITATION,
    editions: EDITIONS,
    sameAs: AUTHOR.sameAs,
  };
}

export function buildStats(counters, { live = false } = {}) {
  const body = {
    site: `${ORIGIN}/`,
    as_of: live ? new Date().toISOString() : "live",
    counters_url: COUNTERS_URL,
    meta_url: META_URL,
    encouragement: ENCOURAGEMENT,
    note: live
      ? "Live Worker snapshot. Do not treat a copied number as current."
      : "Static pointer. GET counters_url for the current views and downloads. This file does not invent counts.",
  };
  if (live && counters && typeof counters === "object") {
    body.views = Number(counters.views) || 0;
    body.downloads = Number(counters.downloads) || 0;
    body.items = counters.items && typeof counters.items === "object" ? counters.items : {};
  } else {
    body.views = null;
    body.downloads = null;
    body.items = null;
  }
  return body;
}

export function buildMeta(counters, { live = false } = {}) {
  const pages = [
    ...EDITIONS,
    { id: "reader", name: "Volume reader", url: `${ORIGIN}/reader.html` },
    { id: "llms", name: "LLM instructions", url: `${ORIGIN}/llms.txt` },
    { id: "cite", name: "Citation package", url: `${ORIGIN}/cite.json` },
    { id: "stats", name: "Public counters", url: `${ORIGIN}/stats.json` },
    { id: "meta", name: "Site metadata", url: `${ORIGIN}/meta.json` },
  ];
  return {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: "He Didn't Jump",
    url: `${ORIGIN}/`,
    what: SITE_DESCRIPTION,
    who: AUTHOR,
    why: WHY,
    pages,
    counters_url: COUNTERS_URL,
    llms_txt: `${ORIGIN}/llms.txt`,
    sitemap: `${ORIGIN}/sitemap.xml`,
    robots: `${ORIGIN}/robots.txt`,
    cite: `${ORIGIN}/cite.json`,
    stats: `${ORIGIN}/stats.json`,
    encouragement: ENCOURAGEMENT,
    counters: live && counters ? counters : { url: COUNTERS_URL },
    as_of: live ? new Date().toISOString() : "live",
  };
}
