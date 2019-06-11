#!/usr/bin/env python

# make_squarify -- render image with squares representing source files
#
# USAGE:
# make_squarify flask.pkl
# -- outputs flask.png

import os
import sys
from collections import Counter

import matplotlib

matplotlib.use("agg")

import matplotlib.pyplot as plt
import pandas as pd
import squarify

PREFIX = "/Users/johnmitchell/jsrc/shotglass/SOURCE/"


def zap_prefix(path):
    if not path.startswith(PREFIX):
        return path
    rest = path[len(PREFIX) :]
    # TODO strip next dir name
    return rest


def make_squarify_files(project_data_path):
    df = pd.read_pickle(project_data_path)
    df = df[df.linecount > 0]
    squarify.plot(sizes=df.linecount, label=df.name, alpha=0.8)
    plt.axis("off")
    name = os.path.splitext(os.path.basename(project_data_path))[0]
    out_path = f"{name}.png"
    print(out_path)
    plt.savefig(out_path)


def make_squarify(project_data_path):
    df = pd.read_pickle(project_data_path)
    dir_size = Counter()
    for item in df.itertuples():
        path = zap_prefix(item.path)
        dir_ = os.path.dirname(path)
        dir_size[dir_] += item.linecount

    items = dir_size.most_common()  # sort
    dir_items = pd.DataFrame(items, columns=("dir", "dir_linecount"))

    dir_items = dir_items[dir_items.dir_linecount > 0]
    squarify.plot(sizes=dir_items.dir_linecount, label=dir_items.dir, alpha=0.8)
    plt.axis("off")

    name = os.path.splitext(os.path.basename(project_data_path))[0]
    plt.title(name.title())
    out_path = f"{name}.png"
    print(out_path)
    plt.savefig(out_path)


if __name__ == "__main__":
    make_squarify(sys.argv[1])
