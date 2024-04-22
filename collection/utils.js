import { hafas_client } from "./client.js";
/*
export async function get_line_ids(
  line_names: string[],
  product: "city-bus" | "tram" | "u-bahn"
) {
  if (!hafas_client.lines) {
    throw new Error("lines function is not defined");
  }

  // @ts-expect-error
  const promises = line_names.map((line) => client.lines(line, undefined));
  const results = await Promise.allSettled(promises);
  let line_ids: string[] = [];

  for (const result of results) {
    if (result.status !== "fulfilled") {
      continue;
    }

    const ids =
      result.value.lines
        ?.filter(
          (res) =>
            res.id?.startsWith("vor") &&
            res.product === product &&
            res.operator?.id === "wiener-linien"
        )
        .map((res) => res.id ?? "") ?? [];

    line_ids = [...line_ids, ...ids];
  }

  return line_ids;
}
*/
export const sleep = async (ms) => new Promise((r) => setTimeout(r, ms));
export async function get_nearby_locations(location) {
    const locations = await hafas_client.nearby(location, {
        products: {
            tram: true,
            "u-bahn": true,
            "city-bus": true,
        },
        subStops: false,
        entrances: false,
        linesOfStops: true,
        results: 5000,
        distance: 100_000,
    });
    return locations;
}
