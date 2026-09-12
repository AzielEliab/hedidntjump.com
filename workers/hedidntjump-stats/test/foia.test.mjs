import test from 'node:test';
import assert from 'node:assert/strict';
import { classifyDenialText, extractPdfText, gateUpload, GENESIS_HASH } from '../src/foia.js';
import { handleRequest } from '../src/index.js';

test('classifyDenialText requires FOIA + Zioncheck + denial language', () => {
  const miss = classifyDenialText('hello world this is a meme');
  assert.equal(miss.ok, false);
  assert.ok(miss.reasons.length >= 2);

  const ok = classifyDenialText(
    'This is a FOIA denial under 5 U.S.C. § 552. The request concerning Marion Zioncheck is denied. Records are withheld under exemption.',
  );
  assert.equal(ok.ok, true);
});

test('extractPdfText reads parenthetical strings', () => {
  const pdf = new TextEncoder().encode('%PDF-1.4 (Marion Zioncheck FOIA denial withheld) end');
  const text = extractPdfText(pdf);
  assert.match(text, /Marion Zioncheck FOIA denial/);
});

test('gateUpload rejects missing attestation and non-pdf/image types', async () => {
  const bytes = new Uint8Array([0x25, 0x50, 0x44, 0x46, 0x2d]);
  const noAttest = await gateUpload({ bytes, type: 'application/pdf', filename: 'x.pdf', attestation: '' }, {});
  assert.equal(noAttest.ok, false);
  assert.ok(noAttest.reasons.some((r) => /attest/i.test(r)));

  const badType = await gateUpload(
    { bytes: new Uint8Array([1, 2, 3]), type: 'text/html', filename: 'x.html', attestation: 'zioncheck-foia-denial' },
    {},
  );
  assert.equal(badType.ok, false);
});

test('gateUpload rejects a PDF that is not a Zioncheck FOIA denial', async () => {
  const body = '%PDF-1.4 (Totally unrelated vacation photos and a grocery list) ';
  const bytes = new TextEncoder().encode(body);
  bytes[0] = 0x25; bytes[1] = 0x50; bytes[2] = 0x44; bytes[3] = 0x46;
  const res = await gateUpload(
    { bytes, type: 'application/pdf', filename: 'vacation.pdf', attestation: 'zioncheck-foia-denial' },
    {},
  );
  assert.equal(res.ok, false);
  assert.ok(res.reasons.some((r) => /Zioncheck/i.test(r) || /FOIA/i.test(r)));
});

test('GET /api/foia/ledger returns an empty genesis chain without receipts', async () => {
  const store = new Map();
  const env = {
    STATS: {
      async get(key) {
        return store.has(key) ? store.get(key) : null;
      },
      async put(key, value) {
        store.set(key, value);
      },
      async list({ prefix }) {
        return { keys: [...store.keys()].filter((k) => k.startsWith(prefix)).map((name) => ({ name })) };
      },
    },
  };
  const res = await handleRequest(new Request('https://stats.test/api/foia/ledger'), env);
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.equal(body.count, 0);
  assert.equal(body.tip, GENESIS_HASH);
  assert.deepEqual(body.receipts, []);
});

test('POST /api/foia/upload rejects without multipart', async () => {
  const res = await handleRequest(
    new Request('https://stats.test/api/foia/upload', { method: 'POST', headers: { 'content-type': 'application/json' }, body: '{}' }),
    {},
  );
  assert.equal(res.status, 400);
  const body = await res.json();
  assert.equal(body.ok, false);
});
