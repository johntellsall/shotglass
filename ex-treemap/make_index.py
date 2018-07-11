import logging
import os
import sys
import multiprocessing.pool as mpool

DULL_DIRECTORIES = set(['.git'])
LOG_FORMAT = '%(asctime)-15s %(message)s'

def count_lines(path):
    return sum(1 for line in open(path))


# TODO make configurable
def walk_tree(topdir):
    for root, dirs, files in os.walk(topdir):
        dirs[:] = list(set(dirs) - DULL_DIRECTORIES)
        for file in files:
            yield os.path.join(root, file)

def make_index(path):
    return path

# TODO make configurable
def is_source(path):
    return os.path.splitext(path)[-1] in ('.py', '.c')

logging.basicConfig(datefmt='%X', format=LOG_FORMAT, level=logging.INFO)

project_dir = sys.argv[1]
source_paths = list(filter(is_source, walk_tree(project_dir)))
logging.info((f'{project_dir}: {len(source_paths)} paths'))
pool = mpool.Pool()
print(pool.map(make_index, source_paths))
pool.close()
pool.join()
logging.info('done')
