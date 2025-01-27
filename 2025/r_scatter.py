from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np

# from packaging import 
from lib import equery

# CREATE TABLE sgalpinepackage (
#         id INTEGER NOT NULL, 
#         alpine_release VARCHAR NOT NULL, 
#         pkgname VARCHAR NOT NULL, 
#         pkgdesc VARCHAR NOT NULL, 
#         pkgver VARCHAR NOT NULL, 
#         pkgrel VARCHAR NOT NULL, 
#         sg_complexity INTEGER,  -- XX: not used?
#         sg_len_build INTEGER, 
#         sg_len_install INTEGER, 
#         sg_len_subpackages INTEGER

def query_data():
    sql = """
    SELECT sg_len_install, sg_len_parse_funcs
    from sgalpinepackage
"""
    return equery(sql)

def scatter():
    plt.style.use('_mpl-gallery')

    data = query_data()
    pprint(data)
    data = np.array(data)

    len_install_data = data[:, 0]
    len_parse_funcs_data = data[:, 1]

    if 1:
        print(len_install_data)
        print(len_parse_funcs_data)

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
    conf = dict(s=sizes, c=colors, vmin=0, vmax=100)
    conf = dict()
    ax.scatter(x=len_install_data, y=len_parse_funcs_data, **conf)

    ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
        ylim=(0, 8), yticks=np.arange(1, 8))

    imgpath = __file__.replace('.py', '.png')
    plt.savefig(imgpath)