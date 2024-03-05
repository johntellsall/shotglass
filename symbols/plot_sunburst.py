from pathlib import Path

import pandas as pd
import plotly.express as px

import state

db = state.get_db()

paths_df = pd.read_sql_query("select distinct(path) from symbol", db)

# remove boring paths
# FIXME: merge with goodsource.py?
paths_df = paths_df[~paths_df["path"].str.contains("__init__")]
# TODO: loop and remove other boring directories


data = []
for index, row in paths_df.iterrows():
    parts = Path(row["path"]).parts
    # FIXME: make this easier/obvious
    if parts[:2] == ("lib", "sqlalchemy"):
        parts = tuple(parts[2:])
    elif parts[:2] == ("src", "flask"):
        parts = tuple(parts[2:])

    data.append(parts)

plot_df = pd.DataFrame(data)
print(paths_df.head())
print(paths_df.describe())

fig = px.sunburst(plot_df, path=plot_df.columns)
fig.show()
