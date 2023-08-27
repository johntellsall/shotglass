import altair as alt
import streamlit as st

import sqlite3

import pandas as pd

conn = sqlite3.connect("../shotglass.db")  # FIXME:

sql_releases = """
select
    strftime('%Y-%m', release_created_at) AS year_month,
    COUNT(*) AS count
from github_releases
where release_created_at < '2023-08-01' -- FIXME:
group by year_month
"""
releases_df = pd.read_sql_query(sql_releases, conn)
releases_df["year_month_date"] = pd.to_datetime(releases_df["year_month"])

chart = alt.Chart(releases_df).mark_line().encode(
    x="year_month_date",
    y="count",
)
st.altair_chart(chart, use_container_width=True)
