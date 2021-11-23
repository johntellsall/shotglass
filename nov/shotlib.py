# shotlib.py


# import json
# import logging
import re

# import subprocess
import sqlite3
import sys

# from datetime import datetime
from pathlib import Path

# import git


# TODO make more general
def is_source_path(path):
    return Path(path).suffix in (".py", ".c")


# TODO make more general
def is_interesting(path):
    return not re.search(r"(docs|examples|migrations|tests)/", path)


def is_interesting_source(path):
    return is_source_path(path) and is_interesting(path)


def get_db(temporary=False):
    path = ":memory:" if temporary else "main.db"
    con = sqlite3.connect(path)  # pylint: disable=no-member
    cur = con.cursor()
    return con, cur


def get_main_tree(git_repo):
    heads = git_repo.heads
    if hasattr(heads, "master"):
        return heads.master.commit.tree
    try:
        return git_repo.heads.main.commit.tree
    except AttributeError as err:
        attrs = [attr for attr in dir(heads) if not attr.startswith("_")]
        sys.exit(f"tags?? {attrs}\n{err}")


def get_project(repo):
    tree = get_main_tree(repo)
    paths = list_paths(repo)
    assert len(paths) > 0, "No source"
    paths = filter(is_interesting_source, paths)
    # paths = filter(is_source_path, paths)
    paths = list(paths)
    assert len(paths) > 0, "No interesting source"
    return tree, paths
    # pylint: disable=unreachable
    paths = filter(is_source_path, paths)
    paths = filter(is_interesting, paths)
    paths = list(paths)
    paths = list(paths)


def list_paths(repo):
    return repo.git.ls_files().split("\n")


def make_file_info(entry):
    "return dict of information for single source file"
    return {"path": entry.path, "num_bytes": entry.size}


def select1(db, sql):
    db.execute(sql)
    return db.fetchone()[0]


def selectall(db, sql):
    db.execute(sql)
    return db.fetchall()


def show_details(db):
    print("DETAILS:")
    print("-- files")
    for row in db.execute("select * from files order by 1 limit 3"):
        print(row)
    print("-- symbols")
    for row in db.execute("select * from symbols order by 1 limit 3"):
        print(row)
