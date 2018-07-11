import logging
import multiprocessing.pool as mpool
import os
import pandas as pd
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
    try:
        out = out.decode("utf-8", errors='ignore')
    except UnicodeDecodeError:
        logging.error(f'{path}: bad Unicode')
        return None
    return out
    # return {"path": path, "ctags": out}


def make_linecount(path):
    count = count_lines(path)
    return count
    # return {"path": path, "lines": count}

# TODO make configurable


def is_source(path):
    return os.path.splitext(path)[-1] in GOOD_EXTENSIONS

def compile(project_dir):
    source_paths = list(filter(is_source, walk_tree(project_dir)))
    logging.info((f'{project_dir}: {len(source_paths)} files'))
    pool = mpool.Pool()
    start_tm = time.time()
    ctags_rows = pool.map(make_ctags, source_paths)
    if 0:
        count_rows = pool.map(make_linecount, source_paths)
    pool.close()
    pool.join()
    elapsed_tm = time.time() - start_tm
    logging.info('done')
    logging.info('%.1f files / sec', len(source_paths)/elapsed_tm)

    df = pd.DataFrame({
        'path': source_paths,
        'ctags': ctags_rows,
        # 'linecount': count_rows,
    })
    return df

def main(project_dir):
    logging.basicConfig(datefmt='%X', format=LOG_FORMAT, level=logging.INFO)

    project_dir = sys.argv[1]
    project_name = os.path.basename(project_dir)
    project_data_path = f'{project_name}.pkl'

    if os.path.exists(project_data_path):
        df = pd.read_pickle(project_data_path)
    else:
        df = compile(project_dir)
        df.to_pickle(project_data_path)
    logging.info(f'{project_name}: {len(df)} files')


if __name__=='__main__':
    main(sys.argv[1])


# df = pd.DataFrame({'path': [8, 3, 4, 2],
#     'group': [
# if 1:
#     print(result1[0])
#     print(result2[0])
