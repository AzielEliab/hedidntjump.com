import assert from "node:assert/strict";
import test from "node:test";

import { canonicalRedirectUrl, onRequest } from "./www-canonical.mjs";

test("www root redirects to the apex", () => {
  assert.equal(
    canonicalRedirectUrl("https://www.hedidntjump.com/", "www.hedidntjump.com"),
    "https://hedidntjump.com/",
  );
});

test("path and query survive the redirect", () => {
  assert.equal(
    canonicalRedirectUrl(
      "https://www.hedidntjump.com/doors?x=1&y=hello%20world",
      "www.hedidntjump.com",
    ),
    "https://hedidntjump.com/doors?x=1&y=hello%20world",
  );
});

test("a www Host header redirects even when the URL host differs", () => {
  assert.equal(
    canonicalRedirectUrl(
      "https://hedidntjump.pages.dev/case?volume=1",
      "www.hedidntjump.com:443",
    ),
    "https://hedidntjump.com/case?volume=1",
  );
});

test("apex, preview, and other hosts stay put", () => {
  for (const [url, host] of [
    ["https://hedidntjump.com/doors?x=1", "hedidntjump.com"],
    ["https://hedidntjump.pages.dev/doors", "hedidntjump.pages.dev"],
    ["http://localhost:8000/doors?x=1", "localhost"],
  ]) {
    assert.equal(canonicalRedirectUrl(url, host), null);
  }
});

test("onRequest returns 301 with the canonical Location", async () => {
  const request = new Request("https://www.hedidntjump.com/foia?ref=paper#ignored");
  let nextCalled = false;
  const response = await onRequest({
    request,
    next: async () => {
      nextCalled = true;
      return new Response("page");
    },
  });
  assert.equal(nextCalled, false);
  assert.equal(response.status, 301);
  assert.equal(response.headers.get("location"), "https://hedidntjump.com/foia?ref=paper");
});

test("onRequest passes apex traffic through", async () => {
  const request = new Request("https://hedidntjump.com/doors");
  const response = await onRequest({
    request,
    next: async () => new Response("doors", { status: 200 }),
  });
  assert.equal(response.status, 200);
  assert.equal(await response.text(), "doors");
});
