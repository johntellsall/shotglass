import logging
import multiprocessing.pool as mpool
import os
import subprocess
import sys
import time


DULL_DIRECTORIES = set(['.git'])
GOOD_EXTENSIONS = ('.py', '.c', '.go')
LOG_FORMAT = '%(asctime)-15s %(message)s'


def count_lines(path):
    return sum(1 for line in open(path))


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
    out = out.decode("utf-8", errors='ignore')
    return {"path": path, "ctags": out}

def make_linecount(path):
    count = count_lines(path)
    return {"path": path, "lines": count}

# TODO make configurable
def is_source(path):
    return os.path.splitext(path)[-1] in GOOD_EXTENSIONS


logging.basicConfig(datefmt='%X', format=LOG_FORMAT, level=logging.INFO)

project_dir = sys.argv[1]
source_paths = list(filter(is_source, walk_tree(project_dir)))
logging.info((f'{project_dir}: {len(source_paths)} files'))
pool = mpool.Pool()
start_tm = time.time()
result1 = pool.map(make_ctags, source_paths)
result2 = pool.map(make_linecount, source_paths)
pool.close()
pool.join()
elapsed_tm = time.time() - start_tm
logging.info('done')
logging.info('%.1f files / sec', len(source_paths)/elapsed_tm)
if 1:
    print(result1[0])
    print(result2[0])
