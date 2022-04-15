import os
import sys

import matplotlib

matplotlib.use('svg')

import matplotlib.pyplot as plt
import pandas as pd
import squarify

DULL_DIRECTORIES = set(['.git'])


def count_lines(path):
    return sum(1 for line in open(path))


# TODO make configurable
def walk_tree(topdir):
    for root, dirs, files in os.walk(topdir):
        dirs[:] = list(set(dirs) - DULL_DIRECTORIES)
        for file in files:
            yield os.path.join(root, file)


# TODO make configurable
def is_source(path):
    return os.path.splitext(path)[-1] == '.py'

project_dir = sys.argv[1]
source_paths = list(filter(is_source, walk_tree(project_dir)))
line_counts = list(map(count_lines, source_paths))
names = list(map(os.path.basename, source_paths))
print(names)
df = pd.DataFrame({
    'paths': source_paths,
    'names': names})
df['line_counts'] = line_counts
# TODO zap items where line_count==0
print(line_counts)

squarify.plot(
    sizes=df['line_counts'],
    label=df['names'], alpha=.8)
plt.axis('off')
title = os.path.basename(project_dir).title()
plt.title(title)
plt.savefig('tree.png')
