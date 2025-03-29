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
import re
import matplotlib.pyplot as plt
import numpy as np
import requests

from lib import equery, savefig


def query_package_sizes():
    # "<a href="a52dec-dev-0.7.4-r7.apk">a52dec-dev-0.7.4-r7.apk</a>    20-Dec-2018 10:39     23K\r\n"
    package_pat = re.compile(r'<a href="(?P<name>.*?)-(?P<version>\d.*?)-(?P<release>.*?).apk">.*?</a>\s+(?P<datestr>\S+ \S+)\s+(?P<size>\d+[A-Z]?)')
    url = 'https://dl-cdn.alpinelinux.org/alpine/v3.9/main/x86_64/'
    page = requests.get(url)
    packages = package_pat.finditer(page.text)
    package_dict = {m.group('name'): m.groupdict() for m in packages}
    return package_dict
    

def calc_size(size_str):
    "handle suffixes like K, M, G"
    multipliers = {'K':1024, 'M':1024**2, 'G':1024**3}
    if mult := multipliers.get(size_str[-1]):
        return int(size_str[:-1]) * mult
    return int(size_str)

def get_size(sizedb, pkgname):
    if info := sizedb.get(pkgname):
        return calc_size(info['size'])
    print(f'{pkgname} not found in size db')
    return 0



plt.style.use('_mpl-gallery')

package_size_dict = query_package_sizes()

res = equery('''
select alpine_release, pkgname, sg_file_num_lines
             from sgalpinepackage
             where alpine_release = '3.9-stable'
             limit 10
''')

pkgnames = [info[1] for info in res]

x = [item[2] for item in res]
y = [get_size(package_size_dict, name) for name in pkgnames]
assert 0, y
# y = 4 + np.random.normal(0, 2, len(x))
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