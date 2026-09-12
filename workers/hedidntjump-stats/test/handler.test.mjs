import test from 'node:test';
import assert from 'node:assert/strict';
import { allowedOrigin, displayMesh, handleRequest } from '../src/index.js';

test('CORS allows the archive hosts and localhost', () => {
  assert.equal(allowedOrigin('https://hedidntjump.com'), 'https://hedidntjump.com');
  assert.equal(allowedOrigin('https://www.hedidntjump.com'), 'https://www.hedidntjump.com');
  assert.equal(allowedOrigin('https://preview.pages.dev'), 'https://preview.pages.dev');
  assert.equal(allowedOrigin('http://localhost:8000'), 'http://localhost:8000');
  assert.equal(allowedOrigin('https://evil.example'), '');
});

function memoryKv(seed = {}) {
  const store = new Map(Object.entries(seed));
  return {
    async get(key) {
      return store.has(key) ? store.get(key) : null;
    },
    async put(key, value) {
      store.set(key, value);
    },
    async list({ prefix }) {
      return { keys: [...store.keys()].filter((k) => k.startsWith(prefix)).map((name) => ({ name })) };
    },
  };
}

test('GET /api/stats does not increment', async () => {
  const env = { STATS: memoryKv({ views: '4', downloads: '2' }) };
  const res = await handleRequest(new Request('https://stats.test/api/stats'), env);
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.equal(body.views, 4);
  assert.equal(body.downloads, 2);
});

test('GET /api/hit?type=view increments views once', async () => {
  const env = { STATS: memoryKv() };
  const res = await handleRequest(new Request('https://stats.test/api/hit?type=view&id=landing'), env);
  const body = await res.json();
  assert.equal(body.views, 1);
  assert.equal(body.downloads, 0);
  assert.equal(body.items.landing, 1);
});

test('download hits increment downloads and item id', async () => {
  const env = { STATS: memoryKv() };
  const res = await handleRequest(
    new Request('https://stats.test/hit?type=download&id=volume-1'),
    env,
  );
  const body = await res.json();
  assert.equal(body.downloads, 1);
  assert.equal(body.items['volume-1'], 1);
});

test('displayMesh is always mesh on and never copies off wording', () => {
  const painted = displayMesh({
    enabled: false,
    mesh_default: 'off',
    live_nodes: 37,
    rollup: { live: 12 },
  });
  assert.equal(painted.mesh, 'on');
  assert.equal(painted.live_nodes, 37);
  assert.equal(painted.author, 'Aziel Eliab');
  assert.equal(painted.identity, 'Aziel Eliab');
  assert.equal(JSON.stringify(painted).includes('off'), false);
});

test('GET /api/mesh proxies a read-only Live Nodes display', async () => {
  const env = {
    MESH_FETCH: async () =>
      new Response(JSON.stringify({ ok: true, enabled: true, live_nodes: 37 }), {
        status: 200,
        headers: { 'content-type': 'application/json' },
      }),
  };
  const res = await handleRequest(new Request('https://stats.test/api/mesh'), env);
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.equal(body.ok, true);
  assert.equal(body.mesh, 'on');
  assert.equal(body.live_nodes, 37);
  assert.equal(body.author, 'Aziel Eliab');
  assert.equal(JSON.stringify(body).includes('off'), false);
});

test('GET /api/mesh/status is the same read-only display', async () => {
  const env = {
    MESH_FETCH: async () =>
      new Response(JSON.stringify({ rollup: { live: 37 } }), { status: 200 }),
  };
  const res = await handleRequest(new Request('https://stats.test/api/mesh/status'), env);
  const body = await res.json();
  assert.equal(body.mesh, 'on');
  assert.equal(body.live_nodes, 37);
});

test('mesh write paths stay unread and unimplemented', async () => {
  for (const path of ['/api/mesh/enable', '/api/mesh/disable', '/mesh/join']) {
    const res = await handleRequest(new Request('https://stats.test' + path, { method: 'POST' }), {});
    assert.equal(res.status, 404);
    const body = await res.json();
    assert.equal(body.error, 'read_only');
  }
});

test('POST /api/mesh is refused', async () => {
  const res = await handleRequest(new Request('https://stats.test/api/mesh', { method: 'POST' }), {});
  assert.equal(res.status, 405);
});
