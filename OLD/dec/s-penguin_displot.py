# s-penguin_displot.py

import matplotlib.pyplot as plt
import seaborn as sns

penguins = sns.load_dataset("penguins")

sns.displot(data=penguins, x="flipper_length_mm", hue="species", col="species")

import sys

image_name = sys.argv[0][:-3]  # strip suffix
plt.savefig(f"{image_name}.png")
