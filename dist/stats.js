'use strict';

(function () {
  const DEFAULT_API = 'https://hedidntjump-stats.vibelock.workers.dev';

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
      label.textContent = id === 'downloads' ? ' downloads' : ' views';
    }
    el.replaceChildren(document.createTextNode(formatCount(value)), label);
  }

  function paint(data) {
    if (!data || typeof data !== 'object') return;
    setPill('views', data.views);
    setPill('downloads', data.downloads);
  }

  function readPill(id) {
    const el = document.getElementById(id);
    if (!el || !el.childNodes[0]) return null;
    const n = Number(String(el.childNodes[0].textContent).replace(/,/g, ''));
    return Number.isFinite(n) ? n : null;
  }

  function endpoint(path) {
    const base = apiBase();
    if (!base) return path;
    return base + path;
  }

  function candidateUrls(path) {
    const urls = [];
    const remote = endpoint(path);
    if (remote) urls.push(remote);
    try {
      urls.push(new URL(path, location.href).href);
    } catch (err) {
      urls.push(path);
    }
    const seen = Object.create(null);
    return urls.filter(function (url) {
      if (!url || seen[url]) return false;
      seen[url] = true;
      return true;
    });
  }

  function isStubPayload(data) {
    return (
      data &&
      Number(data.views) === 0 &&
      Number(data.downloads) === 0 &&
      data.items &&
      typeof data.items === 'object' &&
      Object.keys(data.items).length === 0
    );
  }

  async function request(path, options) {
    const opts = options || {};
    const urls = [path].concat(endpoint(path) === path ? [] : [endpoint(path)]);
    let lastError = new Error('stats unavailable');
    for (const url of urls) {
      try {
        const res = await fetch(url, {
          method: opts.method || 'GET',
          mode: 'cors',
          credentials: 'omit',
          cache: 'no-store',
          keepalive: opts.keepalive !== false,
        });
        if (!res.ok) {
          lastError = new Error('stats ' + res.status);
          continue;
        }
        const data = await res.json();
        if (isStubPayload(data) && url === path && apiBase()) {
          lastError = new Error('stats stub');
          continue;
        }
        return data;
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

  // POST the hit in a way that survives PDF navigation / file-download unload.
  // sendBeacon is always POST; the Worker reads type/id from the query string.
  // Prefer the Worker host first so a same-origin stub cannot swallow the increment.
  function beaconHit(path) {
    if (typeof navigator.sendBeacon !== 'function') return false;
    for (const url of candidateUrls(path)) {
      try {
        if (navigator.sendBeacon(url)) return true;
      } catch (err) {
        /* try next */
      }
    }
    return false;
  }

  async function hit(type, id) {
    const params = new URLSearchParams({ type: type, id: id || 'site' });
    const path = '/api/hit?' + params.toString();

    if (type === 'download') {
      const queued = beaconHit(path);
      const before = readPill('downloads');
      if (queued && before != null) setPill('downloads', before + 1);
      try {
        const data = queued
          ? await request('/api/stats', { keepalive: true })
          : await request(path, { keepalive: true });
        if (queued && before != null && Number(data.downloads) < before + 1) {
          return;
        }
        paint(data);
      } catch (err) {
        /* pills stay at last known / optimistic value */
      }
      return;
    }

    try {
      paint(await request(path, { keepalive: true }));
    } catch (err) {
      /* pills stay at last known value */
    }
  }

  async function zipExists(href) {
    try {
      const res = await fetch(href, { method: 'HEAD', cache: 'no-store', keepalive: true });
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

  function downloadAllVolumes(event, link) {
    const href = (link && link.getAttribute('href')) || '/volumes/hedidntjump-all-volumes.zip';
    // Record immediately — waiting on HEAD lets the zip navigation cancel the hit.
    void hit('download', 'all-volumes');
    event.preventDefault();
    void (async function () {
      const hasZip = await zipExists(href);
      if (hasZip) {
        startFileDownload(href);
        return;
      }
      for (let i = 1; i <= 5; i += 1) {
        startFileDownload('/volumes/volume-' + i + '.pdf', 'hedidntjump-volume-' + i + '.pdf');
        void hit('download', 'volume-' + i);
      }
    })();
  }

  function onDownloadClick(event, link) {
    const id = link.getAttribute('data-download') || 'download';
    if (id === 'all-volumes') {
      downloadAllVolumes(event, link);
      return;
    }
    void hit('download', id);
  }

  document.addEventListener('click', function (event) {
    if (event.defaultPrevented) return;
    if (event.button != null && event.button !== 0) return;
    const link = event.target && event.target.closest && event.target.closest('[data-download]');
    if (!link) return;
    onDownloadClick(event, link);
  });

  const page = document.body.getAttribute('data-stats-page') || '';
  if (page === 'landing') {
    void hit('view', 'landing');
  } else {
    void loadStats();
  }
})();
