# plot_github_releases.py
# FIXME: in development
# FIXME: how to note Packages with zero Releases?

# create table if not exists github_releases (
#         package TEXT, -- not unique
#         release_name TEXT,
#         release_created_at TEXT -- datetime in ISO 8601

import sqlite3
import sys

import pandas as pd
import seaborn as sns
from matplotlib import pyplot

sns.set_theme(style="white")
label = "github_releases.png"
conn = sqlite3.connect("../shotglass.db")  # FIXME:

sql_releases = """
select
    strftime('%Y-%m', release_created_at) AS year_month,
    COUNT(*) AS count
from github_releases 
where release_created_at >= '2010-01-01'
group by year_month
"""
releases_df = pd.read_sql_query(
    sql_releases, conn
)
releases_df['year_month'] = pd.to_datetime(releases_df['year_month'])

print(releases_df.describe())
print(releases_df.head())
print(releases_df.tail())

plt = sns.relplot(x='year_month', y="count", data=releases_df)


# Set 'date' column as the DataFrame index (optional, but can be helpful for time-based resampling)
releases_df.set_index('year_month', inplace=True)

# Resample the data over 3 months and calculate the mean
resampled_data = releases_df.resample('3M').mean()

# Create a line plot with x-axis as the resampled date and y-axis as the mean value
plt.map(sns.lineplot, data=resampled_data, x=resampled_data.index, y='count', color='red')
# plt.map(sns.lineplot, 'year_month', 'count', color='r', errorbar=None, lw=1)

pyplot.xlabel('Date')
pyplot.ylabel('Monthly Releases')

# render to file
plt.savefig(label)
print('DONE')
