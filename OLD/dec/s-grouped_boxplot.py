# s-grouped_boxplot.py

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="ticks", palette="pastel")
plt.figure(figsize=(15, 8))

# Load the example tips dataset
tips = sns.load_dataset("tips")

# Draw a nested boxplot to show bills by day and time
sns.boxplot(
    x="day",
    y="total_bill",
    hue="smoker",
    palette=["m", "g"],
    data=tips,
)
# sns.despine(offset=10, trim=True)

import sys

image_name = sys.argv[0][:-3]  # strip suffix
plt.savefig(f"{image_name}.png")
