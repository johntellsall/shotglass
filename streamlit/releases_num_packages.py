
# create table if not exists github_releases (
#         package TEXT, -- not unique
#         release_name TEXT,
#         release_created_at TEXT -- datetime in ISO 8601

# import altair as alt
import streamlit as st
import pandas as pd

import sqlite3


# "## Shotglass: release heatmap"
"Alpine package releases over time"

conn = sqlite3.connect("../shotglass.db")  # FIXME:

# strftime('%Y-%m', release_created_at) AS year_month,
sql_releases = """
select
    package,
    release_created_at AS release_datetime
from github_releases
"""
data = pd.read_sql_query(sql_releases, conn)

# only render full years worth of data
# data = data[data.release_datetime < '2023-01-01']  # FIXME:

# data['year'] = pd.to_datetime(data['year'], format='%Y')
# data['month'] = pd.to_datetime(data['month'], format='%m')

# print(data.dtypes)
# print(data.head())
# print(data.describe())

"## Number of releases over time"
# st.line_chart(data, y='count')
"---"

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

if st.checkbox("Show summary"):
    st.write(data.describe())
