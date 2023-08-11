# plot_releases4.py -- line plot of total monthly releases
#
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

if 0: # DEMO
    # bin-based visualization of the joint distribution: histogram
    penguins = sns.load_dataset("penguins")
    sns.jointplot(data=penguins, x="bill_length_mm", y="bill_depth_mm", kind="hist")
    plt.savefig(image_filename)
    sys.exit(0)

if 1: # DEMO 2: Heatmap
    import numpy as np
    from string import ascii_letters

    # Generate a large random dataset
    rs = np.random.RandomState(33)
    d = pd.DataFrame(data=rs.normal(size=(100, 26)),
                    columns=list(ascii_letters[26:]))

    # Compute the correlation matrix
    corr = d.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})
    plt.savefig(image_filename)
    sys.exit(0)

conn = sqlite3.connect("../shotglass.db")  # FIXME:

sql_releases = """
select
    strftime('%Y-%m', release_created_at) AS year_month,
    strftime('%Y', release_created_at) AS year,
    strftime('%m', release_created_at) AS month,
    COUNT(*) AS count
from github_releases 
-- where release_created_at between '2010-01-01' and '2023-08-01' -- FIXME:
where release_created_at between '2010-01-01' and '2023-01-01' -- FIXME:
group by year_month
"""
releases_df = pd.read_sql_query(sql_releases, conn)
# releases_df["year_date"] = pd.to_datetime(releases_df["year"])

sns.jointplot(data=releases_df, x="year", y="month", kind="hist")

# Format the x-axis tick labels as year (ex "2023")
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.title("Alpine Package Monthly Releases")
plt.xlabel("Year")
plt.xlim(2010, 2023)
plt.ylabel("Month")

# # Convert date values to numerical values
# num_dates = mdates.date2num(df['date'])
# # Set the y-axis limits as dates
# plt.ylim(min(num_dates), max(num_dates))

plt.savefig(image_filename)
print(releases_df.head())
sys.exit(0)
