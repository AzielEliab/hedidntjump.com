'use strict';

(function () {
  const DEFAULT_API = 'https://hedidntjump-stats.vibelock.workers.dev';

  function apiBase() {
    const meta = document.querySelector('meta[name="hdj-stats-api"]');
    if (meta && meta.content.trim()) return meta.content.trim().replace(/\/+$/, '');
    return DEFAULT_API;
  }

  function endpoint(path) {
    return apiBase() + path;
  }

  function el(id) {
    return document.getElementById(id);
  }

  function escapeHtml(s) {
    return String(s || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function shortHash(h) {
    const hex = String(h || '');
    if (hex.length <= 16) return hex;
    return hex.slice(0, 8) + '…' + hex.slice(-8);
  }

  function paintLedger(data) {
    const count = el('foia-count');
    const list = el('foia-ledger');
    const empty = el('foia-empty');
    if (count) count.textContent = data && Number.isFinite(Number(data.count)) ? String(data.count) : '0';
    if (!list) return;
    const receipts = (data && data.receipts) || [];
    if (!receipts.length) {
      list.replaceChildren();
      if (empty) empty.hidden = false;
      return;
    }
    if (empty) empty.hidden = true;
    const frag = document.createDocumentFragment();
    receipts.forEach(function (row) {
      const article = document.createElement('article');
      article.className = 'receipt';
      const fileHref = endpoint('/api/foia/file/' + row.index);
      article.innerHTML =
        '<p class="receipt-kicker">Indexed denial · No. ' +
        escapeHtml(row.index) +
        '</p>' +
        '<p class="receipt-meta"><time datetime="' +
        escapeHtml(row.timestamp) +
        '">' +
        escapeHtml(row.timestamp) +
        '</time> · ' +
        escapeHtml(row.type || 'file') +
        ' · ' +
        escapeHtml(row.bytes || '') +
        ' bytes</p>' +
        '<dl class="receipt-hashes">' +
        '<div><dt>Index</dt><dd>' +
        escapeHtml(row.index) +
        '</dd></div>' +
        '<div><dt>Content hash</dt><dd><code>' +
        escapeHtml(row.content_hash) +
        '</code></dd></div>' +
        '<div><dt>Prev hash</dt><dd><code title="' +
        escapeHtml(row.prev_hash) +
        '">' +
        escapeHtml(shortHash(row.prev_hash)) +
        '</code></dd></div>' +
        '<div><dt>Chain hash</dt><dd><code>' +
        escapeHtml(row.hash) +
        '</code></dd></div>' +
        '</dl>' +
        '<p class="receipt-file"><a href="' +
        fileHref +
        '">View accepted file ↗</a></p>';
      frag.append(article);
    });
    list.replaceChildren(frag);
  }

  async function loadLedger() {
    const status = el('foia-status');
    try {
      const res = await fetch(endpoint('/api/foia/ledger'), { cache: 'no-store', mode: 'cors' });
      if (!res.ok) throw new Error('ledger ' + res.status);
      paintLedger(await res.json());
      if (status) status.textContent = '';
    } catch (err) {
      paintLedger({ count: 0, receipts: [] });
      if (status) {
        status.textContent =
          'The public ledger Worker is not reachable from this preview. After ZionBot deploys DENIALS R2 + STATS KV, this list fills from the hash chain.';
      }
    }
  }

  function showReasons(reasons) {
    const box = el('foia-reject');
    if (!box) return;
    box.hidden = false;
    box.replaceChildren();
    const title = document.createElement('p');
    title.textContent = 'Upload rejected. Nothing was added to the public ledger.';
    box.append(title);
    const ul = document.createElement('ul');
    (reasons || ['Unknown rejection.']).forEach(function (reason) {
      const li = document.createElement('li');
      li.textContent = reason;
      ul.append(li);
    });
    box.append(ul);
  }

  async function onSubmit(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const fileInput = el('foia-file');
    const reject = el('foia-reject');
    const ok = el('foia-accept');
    const submit = el('foia-submit');
    if (reject) reject.hidden = true;
    if (ok) ok.hidden = true;
    if (!fileInput || !fileInput.files || !fileInput.files[0]) {
      showReasons(['Choose a PDF or image of a Denied FOIA regarding Marion Zioncheck.']);
      return;
    }
    const body = new FormData();
    body.append('file', fileInput.files[0]);
    body.append('attestation', 'zioncheck-foia-denial');
    if (submit) submit.disabled = true;
    try {
      const res = await fetch(endpoint('/api/foia/upload'), { method: 'POST', body: body, mode: 'cors' });
      const data = await res.json();
      if (!res.ok || !data.ok) {
        showReasons(data.reasons || [data.error || 'Rejected.']);
        return;
      }
      if (ok) {
        ok.hidden = false;
        ok.textContent = 'Accepted as indexed denial No. ' + data.receipt.index + '. Hash ' + data.receipt.hash + '.';
      }
      form.reset();
      await loadLedger();
    } catch (err) {
      showReasons([
        'The ledger Worker did not accept the upload. Deploy workers/hedidntjump-stats with the DENIALS R2 bucket, then retry.',
      ]);
    } finally {
      if (submit) submit.disabled = false;
    }
  }

  const form = el('foia-form');
  if (form) form.addEventListener('submit', onSubmit);
  void loadLedger();
})();
