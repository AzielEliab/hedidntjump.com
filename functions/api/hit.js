import { handleRequest } from "../../workers/hedidntjump-stats/src/index.js";

export async function onRequest(context) {
  const url = new URL(context.request.url);
  url.pathname = "/api/hit";
  return handleRequest(new Request(url, context.request), context.env);
}
