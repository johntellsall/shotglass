from collections import defaultdict
from pprint import pprint
import sys
import matplotlib.pyplot as plt
import numpy as np
from lib import equery
from packaging import version


# vegetables = ["cucumber", "tomato", "lettuce", "asparagus",
#               "potato", "wheat", "barley"]
# farmers = ["Joe", "Bros.", "Smith",
#            "Agrifun", "Organic", "Ltd.", "Corp."]

harvest = np.array([[0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                    [2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0],
                    [1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0],
                    [0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0],
                    [0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0],
                    [1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1],
                    [0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3]])

title = "Package Versions over Time"

sql = """
SELECT a.alpine_release, a.pkgname, a.pkgver
FROM sgalpinepackage a
JOIN debianpopcontest d 
ON a.pkgname = d.name 
WHERE a.alpine_release in (
'3.0-stable', '3.5-stable', '3.10-stable', '3.15-stable', '3.21-stable')
AND d.rank <= 500
AND a.pkgname not in ('dash', 'dpkg', 'debian-archive-keyring', 'debootstrap')
ORDER BY a.alpine_release DESC, d.rank
"""

def grid():

    data = equery(sql)

    # X: Alpine releases
    releases = list(set(row[0] for row in data))
    def version_key(rel):
        "parse '1.23-stable' => 1.23"
        return version.parse(rel.split('-')[0])
    releases.sort(key=version_key)
    print(releases)

    # Y: package names
    # - order: earlier = higher popularity rank
    pkgnames = []
    max_packages = 10
    for _,pkgname,_ in data:
        if pkgname not in pkgnames:
            pkgnames.append(pkgname)
        if len(pkgnames) >= max_packages:
            break
    print(pkgnames)

    info = defaultdict(lambda: '-')
    for rel, pkgname, pkgver in data:
        info[(rel, pkgname)] = pkgver

    # grid = np.full((len(pkgnames), len(releases)), '-', dtype=object)
    # grid = np.full((len(pkgnames), len(releases)), 0, dtype=float)
    # for rel, pkgname, pkgver in data:
    #     if pkgname in pkgnames:
    #         row = pkgnames.index(pkgname)
    #         col = releases.index(rel)
    #         grid[row, col] = pkgver
    grid = harvest

    # for rel, pkgname, pkgver in data:
    #     idx = pkgnames.index(pkgname)
    #     if idx >= 0:
    #         grid[]
    #     if pkgname not in pkgnames:
    #         continue
    #         info[rel, pkgname] = pkgver
    # pprint(info)

    xt_style = dict(rotation=45, ha="right", rotation_mode="anchor")
    t_style = dict(ha="center", va="center", color="white", fontweight="bold")

    fig, ax = plt.subplots()

    # Loop over data dimensions and create text annotations.
    for pi,pkgname in enumerate(pkgnames):
        for ri,release in enumerate(releases):
            pkg_version = info.get((release, pkgname), '-')
            text = ax.text(x=ri, y=pi, s=pkg_version, **t_style)

    _im = ax.imshow(grid)

    # Show all ticks and label them with the respective list entries
    short_rel = [rel.split('-')[0] for rel in releases]
    ax.set_xticks(range(len(releases)), labels=short_rel, **xt_style)
    ax.set_yticks(range(len(pkgnames)), labels=pkgnames)



    ax.set_title("test 1020")
    fig.tight_layout()
    plt.savefig("beer.png")
    print('DING')