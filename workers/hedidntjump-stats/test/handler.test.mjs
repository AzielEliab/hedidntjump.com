import test from 'node:test';
import assert from 'node:assert/strict';
import { allowedOrigin, handleRequest } from '../src/index.js';

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

test('GET /api/stats is public-read CORS and does not increment', async () => {
  const env = { STATS: memoryKv({ views: '4', downloads: '2' }) };
  const res = await handleRequest(
    new Request('https://stats.test/api/stats', { headers: { Origin: 'https://evil.example' } }),
    env,
  );
  assert.equal(res.status, 200);
  assert.equal(res.headers.get('access-control-allow-origin'), '*');
  const body = await res.json();
  assert.equal(body.views, 4);
  assert.equal(body.downloads, 2);
});

test('GET /api/meta returns identity plus live counters', async () => {
  const env = { STATS: memoryKv({ views: '104', downloads: '0' }) };
  const res = await handleRequest(
    new Request('https://stats.test/api/meta', { headers: { Origin: 'https://elsewhere.example' } }),
    env,
  );
  assert.equal(res.status, 200);
  assert.equal(res.headers.get('access-control-allow-origin'), '*');
  const body = await res.json();
  assert.equal(body.who.name, 'Aziel Eliab');
  assert.ok(body.who.jobTitle.includes('Truthseeker'));
  assert.ok(body.pages.some((p) => p.id === 'azieleliab'));
  assert.equal(body.counters.views, 104);
  assert.equal(body.counters.downloads, 0);
  assert.match(body.as_of, /^\d{4}-\d{2}-\d{2}T/);
  assert.match(body.encouragement, /Read the five volumes/);
});

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
