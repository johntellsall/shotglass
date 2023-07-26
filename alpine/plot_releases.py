# plot_releases.py -- plot package releases from database

import json
import sqlite3
import pandas as pd
import seaborn as sns

sns.set_theme(style="white")

conn = sqlite3.connect("../shotglass.db")  # FIXME:
releases_df = pd.read_sql_query(
    "select package,releases_json from package_releases", conn)

# Release Keys:
# ['assets', 'assets_url', 'author', 'body', 'created_at', 'draft', 'html_url',
# 'id', 'name', 'node_id', 'prerelease', 'published_at', 'tag_name',
# 'tarball_url', 'target_commitish', 'upload_url', 'url', 'zipball_url']

for index, row in releases_df.iterrows():
    package = row.package
    releases = json.loads(row.releases_json)
    print(f"{package=}: {len(releases)} releases")
    for rel in releases:
        print(f"- {rel['name']} {rel['tag_name']} {rel['created_at']}")

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
# plt.savefig("demo_scatter.png")
# print('DONE')
