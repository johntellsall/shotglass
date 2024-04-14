# shotglass.py -- count source lines, render simply

import glob
import sqlite3
import sys
from itertools import filterfalse, islice
from pathlib import Path

SOURCE_EXTENSIONS = ('.py', '.c', '.cpp')

# FIXME: make configurable
def is_source(path):
    return path.endswith(SOURCE_EXTENSIONS)

# FIXME: make configurable
def is_test(path):
    return '/test' in path

# FIXME: make configurable
def find_source(root_dir):
    if not Path(root_dir).is_dir():
        raise ValueError(f'{root_dir} is not a directory')
    file_paths = glob.iglob(root_dir + '/**', recursive=True)
    sources = filter(is_source, file_paths)
    no_tests = filterfalse(is_test, sources)
    return no_tests

def scan(source_dirs):
    for source_dir in source_dirs:
        print(f'{source_dir=}')
        sources = list(find_source(source_dir))
        source_count = len(sources)
        print(f'\t{source_count=}')

        total_lines = sum(map(count_lines, sources))
        print(f'\t{total_lines=}')

def count_lines(path):
    return sum(1 for _ in open(path))

# FIXME: make more flexible
def dbopen():
    dbpath = 'shotglass.db'
    sqlpath = 'shotglass.sql'

    con = sqlite3.connect(dbpath)

    tables = con.execute("SELECT name FROM sqlite_master WHERE type='table';")
    if not tables:
        print(f'{dbpath}: No tables, creating from {sqlpath}')
        with open(sqlpath) as sqlfile:
            con.executescript(sqlfile.read())

    return con


def dbclose(con):
    con.close()

def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python shotglass.py <filename>")

    db = dbopen()

    source_dirs = sys.argv[1:]
    scan(source_dirs)

if __name__ == "__main__":
    main()