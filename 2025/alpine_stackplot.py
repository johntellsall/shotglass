# alpine_stackplot.py -- show XX in Alpine releases
# 

import re
import matplotlib.pyplot as plt
import numpy as np

import lib


plt.style.use('_mpl-gallery')

releases = lib.equery_col('select distinct(alpine_release) from sgalpinepackage')
releases.sort(key=lib.cmp_version)


# res = equery(
# f"select pkgname from sgalpinepackage where alpine_release = '{latest_version}'"
# )
# packages = [row[0] for row in res]


def count_fun_packages(packages):
       dull_pat = re.compile(r'(acf-|apache-mod-|aspell-|clang[0-9]|freeswitch-|font-|lua[0-9]|lua-|perl-|py3-|ruby-)')
       count_dull = len([pkg for pkg in packages if dull_pat.match(pkg)])
       count = {"total": len(packages),
              'dull': count_dull,
              'interesting': len(packages) - count_dull}
       return count

release_stats = []
for release in releases:
       packages = lib.equery_col(
              f"select pkgname from sgalpinepackage where alpine_release = '{release}'"
       )
       count = count_fun_packages(packages)
       row = (release, count['interesting'], count['dull'])
       release_stats.append(row)

x = releases
dull = [row[1] for row in release_stats]
interesting = [row[2] for row in release_stats]
y = np.vstack([dull, interesting])

# plot
fig, ax = plt.subplots()

ax.set_title("Alpine Fun/Dull Packages")

ax.stackplot(x, y)
ax.legend(loc='upper right', labels=['dull', 'interesting'])

# ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
#        ylim=(0, 8), yticks=np.arange(1, 8))

# plt.show()
page_path = lib.savefig(plt, __file__)
print(f'{page_path} saved')