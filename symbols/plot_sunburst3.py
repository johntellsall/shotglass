# plot_sunburst3.py -- show directories and source files in a sunburst plot
# FIXME: set slice width based on number of symbols

from pathlib import Path
import sys

import pandas as pd
import plotly.express as px

import state

db = state.get_db()

# TODO: get path from linked file
paths_df = pd.read_sql_query("select distinct(path) from symbol", db)
if paths_df.empty:
    sys.exit("symbol: No paths found in database")

# remove boring paths
# FIXME: merge with goodsource.py?
paths_df = paths_df[~paths_df["path"].str.contains("__init__")]
# TODO: loop and remove other boring directories


data = []
for _index, row in paths_df.iterrows():
    parts = Path(row["path"]).parts
    # FIXME: make this easier/obvious
    if parts[:2] == ("lib", "sqlalchemy"):
        parts = tuple(parts[2:])
    # elif parts[:2] == ('src', 'flask'):
    #     parts = tuple(parts[2:])

    data.append(parts)

plot_df = pd.DataFrame(data)
print(paths_df.head())
print(paths_df.describe())

fig = px.sunburst(plot_df, path=plot_df.columns)
fig.show()
