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
from packaging.version import Version

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


CONFIG = {
    'logscale': False,
    'xmax': (0, 400),
    'ymax': (0, 0.4e8),
}

QUERY_DB = {
    'full': '''
select alpine_release, pkgname, sg_file_num_lines
    from sgalpinepackage
''',
    'fast': '''
select alpine_release, pkgname, sg_file_num_lines
    from sgalpinepackage
    where substr(pkgname, 1, 1) between 'a' and 'd'
    limit 1000
'''}

pkgdata_rows = equery(QUERY_DB['full'])

# Create a structured numpy array with columns: release, pkgname, numlines
dtype = [('release', 'U10'), ('pkgname', 'U100'), ('numlines', 'i4')]
pkgdata = np.array([(parse_release(info[0]), info[1], info[2]) for info in pkgdata_rows], dtype=dtype)

releases = set(pkgdata['release'])
releases = sorted(releases, key=Version)
latest_rel = releases[-1]

# too many releases => simplify
if len(releases) > 10:
    temp_releases = [releases[0], releases[-1]]
    keep = int(len(releases) / 8)
    for i in range(1, len(releases) - 1, keep):
        temp_releases.append(releases[i])
    releases = sorted(temp_releases, key=Version)
    print(f'Keeping {len(releases)} releases: {list(map(str, releases))}')

size_db = update_size_cache(releases)


# plot
fig, ax = plt.subplots()

for rel in releases:
    rel_x = pkgdata['numlines'][pkgdata['release'] == rel]
    rel_y = [get_size(size_db, release=rel, pkgname=pkg) for pkg in pkgdata['pkgname'][pkgdata['release'] == rel]]
    
    style = dict(alpha=0.5)
    if rel == latest_rel:
        style = dict(edgecolor='black')
    ax.scatter(rel_x, rel_y, label=rel, **style)


ax.set_xlabel('Apkbuild complexity')
ax.set_ylabel('Package size')
ax.set_title('Alpine packages over time')
# ax.set_xlim(xmax=400)
# ax.set_ylim(ymax=0.4e8)
if CONFIG['logscale']:
    ax.set_xscale('log')
    ax.set_yscale('log')
else:
    ax.set_xlim(CONFIG['xmax'])
    ax.set_ylim(CONFIG['ymax'])

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