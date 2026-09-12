import { handleRequest } from "../../../workers/hedidntjump-stats/src/index.js";

export async function onRequest(context) {
  const url = new URL(context.request.url);
  const rest = (context.params.path || []).join("/");
  url.pathname = "/api/foia" + (rest ? "/" + rest : "/ledger");
  return handleRequest(new Request(url, { method: context.request.method, headers: context.request.headers, body: context.request.body }), context.env);
}
