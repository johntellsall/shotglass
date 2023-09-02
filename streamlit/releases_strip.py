# releases_strip.py -- show Alpine releases over time

import altair as alt
import streamlit as st

import sqlite3

import pandas as pd

conn = sqlite3.connect("../shotglass.db")  # FIXME:

sql_releases = """
select
    package,
    release_created_at
from github_releases
"""
data = pd.read_sql_query(sql_releases, conn)

# only "recent", and strip this partial year
data['release_created_at'] = pd.to_datetime(data['release_created_at'])
data = data[data.release_created_at >= '2010-01-01']
data = data[data.release_created_at < '2023-01-01']  # FIXME:

print(data.describe())
print(data.head())

# suffix: T=time, Q=quantitative, O=ordinal, N=nominal
plot = alt.Chart(data).mark_tick().encode(
    y='package:O',
    x=alt.X('release_created_at:T', title='Release Date'),
)
st.altair_chart(plot, use_container_width=True)
