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

conn = sqlite3.connect("../shotglass.db")  # FIXME:

# strftime('%m', release_created_at) AS month,

sql_releases = """
select
    strftime('%Y', release_created_at) AS year,
    release_created_at AS release_datetime,
    count(*) AS count
from github_releases
where release_created_at < '2023-08-01' -- FIXME:
group by year, month
"""
releases_df = pd.read_sql_query(sql_releases, conn)


# Group data by month and calculate the sum of values
# monthly_data = data.groupby(data['date'].dt.to_period('M')).sum().reset_index()

# Convert month numbers to datetime objects
# releases_df['release_created_at'] = pd.to_datetime(releases_df['release_created_at'], format='%m')
# .. then to month names (ex: "Jan")
# releases_df['month'] = releases_df['month'].dt.strftime('%b')
print(releases_df.head())


chart = alt.Chart(releases_df).mark_rect().encode(
    x=alt.X("year"),
    # y=alt.Y('month:N', sort=None),  # Use ordinal scale for month names
    y=alt.Y('release_created_at:T'),
    color='count:Q'  # Quantitative scale for color
).properties(
    title="Alpine-GitHub Releases",
)
st.altair_chart(chart, use_container_width=True)
