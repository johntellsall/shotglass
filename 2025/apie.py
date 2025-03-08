# apie.py # everyone loves pie
# 

import matplotlib.pyplot as plt
import numpy as np

from lib import equery1

res = equery1('select count(*) from sgalpinepackage')
assert 0, res

fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

recipe = ["375 g flour",
          "75 g sugar",
          "250 g butter",
          "300 g berries"]

data = [float(x.split()[0]) for x in recipe]
ingredients = [x.split()[-1] for x in recipe]


def func(pct, allvals):
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    return f"{pct:.1f}%\n({absolute:d} g)"


wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                  textprops=dict(color="w"))

ax.legend(wedges, ingredients,
          title="Ingredients",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

plt.setp(autotexts, size=8, weight="bold")

ax.set_title("Matplotlib bakery: A pie")

from pathlib import Path
imgpath = Path(__file__).with_suffix('.png')
plt.savefig(imgpath)
print(f'{imgpath}: saved')

# from matplotlib import image
# preview = image.imread(imgpath)

# CREATE TABLE sgalpinepackage (
#         id INTEGER NOT NULL, 
#         alpine_release VARCHAR NOT NULL, 
#         pkgname VARCHAR NOT NULL, 
#         pkgdesc VARCHAR NOT NULL, 
#         pkgver VARCHAR NOT NULL, 
#         pkgrel VARCHAR NOT NULL, 
#         sg_complexity INTEGER, 
#         sg_len_install INTEGER, 
#         sg_len_parse_funcs INTEGER, 
#         sg_len_subpackages INTEGER, 