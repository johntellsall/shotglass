# plot_releases3.py
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
    strftime('%Y', release_created_at) AS year,
    strftime('%m', release_created_at) AS month,
    COUNT(*) AS count
from github_releases 
where release_created_at >= '2010-01-01'
and release_created_at < '2023-08-01' -- FIXME:
and package = 'tmux' -- <==
group by year_month
"""
releases_df = pd.read_sql_query(sql_releases, conn)

releases_df["year_date"] = pd.to_datetime(releases_df["year"])
releases_df["month_date"] = pd.to_datetime(releases_df["month"], format='%m')

# plot number of monthly releases
sns.jointplot(data=releases_df, x="year_date", y="month_date")

# Format the y-axis tick labels as months
plt.gca().yaxis.set_major_formatter(mdates.DateFormatter('%b'))

plt.title("Alpine Releases -- only tmux")
plt.xlabel("Date")
plt.ylabel("Monthly Release Count")

plt.savefig(image_filename)
print("DONE")
