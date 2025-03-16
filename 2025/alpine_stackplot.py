# alpine_stackplot.py -- show XX in Alpine releases
# 

import matplotlib.pyplot as plt
import numpy as np

import lib


plt.style.use('_mpl-gallery')

releases = lib.equery_col('select distinct(alpine_release) from sgalpinepackage')
releases.sort(key=lib.cmp_version)

num_packages_per_release = lib.equery('''
select alpine_release, count(*)
from sgalpinepackage
group by alpine_release
''')
# assert 0, num_packages_per_release
# make data
# x = np.arange(0, 10, 2)
x = releases
if 0:
       ay = [1, 1.25, 2]
       by = [1, 1, 1]
       cy = [2, 1, 2]
       y = np.vstack([ay, by, cy])
else:
       y = [row[1] for row in num_packages_per_release]

# plot
fig, ax = plt.subplots()

ax.stackplot(x, y)

# ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
#        ylim=(0, 8), yticks=np.arange(1, 8))

# plt.show()
page_path = lib.savefig(plt, __file__)
print(f'{page_path} saved')