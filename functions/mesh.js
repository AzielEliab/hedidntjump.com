import { pullMesh } from "./_lib/mesh-pull.js";

export async function onRequest(context) {
  return pullMesh(context.request);
}
