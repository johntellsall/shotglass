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
import shelve


def query_package_sizes(release):
    assert '-' not in release

    package_pat = re.compile(r'<a href="(?P<name>.*?)-(?P<version>\d.*?)-(?P<release>.*?).apk">.*?</a>\s+(?P<datestr>\S+ \S+)\s+(?P<size>\d+[A-Z]?)')
    url = f'https://dl-cdn.alpinelinux.org/alpine/v{release}/main/x86_64/'
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

output_size_notfound = 0

def get_size(sizedb, release, pkgname):
    assert '-' not in release
    if info := sizedb.get(release, {}).get(pkgname):
        return calc_size(info['size'])
    print(f'{release} {pkgname} not found in size db')
    global output_size_notfound
    output_size_notfound += 1
    return 0


def parse_release(verstring):
    "Ex: '3.9-release' -> '3.9'"
    return verstring.split('-')[0]



plt.style.use('_mpl-gallery')


res = equery('''
select alpine_release, pkgname, sg_file_num_lines
             from sgalpinepackage
             where substr(pkgname, 1, 1) between 'a' and 'g'
             -- limit 10
''')


def update_size_cache(releases):
    shelf_filename = "package_size.shelve"

    with shelve.open(shelf_filename) as shelf:
        package_size_dict = shelf.get("package_size_dict", {})
        releases = set(releases)
        for rel in releases:
            if rel not in package_size_dict:
                print(f"{rel}: Fetching package sizes...")
                package_size_dict[rel] = query_package_sizes(rel)
                print(f"{rel}: {len(package_size_dict[rel])} packages fetched")
        shelf["package_size_dict"] = package_size_dict
    return package_size_dict


releases = set(parse_release(info[0]) for info in res)
size_db = update_size_cache(releases)

pkgnames = [info[1] for info in res]

x = [item[2] for item in res]
y = [get_size(size_db, release=parse_release(item[0]), pkgname=item[1]) for item in res]

# size and color:
# sizes = np.random.uniform(15, 80, len(x))

# NOTE: janky: version 3.12 should be after 3.9
colors = [float(parse_release(info[0])) for info in res]

if len(pkgnames) < 20:
    pprint(dict(x=x, y=y, sizes=sizes, colors=colors))

# plot
fig, ax = plt.subplots()

# ax.scatter(x, y, s=sizes, c=colors, vmin=3.7, vmax=4.0)
ax.scatter(x, y, c=colors, vmin=3.7, vmax=4.0)

# ax.set(xlim=(0, 100), xticks=np.arange(1, 8),
#        ylim=(0, 10), yticks=np.arange(1, 8))

imgpath = __file__.replace('.py', '.png')
plt.savefig(imgpath)

print(f'{output_size_notfound} packages not found in size db')

# CREATE TABLE sgalpinepackage (
#         id INTEGER NOT NULL, 
#         alpine_release VARCHAR NOT NULL, 
#         pkgname VARCHAR NOT NULL, 
#         pkgdesc VARCHAR NOT NULL, 
#         pkgver VARCHAR NOT NULL, 
#         pkgrel VARCHAR NOT NULL, 
#         sg_file_num_lines INTEGER, 
#         PRIMARY KEY (id)