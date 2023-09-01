# releases_strip.py -- show Alpine releases over time as points

import altair as alt
import streamlit as st

import sqlite3

import pandas as pd
import numpy as np
import pandas as pd

    # Create some example data for a heatmap
# from vega_datasets import data

# source = data.cars()
# print(source.info())
# print(source.columns)
# # print(source.loc['Horsepower'])

# plot = alt.Chart(source).mark_tick().encode(
#     x='Weight_in_lbs:Q',
#     y='Cylinders:O'
# )
# st.altair_chart(plot, use_container_width=True)

conn = sqlite3.connect("../shotglass.db")  # FIXME:

sql_releases = """
select
    package,
    release_created_at
from github_releases
where package like 't%' -- FIXME:
"""
data = pd.read_sql_query(sql_releases, conn)

# only "recent", and strip this partial year
data['release_created_at'] = pd.to_datetime(data['release_created_at'])
data = data[data.release_created_at >= '2010-01-01']
data = data[data.release_created_at < '2023-01-01']

print(data.describe())

# Reset the index and treat it as a data column
data.reset_index(drop=True, inplace=True)

print(data.head())

# suffix: T=time, Q=quantitative, O=ordinal, N=nominal
plot = alt.Chart(data).mark_tick().encode(
    y='package:O',
    x='release_created_at:T',
)
st.altair_chart(plot, use_container_width=True)

assert 0

# # only render full years worth of data
# data = data[data.release_datetime < '2023-01-01']  # FIXME:

# data['year'] = pd.to_datetime(data['year'], format='%Y')
# data['month'] = pd.to_datetime(data['month'], format='%m')
# print(data.dtypes)
# # data['month'] = data['month'].dt.strftime('%b')

# print(data.head())

# heatmap = alt.Chart(data).mark_rect().encode(
#         x='year:T',
#         y=alt.Y('month:T', sort=None),
#         color='count:Q'  # Quantitative scale for color
#     )
# st.altair_chart(heatmap, use_container_width=True)
