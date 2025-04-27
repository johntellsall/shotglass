

# ----------------------------------------# load libraries
import squarify # pip install squarify (algorithm for treemap)
import matplotlib.pyplot as plt
from pypalettes import load_cmap
import pandas as pd
# from highlight_text import fig_text

PlotFile = 'extreemap.png'

# set a higher resolution
plt.rcParams['figure.dpi'] = 300

df = pd.read_csv("https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/simple-treemap.csv")
df

# create a figure
fig, ax = plt.subplots(figsize=(10,10))
ax.set_axis_off()

# add treemap
squarify.plot(
   sizes=df["value"],
   label=df["name"],
   ax=ax
)

# display plot
# plt.show()

# create a color palette
cmap = load_cmap('Acadia')
category_codes, unique_categories = pd.factorize(df['parent'])
colors = [cmap(code) for code in category_codes]

# create a treemap
fig, ax = plt.subplots(figsize=(10,10))
ax.set_axis_off()
squarify.plot(
   sizes=df["value"],
   label=df["name"],
   color=colors,
   text_kwargs={'color':'white'},
   pad=True,
   ax=ax
)

# create a color palette
cmap = load_cmap('Acadia')
category_codes, unique_categories = pd.factorize(df['parent'])
colors = [cmap(code) for code in category_codes]

# customize the labels
labels = [f"{name} ({parent[5:]})\n{value}" for name, value, parent in zip(df['name'], df['value'], df['parent'])]

# create a treemap
fig, ax = plt.subplots(figsize=(10,10))
ax.set_axis_off()
squarify.plot(
   sizes=df["value"],
   label=labels,
   color=colors,
   text_kwargs={
      'color':'white',
      'fontsize':8,
      'fontweight':'bold'
   },
   pad=True,
   ax=ax
)

# create a color palette
cmap = load_cmap('Acadia')
category_codes, unique_categories = pd.factorize(df['parent'])
colors = [cmap(code) for code in category_codes]

# customize the labels
labels = [f"{name}\n{parent[5:]}\n{value}" for name, value, parent in zip(df['name'], df['value'], df['parent'])]

# create a treemap
fig, ax = plt.subplots(figsize=(10,8))
ax.set_axis_off()
squarify.plot(
   sizes=df["value"],
   label=labels,
   color=colors,
   text_kwargs={
      'color':'white',
      'fontsize':9,
      'fontweight':'bold'
   },
   pad=True,
   ax=ax
)

if 0:
   # add a title and legend
   text = """<Treemap of a Simple Dataset>
   Each color represents a category: <Dataviz>, <Sales> and <DevOps>.
   Each rectangle represents a person.
   """
   fig_text(
      x=0.133, y=0.98,
      s=text,
      color="black",
      highlight_textprops=[
         {"fontsize": 20, 'fontweight': 'bold'},
         {"color": cmap(0), 'fontweight': 'bold'},
         {"color": cmap(2), 'fontweight': 'bold'},
         {"color": cmap(1), 'fontweight': 'bold'},
      ],
      fontsize=14,
      ha='left'
   )

fig.savefig(PlotFile, bbox_inches='tight', dpi=300)
print(f"Figure saved as {PlotFile}")