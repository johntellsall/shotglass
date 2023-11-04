import plotly.express as px
import pandas as pd
import state

db = state.get_db()

paths_df = pd.read_sql_query("select distinct(path) from symbol", db)
print(paths_df.head())

# remove boring paths
paths_df = paths_df[~paths_df['path'].str.contains('__init__')]
# TODO: loop and remove other boring directories
print(paths_df.head())

# df = px.data.tips()
# fig = px.sunburst(df, path=['day', 'time', 'sex'], values='total_bill')
