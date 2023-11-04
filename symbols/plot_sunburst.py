import plotly.express as px
import pandas as pd
import state
from pathlib import Path

db = state.get_db()

paths_df = pd.read_sql_query("select distinct(path) from symbol", db)

# remove boring paths
paths_df = paths_df[~paths_df['path'].str.contains('__init__')]
# TODO: loop and remove other boring directories

data = []
for index, row in paths_df.iterrows():
    parts = Path(row['path']).parts
    if parts[:2] == ('lib', 'sqlalchemy'):
        parts = tuple(parts[2:])
    data.append(parts)

plot_df = pd.DataFrame(data)
print(paths_df.head())
print(paths_df.describe())

print(plot_df.head())
print(plot_df.describe())

# fig = px.sunburst(df, path=['day', 'time', 'sex'], values='total_bill')
fig = px.sunburst(plot_df, path=list(range(3)))
fig.show()