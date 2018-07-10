import os
import sys

import matplotlib
matplotlib.use('svg')

import matplotlib.pyplot as plt
import pandas as pd
import squarify

# # If you have 2 lists
# squarify.plot(sizes=[13, 22, 35, 5],
# 	label=["group A", "group B", "group C", "group D"],
# 	alpha=.7)
# plt.axis('off')
# plt.savefig('one.png')

DULL_DIRECTORIES = set(['.git'])


def count_lines(path):
    return sum(1 for line in open(path))


def walk_tree(topdir):
    for root, dirs, files in os.walk(topdir):
        dirs[:] = list(set(dirs) - DULL_DIRECTORIES)
        for file in files:
            yield os.path.join(root, file)


def is_source(path):
    return os.path.splitext(path)[-1] == '.py'



source_paths = list(filter(is_source, walk_tree(sys.argv[1])))
print(len(source_paths)); sys.exit(1)
line_counts = list(map(count_lines, source_paths))
names = list(map(os.path.basename, source_paths))
print(line_counts)
print(names)
df = pd.DataFrame({
    'lines': line_counts,
    'name': names,
})
squarify.plot(sizes=df['lines'], label=df['name'], alpha=.8)
plt.axis('off')
plt.savefig('dir.png')
