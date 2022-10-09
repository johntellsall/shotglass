# Import seaborn
import seaborn as sns
import matplotlib.pyplot as plt

# Apply the default theme
# sns.set_theme()
sns.set(rc={"figure.dpi": 300, "savefig.dpi": 300})
sns.set_context("notebook")
sns.set_style("ticks")

# Load an example dataset
tips = sns.load_dataset("tips")


# Create a visualization
sns.relplot(
    data=tips,
    x="total_bill",
    y="tip",
    col="time",
    hue="smoker",
    style="smoker",
    size="size",
)

plt.savefig("plot.png")
