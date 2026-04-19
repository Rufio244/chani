import { aiV1 } from "../services/ai/v1.js";
import { aiV2 } from "../services/ai/v2.js";
import { businessV1 } from "../services/business/v1.js";

export async function routeRequest(req) {

  const { path, version } = req.query;

  if (path === "ai" && version === "v1") return aiV1(req);
  if (path === "ai" && version === "v2") return aiV2(req);

  if (path === "business") return businessV1(req);

  return { error: "route not found" };
}
