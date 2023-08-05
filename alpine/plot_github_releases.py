# plot_github_releases.py
# FIXME: in development

# create table if not exists github_releases (
#         package TEXT, -- not unique
#         release_name TEXT,
#         release_created_at TEXT -- datetime in ISO 8601

import sqlite3
import sys

import pandas as pd
import seaborn as sns

sns.set_theme(style="white")
label = "github_releases.png"


tips = sns.load_dataset("tips")
print(tips.head())
plt = sns.relplot(data=tips, x="total_bill", y="tip", hue="day")
plt.savefig(label)
sys.exit(0)


conn = sqlite3.connect("../shotglass.db")  # FIXME:
sql_releases = "select package, release_created_at from github_releases limit 3"
sql_package_release_count = """
    select package, count(package) as release_count
    from github_releases
    group by package
"""
releases_df = pd.read_sql_query(
    sql_package_release_count, conn
)
assert 0, releases_df.head()
if 0: # FIXME: later
    releases_df['release_created_at'] = pd.to_datetime(releases_df['release_created_at'])

plt = sns.relplot(
    y="release_count",
    data=releases_df
)
# # Plot miles per gallon against horsepower with other semantics
# plt = sns.relplot(
#     x="horsepower",
#     y="mpg",
#     hue="origin",
#     size="weight",
#     sizes=(40, 400),
#     alpha=0.5,
#     palette="muted",
#     height=6,
#     data=mpg_df,
# )

# # render to file
plt.savefig(label)
print('DONE')
