'use strict';

(function () {
  const DEFAULT_API = 'https://hedidntjump-stats.vibelock.workers.dev';
  const RUNTIME_MESH = 'https://aziel-runtime.vibelock.workers.dev/v1/mesh';

  function apiBase() {
    const meta = document.querySelector('meta[name="hdj-stats-api"]');
    if (meta && meta.content.trim()) return meta.content.trim().replace(/\/+$/, '');
    if (typeof window.HDJ_STATS_API === 'string' && window.HDJ_STATS_API) {
      return window.HDJ_STATS_API.replace(/\/+$/, '');
    }
    return DEFAULT_API;
  }

  function formatCount(n) {
    const num = Number(n);
    if (!Number.isFinite(num) || num < 0) return '—';
    return new Intl.NumberFormat('en-US').format(Math.floor(num));
  }

  function setPill(id, value) {
    const el = document.getElementById(id);
    if (!el) return;
    let label = el.querySelector('span');
    if (!label) {
      label = document.createElement('span');
      label.textContent = id === 'downloads' ? 'downloads' : 'views';
    }
    el.replaceChildren(document.createTextNode(formatCount(value)), label);
  }

  function paint(data) {
    if (!data || typeof data !== 'object') return;
    setPill('views', data.views);
    setPill('downloads', data.downloads);
  }

  function liveNodeCount(data) {
    if (!data || typeof data !== 'object') return null;
    const src = data.src && typeof data.src === 'object' ? data.src : null;
    const n =
      data.live_nodes != null
        ? data.live_nodes
        : src && src.live_nodes != null
          ? src.live_nodes
          : data.rollup && data.rollup.live != null
            ? data.rollup.live
            : Array.isArray(data.nodes)
              ? data.nodes.length
              : null;
    const num = Number(n);
    return Number.isFinite(num) && num >= 0 ? Math.floor(num) : null;
  }

  function paintMesh(data) {
    const el = document.getElementById('aziel-live-nodes');
    if (!el) return;
    const n = liveNodeCount(data);
    const count = n == null ? '—' : formatCount(n);
    let label = el.querySelector('span');
    if (!label) {
      label = document.createElement('span');
    }
    label.textContent = 'mesh on';
    el.replaceChildren(document.createTextNode('Live Nodes · ' + count + ' / '), label);
  }

  function meshUrls() {
    const urls = ['/api/mesh', '/api/mesh/status'];
    const base = apiBase();
    if (base) {
      urls.push(base + '/api/mesh');
      urls.push(base + '/api/mesh/status');
    }
    urls.push(RUNTIME_MESH);
    urls.push(RUNTIME_MESH + '/status');
    return urls;
  }

  async function loadMesh() {
    paintMesh({ live_nodes: null });
    for (const url of meshUrls()) {
      try {
        const res = await fetch(url, {
          method: 'GET',
          mode: 'cors',
          credentials: 'omit',
          cache: 'no-store',
          headers: { Accept: 'application/json' },
        });
        if (!res.ok) continue;
        const data = await res.json();
        if (data && typeof data === 'object') {
          paintMesh(data);
          return;
        }
      } catch (err) {
        /* try the next source */
      }
    }
    paintMesh({ live_nodes: null });
  }

  function endpoint(path) {
    const base = apiBase();
    if (!base) return path;
    return base + path;
  }

  async function request(path) {
    const urls = [endpoint(path)];
    if (apiBase()) urls.push(path);
    let lastError = new Error('stats unavailable');
    for (const url of urls) {
      try {
        const res = await fetch(url, {
          method: 'GET',
          mode: 'cors',
          credentials: 'omit',
          cache: 'no-store',
        });
        if (!res.ok) {
          lastError = new Error('stats ' + res.status);
          continue;
        }
        return await res.json();
      } catch (err) {
        lastError = err;
      }
    }
    throw lastError;
  }

  async function loadStats() {
    try {
      paint(await request('/api/stats'));
    } catch (err) {
      paint({ views: null, downloads: null });
    }
  }

  async function hit(type, id) {
    const params = new URLSearchParams({ type: type, id: id || 'site' });
    try {
      paint(await request('/api/hit?' + params.toString()));
    } catch (err) {
      /* pills stay at last known value */
    }
  }

  async function zipExists(href) {
    try {
      const res = await fetch(href, { method: 'HEAD', cache: 'no-store' });
      return res.ok;
    } catch (err) {
      return false;
    }
  }

  function startFileDownload(href, filename) {
    const a = document.createElement('a');
    a.href = href;
    if (filename) a.setAttribute('download', filename);
    a.rel = 'noopener';
    document.body.appendChild(a);
    a.click();
    a.remove();
  }

  async function downloadAllVolumes(event) {
    const link = event.currentTarget;
    const href = link.getAttribute('href') || '/volumes/hedidntjump-all-volumes.zip';
    const hasZip = await zipExists(href);
    if (hasZip) {
      void hit('download', 'all-volumes');
      return;
    }
    event.preventDefault();
    void hit('download', 'all-volumes');
    for (let i = 1; i <= 5; i += 1) {
      startFileDownload('/volumes/volume-' + i + '.pdf', 'hedidntjump-volume-' + i + '.pdf');
      void hit('download', 'volume-' + i);
    }
  }

  function onDownloadClick(event) {
    const link = event.currentTarget;
    const id = link.getAttribute('data-download') || 'download';
    if (id === 'all-volumes') {
      void downloadAllVolumes(event);
      return;
    }
    void hit('download', id);
  }

  document.querySelectorAll('[data-download]').forEach(function (link) {
    link.addEventListener('click', onDownloadClick);
  });

  const page = document.body.getAttribute('data-stats-page') || '';
  if (page === 'landing') {
    void hit('view', 'landing');
  } else {
    void loadStats();
  }
  void loadMesh();
})();
