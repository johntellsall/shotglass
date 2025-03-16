# alpine_stackplot.py -- show XX in Alpine releases
# 

import matplotlib.pyplot as plt
import numpy as np

import lib


plt.style.use('_mpl-gallery')

releases = lib.equery_col('select distinct(alpine_release) from sgalpinepackage')
releases.sort(key=lib.cmp_version)
assert 0, releases

# make data
x = np.arange(0, 10, 2)
ay = [1, 1.25, 2, 2.75, 3]
by = [1, 1, 1, 1, 1]
cy = [2, 1, 2, 1, 2]
y = np.vstack([ay, by, cy])

# plot
fig, ax = plt.subplots()

ax.stackplot(x, y)

ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
       ylim=(0, 8), yticks=np.arange(1, 8))

# plt.show()
page_path = lib.savefig(plt, __file__)
print(f'{page_path} saved')