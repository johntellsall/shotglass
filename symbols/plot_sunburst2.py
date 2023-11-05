import plotly.express as px
import pandas as pd
import state
from pathlib import Path

db = state.get_db()

sql = """
select f.path as path, count(*) as count
from symbol s, file f
where s.file_id = f.id
order by path
"""
paths_df = pd.read_sql_query(sql, db)
if len(paths_df) <= 1:
    print("No data")
    assert 0
if 1:
    print(paths_df.head())
    print(paths_df.describe())
    breakpoint()
#     assert 0

# remove boring paths
# FIXME: merge with goodsource.py?
paths_df = paths_df[~paths_df['path'].str.contains('__init__')]
# TODO: loop and remove other boring directories


# simplify paths for a nicer plot
# FIXME: make this more flexible
data = []
for index, row in paths_df.iterrows():
    parts = Path(row['path']).parts
    if parts[:2] == ('lib', 'sqlalchemy'):
        parts = tuple(parts[2:])
    elif parts[:2] == ('src', 'flask'):
        parts = tuple(parts[2:])
    data.append([parts, row['count']])
    breakpoint()

plot_df = pd.DataFrame(data, columns=['path', 'count'])
print(paths_df.head())
print(paths_df.describe())
# breakpoint()
fig = px.sunburst(plot_df, path=plot_df.columns, values='count')
fig.show()