import pandas as pd
import plotly.graph_objects as go


def puncutality_rate(delays, threshold=180):
    return 1 - len([delay for delay in delays if delay > threshold]) / delays.size


def print_df(name, df):
    print(name)
    print(df)
    print("\n")


departures = pd.read_csv("../collection/departures.csv")
departures = departures.fillna(0)
departures = departures[departures["product"].isin(["u-bahn", "tram", "city-bus"])]
departures = departures[departures["line_name"] != "Badner Bahn BB"]
departures[["station_id", "trip_id"]] = departures.apply(
    lambda row: row["id"].split("_"), axis=1, result_type="expand"
)

print_df("TABLE 1", departures["delay"].describe().round(2))


print("TABLE 2")
print(puncutality_rate(departures["delay"], 0))
print(puncutality_rate(departures["delay"], 60))
print(puncutality_rate(departures["delay"], 120))
print(puncutality_rate(departures["delay"], 180))
print(puncutality_rate(departures["delay"], 240))
print(puncutality_rate(departures["delay"], 300))
print("\n")

punct_rate_per_line = (
    departures.groupby("line_name", as_index=False)
    .agg(
        punct_rate=("delay", puncutality_rate),
        product=("product", pd.Series.mode),
        mean_delay=("delay", "mean"),
    )
    .sort_values(["punct_rate"], ascending=False)
)

print_df("TABLE 3", punct_rate_per_line.head(10))
print_df("TABLE 4", punct_rate_per_line.tail(5))
print_df("TABLE 5", punct_rate_per_line[punct_rate_per_line["product"] == "u-bahn"])
print_df("TABLE 6 & 7", punct_rate_per_line[punct_rate_per_line["product"] == "tram"])


punct_rate_per_station = (
    departures.groupby("station_name", as_index=False)
    .agg(
        punct_rate=("delay", puncutality_rate),
        products=("product", lambda x: set(x)),
        mean_delay=("delay", "mean"),
    )
    .sort_values(["punct_rate"], ascending=False)
)

print_df("TABLE 8", punct_rate_per_station.tail(10))
print_df("(SIDE CALCULATION)", punct_rate_per_station["punct_rate"].diff().nsmallest(5))


ubahn_stations = punct_rate_per_station[
    punct_rate_per_station["products"].isin(
        [
            {"u-bahn"},
            {"u-bahn", "city-bus"},
            {"u-bahn", "tram"},
            {"u-bahn", "city-bus", "tram"},
        ]
    )
]

print_df("TABLE 9", ubahn_stations.head(5))
print_df("TABLE 10", ubahn_stations.tail(5))

tram_stations = punct_rate_per_station[
    punct_rate_per_station["products"].isin(
        [
            {"tram"},
            {"tram", "city-bus"},
            {"u-bahn", "tram"},
            {"u-bahn", "city-bus", "tram"},
        ]
    )
]

bus_stations = punct_rate_per_station[
    punct_rate_per_station["products"].isin(
        [
            {"city-bus"},
            {"tram", "city-bus"},
            {"u-bahn", "city-bus"},
            {"u-bahn", "city-bus", "tram"},
        ]
    )
]

fig = go.Figure()
fig.add_trace(go.Box(x=punct_rate_per_station["punct_rate"], name="Overall"))
fig.add_trace(go.Box(x=ubahn_stations["punct_rate"], name="Metro"))
fig.add_trace(go.Box(x=tram_stations["punct_rate"], name="Tram"))
fig.add_trace(go.Box(x=bus_stations["punct_rate"], name="Bus"))
fig.write_image(file="figure-3.png", scale=3)


tram_71 = departures[departures["line_name"] == "Straßenbahn 71"]

print_df(
    "TABLE 11",
    tram_71.groupby("station_name")
    .filter(lambda g: len(g) > 1000)
    .groupby("station_name")
    .agg(punct_rate=("delay", puncutality_rate), avg_delay=("delay", "mean"))
    .sort_values(["punct_rate"], ascending=False),
)


karlsplatz = departures[
    departures["station_name"].isin(
        [
            "Wien Karlsplatz",
            "Wien Oper/Karlsplatz U",
            "Wien Bösendorferstraße/Karlsplatz U",
        ]
    )
]

print_df(
    "TABLE 12",
    karlsplatz.groupby("line_name")
    .filter(lambda g: len(g) > 1000)
    .groupby("line_name")
    .agg(punct_rate=("delay", puncutality_rate), avg_delay=("delay", "mean"))
    .sort_values(["punct_rate"], ascending=False),
)
