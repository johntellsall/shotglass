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


def count_lines(path):
    return sum(1 for line in open(path))


def is_source(path):
    return os.path.splitext(path)[-1] == '.py'



source_paths = list(filter(is_source, sys.argv[1:]))
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
