import { pullSurvival } from "../_lib/survival-pull.js";

export async function onRequest(context) {
  return pullSurvival(context.request);
}
