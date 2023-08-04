import sqlite3

import pandas as pd
import seaborn as sns

sns.set_theme(style="white")
conn = sqlite3.connect("../shotglass.db")
releases_df = pd.read_sql_query("select * from package_releases", conn)
assert 0, releases_df.head()

# Plot miles per gallon against horsepower with other semantics
plt = sns.relplot(
    x="horsepower",
    y="mpg",
    hue="origin",
    size="weight",
    sizes=(40, 400),
    alpha=0.5,
    palette="muted",
    height=6,
    data=mpg_df,
)

# render to file
plt.savefig("demo_scatter.png")
print("DONE")
