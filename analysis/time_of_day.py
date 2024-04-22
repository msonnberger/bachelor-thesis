import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def puncutality_rate(delays):
    return 1 - len([delay for delay in delays if delay > 180]) / delays.size


departures = pd.read_csv("../collection/departures.csv")
departures = departures.fillna(0)
departures = departures[departures["product"].isin(["u-bahn", "tram", "city-bus"])]

departures["when"] = pd.to_datetime(departures["when"])
departures["planned_when"] = pd.to_datetime(departures["planned_when"])
departures["hour"] = departures["planned_when"].dt.hour
departures["weekday"] = departures["planned_when"].dt.day_of_week < 5


def generate_plot(grouped):
    hours = grouped["hour"]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=hours, y=grouped["punct_rate"], name="punctuality rate"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=hours, y=grouped["departures"], name="departures"),
        secondary_y=True,
    )

    fig.update_xaxes(title_text="hour", dtick=1)

    # Set y-axes titles
    fig.update_yaxes(title_text="punctuality rate", secondary_y=False)
    fig.update_yaxes(title_text="departures", secondary_y=True)

    return fig


grouped = departures.groupby(["hour", "weekday"], as_index=False).agg(
    punct_rate=("delay", puncutality_rate),
    avg_delay=("delay", "mean"),
    departures=("hour", "size"),
)

weekday = grouped[grouped["weekday"] == True]
fig_7 = generate_plot(weekday)
fig_7.write_image("figure-7.png", scale=3)

weekend = grouped[grouped["weekday"] == False]
fig_8 = generate_plot(weekend)
fig_8.write_image("figure-8.png", scale=3)
