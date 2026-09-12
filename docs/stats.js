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

  function endpoint(path) {
    const base = apiBase();
    if (!base) return path;
    return base + path;
  }

  async function request(path) {
    // Prefer same-origin /api (Pages Function proxies to the Worker). Fallback to Worker URL.
    const urls = [path, endpoint(path)];
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
        const data = await res.json();
        // Ignore empty stub payloads from an unbound Pages Function
        if (
          data &&
          Number(data.views) === 0 &&
          Number(data.downloads) === 0 &&
          data.items &&
          typeof data.items === 'object' &&
          Object.keys(data.items).length === 0 &&
          url === path &&
          apiBase()
        ) {
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
})();
