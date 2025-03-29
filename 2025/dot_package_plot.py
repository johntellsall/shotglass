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


output_size_notfound = 0


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


def get_size(sizedb, release, pkgname):
    assert '-' not in release
    if info := sizedb.get(release, {}).get(pkgname):
        return calc_size(info['size'])
    # print(f'{release} {pkgname} not found in size db')
    global output_size_notfound
    output_size_notfound += 1
    return 0


def parse_release(verstring):
    "Ex: '3.9-release' -> '3.9'"
    return verstring.split('-')[0]


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


res = equery('''
select alpine_release, pkgname, sg_file_num_lines
             from sgalpinepackage
             -- where substr(pkgname, 1, 1) between 'a' and 'g'
             -- limit 10
''')



releases = set(parse_release(info[0]) for info in res)
size_db = update_size_cache(releases)

x = [item[2] for item in res]
y = [get_size(size_db, release=parse_release(item[0]), pkgname=item[1]) for item in res]

# NOTE: janky: version 3.12 should be after 3.9
colors = [float(parse_release(info[0])) for info in res]


# plot
fig, ax = plt.subplots()

for rel in releases:
    rel_x = [x[i] for i in range(len(x)) if parse_release(res[i][0]) == rel]
    rel_y = [y[i] for i in range(len(y)) if parse_release(res[i][0]) == rel]
    ax.scatter(rel_x, rel_y, label=rel)


ax.set_xlabel('Apkbuild complexity')
ax.set_ylabel('Package size')
ax.set_title('Alpine packages over time')
# ax.set_xlim(xmax=400)
# ax.set_ylim(ymax=0.4e8)
ax.set_xscale('log')
ax.set_yscale('log')
ax.legend()
ax.grid(True)

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