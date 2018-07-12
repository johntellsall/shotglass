import os
import sys

import matplotlib
matplotlib.use('agg')

import matplotlib.pyplot as plt
import pandas as pd
import squarify


def make_squarify(project_data_path):
    df = pd.read_pickle(project_data_path)
    df = df[df.linecount > 0]
    squarify.plot(sizes=df.linecount, label=df.name, alpha=.8)
    plt.axis('off')
    name = os.path.splitext(os.path.basename(project_data_path))[0]
    out_path = f'{name}.png'
    print(out_path)
    plt.savefig(out_path)


if __name__ == '__main__':
    make_squarify(sys.argv[1])

# source_paths = list(filter(is_source, sys.argv[1:]))
# line_counts = list(map(count_lines, source_paths))
# names = list(map(os.path.basename, source_paths))
# print(line_counts)
# print(names)
# df = pd.DataFrame({
#     'lines': line_counts,
#     'name': names,
# })
