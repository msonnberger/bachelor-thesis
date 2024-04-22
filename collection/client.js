import { createClient } from "hafas-client";
import { profile as vorProfile } from "hafas-client/p/vor/index.js";
export const hafas_client = createClient(vorProfile, "hafas-ba");
