import altair as alt
import streamlit as st

import sqlite3

import pandas as pd
import altair as alt
import numpy as np
import pandas as pd

if 0:
    # Create some example data for a heatmap
    data = pd.DataFrame({
        'x': np.repeat(range(5), 5),
        'y': np.tile(range(5), 5),
        'value': np.random.randint(1, 10, size=25)
    })
    heatmap = alt.Chart(data).mark_rect().encode(
        x='x:O',  # Ordinal scale for x-axis
        y='y:O',  # Ordinal scale for y-axis
        color='value:Q'  # Quantitative scale for color
    )
    st.altair_chart(heatmap, use_container_width=True)

"## Shotglass: release heatmap"
"Alpine package releases over time"

conn = sqlite3.connect("../shotglass.db")  # FIXME:

sql_releases = """
select
    strftime('%Y', release_created_at) AS year,
    strftime('%m', release_created_at) AS month,
    strftime('%Y-%m', release_created_at) AS year_month,
    release_created_at AS release_datetime,
    count(*) AS count
from github_releases
group by year, month
"""
data = pd.read_sql_query(sql_releases, conn)

# only render full years worth of data
data = data[data.release_datetime < '2023-01-01']  # FIXME:

data['year'] = pd.to_datetime(data['year'], format='%Y')
data['month'] = pd.to_datetime(data['month'], format='%m')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

if st.checkbox("Show summary"):
    st.write(data.describe())

print(data.dtypes)
# data['month'] = data['month'].dt.strftime('%b')

print(data.head())
print(data.describe())

# T=time, O=ordinal, Q=quantitative
heatmap = alt.Chart(data).mark_rect().encode(
        x=alt.X('year', title='Year', timeUnit='year'),
        y=alt.Y('month:O', sort=None),
        color=alt.Color('count')
    )
st.altair_chart(heatmap, use_container_width=True)

"## 832"
