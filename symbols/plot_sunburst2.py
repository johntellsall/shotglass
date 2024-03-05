# FIXME: BROKEN: doesn't show paths with parent directories

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px

import state

db = state.get_db()

sql = """
select f.path as path, count(*) as count
from symbol s, file f
where s.file_id = f.id
group by f.path
order by f.path
"""
paths_df = pd.read_sql_query(sql, db)
if len(paths_df) <= 1:
    sys.exit("No data")

if 1:
    print(paths_df.head())
    print(paths_df.describe())

# simplify paths for a nicer plot
# - strip common prefix
# FIXME: make this more flexible
data = []
for index, row in paths_df.iterrows():
    parts = Path(row["path"]).parts
    if parts[:2] == ("lib", "sqlalchemy"):
        parts = tuple(parts[2:])
    elif parts[:2] == ("src", "flask"):
        parts = tuple(parts[2:])
    # data.append([parts, row['count']])
    data.append([parts])


plot_df = pd.DataFrame(data, columns=["path"])
print(paths_df.head())
print(paths_df.describe())

fig = px.sunburst(plot_df, path=plot_df.columns)
fig.show()
