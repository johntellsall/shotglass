# dot_package_plot.py
# 
# Alpine packages:
# - plot one dot per package
#    - X = APKGBUILD size
#    - Y = APK size
#    - color = release
#
# Resources
# - list of packages with size
#    - https://dl-cdn.alpinelinux.org/alpine/

from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np

from lib import equery, savefig


plt.style.use('_mpl-gallery')

res = equery('''
select alpine_release, pkgname, sg_file_num_lines
             from sgalpinepackage
             limit 10
''')

x = [item[2] for item in res]

y = 4 + np.random.normal(0, 2, len(x))
# size and color:
sizes = np.random.uniform(15, 80, len(x))
colors = np.random.uniform(15, 80, len(x))
pprint(dict(x=x, y=y, sizes=sizes, colors=colors))

# plot
fig, ax = plt.subplots()

ax.scatter(x, y, s=sizes, c=colors, vmin=0, vmax=100)

ax.set(xlim=(0, 100), xticks=np.arange(1, 8),
       ylim=(0, 10), yticks=np.arange(1, 8))

imgpath = __file__.replace('.py', '.png')
plt.savefig(imgpath)


# CREATE TABLE sgalpinepackage (
#         id INTEGER NOT NULL, 
#         alpine_release VARCHAR NOT NULL, 
#         pkgname VARCHAR NOT NULL, 
#         pkgdesc VARCHAR NOT NULL, 
#         pkgver VARCHAR NOT NULL, 
#         pkgrel VARCHAR NOT NULL, 
#         sg_file_num_lines INTEGER, 
#         PRIMARY KEY (id)