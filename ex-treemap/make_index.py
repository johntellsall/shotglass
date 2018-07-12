#!/usr/bin/env python

import logging
import multiprocessing.pool as mpool
import os
import pandas as pd
import subprocess
import sys
import time
import traceback


DULL_DIRECTORIES = set(['.git'])
GOOD_EXTENSIONS = ('.py', '.c', '.go')
LOG_FORMAT = '%(asctime)-15s %(message)s'


def count_lines(path):
    try:
        return sum(1 for line in open(path, newline=None))
    except UnicodeDecodeError:
        return None


# TODO make configurable
def walk_tree(topdir):
    for root, dirs, files in os.walk(topdir):
        dirs[:] = list(set(dirs) - DULL_DIRECTORIES)
        for file in files:
            yield os.path.join(root, file)

# ctags -o - --extras=* --fields='*' --pseudo-tags='TAG_KIND_DESCRIPTION'


def format_index_cmd(path):
    cmd = 'ctags -o -'.split()
    return cmd + [path]


def make_ctags(path):
    cmd = format_index_cmd(path)
    out = subprocess.check_output(cmd)
    try:
        out = out.decode("utf-8", errors='ignore')
    except UnicodeDecodeError:
        logging.error(f'{path}: bad Unicode')
        return None
    return out


def make_linecount(path):
    try:
        count = count_lines(path)
        return count
    except Exception as e:
        traceback.print_exc()
        raise

# TODO make configurable


def is_source(path):
    return os.path.splitext(path)[-1] in GOOD_EXTENSIONS

def compile(project_dir, paths=None):
    source_paths = paths
    if source_paths is None:
        source_paths = list(filter(is_source, walk_tree(project_dir)))
    logging.info((f'{project_dir}: {len(source_paths)} files'))
    pool = mpool.Pool()
    start_tm = time.time()
    ctags_rows = pool.map(make_ctags, source_paths)
    count_rows = pool.map(make_linecount, source_paths)
    pool.close()
    pool.join()
    elapsed_tm = time.time() - start_tm
    logging.info('done')
    logging.info('%.1f files / sec', len(source_paths)/elapsed_tm)

    df = pd.DataFrame({
        'path': source_paths,
        'ctags_raw': ctags_rows,
        'linecount': count_rows,
    })
    return df

def make_project(project_dir):
    project_name = os.path.basename(project_dir)
    project_data_path = f'{project_name}.pkl'

    if os.path.exists(project_data_path):
        df = pd.read_pickle(project_data_path)
    else:
        df = compile(project_dir)
        df.to_pickle(project_data_path)
    logging.info(f'{project_name}: {len(df)} files')

def main(argv):
    logging.basicConfig(datefmt='%X', format=LOG_FORMAT, level=logging.INFO)
    for project_dir in argv:
        make_project(project_dir)

if __name__=='__main__':
    main(sys.argv[1:])

