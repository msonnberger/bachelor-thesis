import { db } from "./db.js";
import { get_nearby_locations } from "./utils.js";

const center = {
  type: "location",
  latitude: 48.2084,
  longitude: 16.3778,
};
const meidling = {
  type: "location",
  latitude: 48.172233,
  longitude: 16.327456,
};
const simmering = {
  type: "location",
  latitude: 48.170523,
  longitude: 16.420444,
};
const kagran = {
  type: "location",
  latitude: 48.24883,
  longitude: 16.442337,
};
const waehring = {
  type: "location",
  latitude: 48.234622,
  longitude: 16.333863,
};
const stations = new Map();
const l = await Promise.all([
  get_nearby_locations(center),
  get_nearby_locations(meidling),
  get_nearby_locations(simmering),
  get_nearby_locations(kagran),
  get_nearby_locations(waehring),
]);
const locations = [...l[0], ...l[1], ...l[2], ...l[3], ...l[4]];
for (const location of locations) {
  if (location.type === "station" && location.id && location.name) {
    stations.set(location.id, {
      id: location.id,
      name: location.name,
      lat: location.location.latitude,
      lon: location.location.longitude,
    });
    continue;
  }
  if (
    location.type === "stop" &&
    location.station?.id &&
    location.station?.name
  ) {
    stations.set(location.station.id, {
      id: location.station.id,
      name: location.station.name,
      lat: location.station.location.latitude,
      lon: location.station.location.longitude,
    });
  }
}
await db
  .insertInto("stations")
  .values([...stations.values()])
  .onConflict((cf) => cf.column("id").doNothing())
  .execute();
await db.deleteFrom("stations").where("name", "not like", "Wien%").execute();
