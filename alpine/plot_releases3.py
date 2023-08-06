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
from matplotlib import pyplot

sns.set_theme(style="white")
image_filename = Path(sys.argv[0]).stem.replace("plot_", "") + ".png"

conn = sqlite3.connect("../shotglass.db")  # FIXME:

if 0:
    penguins = sns.load_dataset("penguins")
    sns.jointplot(data=penguins, x="bill_length_mm", y="bill_depth_mm")
    pyplot.savefig(image_filename)
    print(" penguins")
sys.exit(0)

# FIXME: plot only complete months
sql_releases = """
select
    strftime('%Y-%m', release_created_at) AS year_month,
    COUNT(*) AS count
from github_releases 
where release_created_at >= '2010-01-01'
and release_created_at < '2023-08-01' -- FIXME:
and package = 'tmux'
group by year_month
"""
releases_df = pd.read_sql_query(sql_releases, conn)

releases_df["year_month"] = pd.to_datetime(releases_df["year_month"])

# missing counts are plotted as zero
# XXX doesn't work
# releases_df['year_month'] = releases_df['year_month'].fillna(0)

print(releases_df)

# plot number of monthly releases
plt = sns.relplot(x="year_month", y="count", data=releases_df, marker="o")

if 1:
    # resample the data over 3 months and calculate the mean
    releases_df.set_index("year_month", inplace=True)
    resampled_data = releases_df.resample("3M").mean()

    # add a line plot with x-axis as the resampled date and y-axis as the mean value
    plt.map(
        sns.lineplot,
        data=resampled_data,
        x=resampled_data.index,
        y="count",
        color="red",
    )

pyplot.title("Alpine Package -- only one")
pyplot.xlabel("Date")
pyplot.ylabel("Monthly Release Count")

# render to file
plt.savefig(label)
print("DONE")
