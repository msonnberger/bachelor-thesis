import plotly.express as px
import pandas as pd


def puncutality_rate(delays):
    return 1 - len([delay for delay in delays if delay > 180]) / delays.size


px.set_mapbox_access_token(open(".mapbox_token").read())
stations = pd.read_csv("../collection/stations.csv", sep=";", index_col=0).to_dict(
    orient="index"
)
departures = pd.read_csv("../collection/departures.csv")
departures = departures.fillna(0)


def generate_map(departures):
    punct_rate_per_station = (
        departures.groupby("station_id")
        .agg(
            punct_rate=("delay", puncutality_rate),
            avg_delay=("delay", "mean"),
            products=("product", lambda x: set(x)),
            station_name=("station_name", pd.Series.mode),
        )
        .sort_values(["punct_rate"], ascending=False)
        .reset_index()
    )

    punct_rate_per_station = punct_rate_per_station[
        punct_rate_per_station["station_name"] != "Wien Blaasstraße"
    ]

    punct_rate_per_station = punct_rate_per_station[
        punct_rate_per_station["station_name"] != "Wien Rueppgasse"
    ]

    punct_rate_per_station = punct_rate_per_station[
        punct_rate_per_station["station_name"] != "Wien Sternwartestraße"
    ]

    punct_rate_per_station = punct_rate_per_station[
        punct_rate_per_station["station_name"] != "Wien St. Marx/Leberstraße"
    ]

    punct_rate_per_station[["lat", "lon"]] = punct_rate_per_station.apply(
        lambda row: (
            stations[row["station_id"]]["lat"],
            stations[row["station_id"]]["lon"],
        ),
        axis=1,
        result_type="expand",
    )

    fig = px.scatter_mapbox(
        punct_rate_per_station,
        lat="lat",
        lon="lon",
        color="punct_rate",
        color_continuous_scale=["#ff0000", "#ffa700", "#fff400", "#a3ff00", "#2cba00"],
        zoom=10,
        hover_name="station_name",
        mapbox_style="mapbox://styles/msonnberger/cl5p8hn9x000d14kfe0x09188",
        center={"lat": 48.209, "lon": 16.3778},
        labels={"punct_rate": "Punctuality rate"},
    )

    return fig


overall = departures[departures["product"].isin(["u-bahn", "tram", "city-bus"])]
fig_4 = generate_map(overall)
fig_4.write_image("figure-4.png", scale=3)

no_bus = departures[departures["product"].isin(["u-bahn", "tram"])]
fig_5 = generate_map(no_bus)
fig_5.write_image("figure-5.png", scale=3)

only_metro = departures[departures["product"].isin(["u-bahn"])]
fig_6 = generate_map(only_metro)
fig_6.write_image("figure-6.png", scale=3)
