# shotglass.py -- count source lines, render simply

import glob
from pprint import pprint
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

from collections import Counter

import subprocess
def run_ctags(path):
    cmd = "ctags --fields=* --output-format=json".split()
    cmd += [path]
    proc = subprocess.run(cmd + [path], stdout=subprocess.PIPE, text=True)
    return proc.stdout.split(r'\n')

def scan_file_tags(con, path):
    lines = run_ctags(path)
    assert 0, lines[:5]
                   
# TODO: optimize with executemany?
def scan_project(con, source_dir):
    sources = list(find_source(source_dir))
    source_count = len(sources)
    line_counter = Counter()
    linecount_sql = 'insert into shotglass (path, line_count) values (?, ?)'
    for source in sources:
        scan_file_tags(con, source)
    for source in sources:
        line_counter[source] = count_lines(source)
    for source, lines in line_counter.items():
        con.execute(linecount_sql, (source, lines))
    total_lines = sum(line_counter.values())
    info = {
        'source_count': source_count,
        'total_lines': total_lines,
        'source_dir': source_dir,
    }
    return info

def scan_projects(con, source_dirs):
    for source_dir in source_dirs:
        print(f'{source_dir=}')
        info = scan_project(con, source_dir)
        print('\t', end='')
        pprint(info)

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

    print('WARNING: resetting database')
    con.execute('delete from shotglass')
    con.commit()

    return con


def dbclose(con):
    con.close()

def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python shotglass.py <filename>")

    con = dbopen()

    source_dirs = sys.argv[1:]
    scan_projects(con, source_dirs)

if __name__ == "__main__":
    main()