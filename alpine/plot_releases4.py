# plot_releases4.py
# FIXME: in development
# create table if not exists github_releases (
#         package TEXT, -- not unique
#         release_name TEXT,
#         release_created_at TEXT -- datetime in ISO 8601

import sqlite3
import sys
from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

sns.set_theme(style="white")
image_filename = Path(sys.argv[0]).stem.replace("plot_", "") + ".png"

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

sns.lineplot(x=releases_df["year_month_date"], y=releases_df["count"])

# Format the x-axis tick labels as year (ex "2023")
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.title("Alpine Package Monthly Releases")
plt.xlabel("Year")
plt.ylabel("Count")

plt.savefig(image_filename)
print(releases_df.head())
sys.exit(0)
