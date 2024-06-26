# build.py -- count source lines, build index

import glob
import json
import os
import sqlite3
import subprocess
import sys
from collections import Counter
from itertools import filterfalse
from pathlib import Path
from pprint import pprint

SOURCE_EXTENSIONS = (".py", ".c", ".cpp")


# FIXME: make configurable
def is_source(path):
    return path.endswith(SOURCE_EXTENSIONS)


# FIXME: make configurable
def is_test(path):
    return "/test" in path


# FIXME: make configurable
def find_source(root_dir):
    if not Path(root_dir).is_dir():
        raise ValueError(f"{root_dir} is not a directory")
    file_paths = glob.iglob(root_dir + "/**", recursive=True)
    sources = filter(is_source, file_paths)
    no_tests = filterfalse(is_test, sources)
    return no_tests


def run_ctags(path):
    cmd = "ctags --fields=* --output-format=json".split()
    cmd += [path]
    proc = subprocess.run(cmd + [path], stdout=subprocess.PIPE, text=True)
    return proc.stdout.splitlines()


# FIXME: make clearer and simpler
def scan_file_tags(con, path):
    fields = """
_type name path language line
kind access signature roles end""".split()
    fields_sql = ", ".join(fields)
    num_fields = len(fields) + 1  # +1 for shotglass_path
    values_sql = "?," * (num_fields - 1) + "?"
    tag_sql = f"insert into tag (shotglass_path, {fields_sql}) values ({values_sql})"
    shotglass_values = [path]

    lines = list(run_ctags(path))
    for tag in map(json.loads, lines):
        tag_values = [tag.get(field, f"UNKNOWN-{field}") for field in fields]
        con.execute(tag_sql, shotglass_values + tag_values)
    con.commit()


def show_sample(con):
    print("SAMPLE:")
    sample = con.execute("select * from tag limit 3").fetchall()
    for item in sample:
        print(f"\t{item=}")


def show_stats(con):
    print("STATS:")
    sample = con.execute("select count(*) from tag").fetchall()
    for tag_count in sample:
        print(f"\t{tag_count=}")


# TODO: optimize with executemany?
def scan_project(con, source_dir):
    sources = list(find_source(source_dir))
    source_count = len(sources)
    line_counter = Counter()
    linecount_sql = "insert into shotglass (path, line_count) values (?, ?)"
    for source in sources:
        scan_file_tags(con, source)
    for source in sources:
        line_counter[source] = count_lines(source)
    for source, lines in line_counter.items():
        con.execute(linecount_sql, (source, lines))
    con.commit()
    total_lines = sum(line_counter.values())
    info = {
        "source_count": source_count,
        "total_lines": total_lines,
        "source_dir": source_dir,
    }
    return info


def scan_projects(con, source_dirs):
    for source_dir in source_dirs:
        print(f"{source_dir=}")
        info = scan_project(con, source_dir)
        print("\t", end="")
        pprint(info)


def count_lines(path):
    return sum(1 for _ in open(path))


SQL_LIST_TABLES = "SELECT name FROM sqlite_master WHERE type='table';"


# FIXME: make more flexible
def dbopen():
    dbpath = "shotglass.db"
    sqlpath = "shotglass.sql"

    if dbpath:
        print("WARNING: resetting database")
        os.remove(dbpath)
        con = sqlite3.connect(dbpath)
    else:
        con = sqlite3.connect(":memory:")

    tables = list(con.execute(SQL_LIST_TABLES))
    if not tables:
        print(f"{dbpath}: No tables, creating from {sqlpath}")
        with open(sqlpath) as sqlfile:
            con.executescript(sqlfile.read())
        con.commit()

    return con


def build(source_dirs):
    with dbopen() as con:
        scan_projects(con, source_dirs)

        show_sample(con)
        show_stats(con)
