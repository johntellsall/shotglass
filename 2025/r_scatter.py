from pprint import pprint
import re
import matplotlib.pyplot as plt
import numpy as np

# from packaging import 
from lib import equery


# class SGAlpinePackage(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     alpine_release: str  # FIXME: rename -> sg_alpine_release
#     pkgname: str
#     pkgdesc: str
#     pkgver: str
#     pkgrel: str
#     sg_complexity: int | None = None
#     sg_len_build: int | None = None
#     sg_len_install: int | None = None
#     sg_len_subpackages: int | None = None
#     sg_file_num_lines: int | None = None

def query_data():
    sql = """
    SELECT alpine_release, pkgname, pkgver, sg_file_num_lines
    from sgalpinepackage
"""
    return equery(sql)

def scatter():
    # plt.style.use('_mpl-gallery')
    # plt.style.use('fivethirtyeight')

    data = query_data()
    pprint(data[:10])
    data = np.array(data)

    data_alpine_release = data[:, 0]
    data_alpine_release = [rel.replace('-stable', '') for rel in data_alpine_release]
    data_file_num_lines = data[:, 3].astype(int)

    version_pat = re.compile(r'(\d+\.\d+)') # major.minor only
    def parse_version(ver):
        if m := version_pat.match(ver):
            return float(m.group(1))
        return 0
    data_pkgver = data[:, 2]
    data_pkgver = [parse_version(ver) for ver in data_pkgver]

    print(data_alpine_release[:10])
    print(data_pkgver[:10])
    print(data_file_num_lines[:10])

    if 0:
        # make the data
        np.random.seed(3)
        x = 4 + np.random.normal(0, 2, 24)
        y = 4 + np.random.normal(0, 2, len(x))
        # size and color:
        sizes = np.random.uniform(15, 80, len(data))
        colors = np.random.uniform(15, 80, len(data))

    # plot
    fig, ax = plt.subplots()

    # ax.scatter(x, y, s=sizes, c=colors, vmin=0, vmax=100)
    # conf = dict(s=sizes, c=colors, vmin=0, vmax=100)
    conf = dict()
    # ax.scatter(x=data_alpine_release, y=data_file_num_lines, **conf)
    ax.scatter(x=data_alpine_release, y=data_file_num_lines, **conf)
    print(len(data_pkgver), len(data_file_num_lines))

    ax.set_xlabel('Alpine Release')
    ax.set_ylabel('Apkgbuild Size')
    # plt.xlim(0, 4) # only see Package Versions up to 3
    # ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
    #     ylim=(0, 8), yticks=np.arange(1, 8))

    imgpath = __file__.replace('.py', '.png')
    plt.savefig(imgpath)