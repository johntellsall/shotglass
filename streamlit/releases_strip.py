# releases_strip.py -- show Alpine releases over time as points

import altair as alt
import streamlit as st

import sqlite3

import pandas as pd
import numpy as np
import pandas as pd

if 1:
    # Create some example data for a heatmap
    from vega_datasets import data

    source = data.cars()
    print(source.info())
    print(source.columns)
    # print(source.loc['Horsepower'])

    plot = alt.Chart(source).mark_tick().encode(
        x='Weight_in_lbs:Q',
        y='Cylinders:O'
    )
    st.altair_chart(plot, use_container_width=True)

conn = sqlite3.connect("../shotglass.db")  # FIXME:


sql_releases = """
select
    package,
    release_created_at
from github_releases
where package='tmux'
"""
data = pd.read_sql_query(sql_releases, conn)
print(data.head())
assert 0

# only render full years worth of data
data = data[data.release_datetime < '2023-01-01']  # FIXME:

data['year'] = pd.to_datetime(data['year'], format='%Y')
data['month'] = pd.to_datetime(data['month'], format='%m')
print(data.dtypes)
# data['month'] = data['month'].dt.strftime('%b')

print(data.head())

heatmap = alt.Chart(data).mark_rect().encode(
        x='year:T',
        y=alt.Y('month:T', sort=None),
        color='count:Q'  # Quantitative scale for color
    )
st.altair_chart(heatmap, use_container_width=True)
