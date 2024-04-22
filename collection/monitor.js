import { hafas_client } from "./client.js";
import { db } from "./db.js";
import { sleep } from "./utils.js";

const station_ids = await db.selectFrom("stations").select("id").execute();
let i = 0;

while (i < station_ids.length) {
  try {
    const { id: station_id } = station_ids[i];
    const { departures } = await hafas_client.departures(station_id, {
      duration: 50,
      subStops: false,
      entrances: false,
      results: 60,
    });
    let inserted = 0;

    for (const dep of departures) {
      const new_dep = {
        id: "",
        direction: dep.direction,
        delay: dep.delay,
        when: dep.when,
        planned_when: dep.plannedWhen,
        station_id: dep.stop?.station?.id ?? dep.stop?.id,
        station_name: dep.stop?.station?.name ?? dep.stop?.name,
        line_id: dep.line?.id,
        line_name: dep.line?.name,
        product: dep.line?.product,
      };
      new_dep.id = `${new_dep.station_id}_${dep.tripId}`;
      const result = await db
        .insertInto("departures")
        .values(new_dep)
        .onConflict((oc) => oc.column("id").doUpdateSet(new_dep))
        .execute();
      inserted += Number(result[0].numInsertedOrUpdatedRows ?? 0);
    }

    console.log(`${inserted} rows updated`);
    await sleep(1000);
    i++;

    if (i === station_ids.length) {
      i = 0;
    }
  } catch (error) {
    console.error(error);
  }
}
