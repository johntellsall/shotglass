"""
USAGE

shotglass.py <command> <project path>
"""

import json
import logging
import re
import subprocess
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

import git

import shotlib

# Universal Ctags
CTAGS_ARGS = "ctags --output-format=json --fields=*-P -o -".split()

logging.basicConfig(format="%(asctime)-15s %(message)s", level=logging.INFO)


def run_ctags(path, verbose=False):
    "return fulltext of Ctags command output"
    cmd = CTAGS_ARGS + [path]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    if verbose:
        print(f"-- RAW\n{proc.stdout[:300]}\n-- ENDRAW")
    return proc.stdout


def parse_ctags(blob):
    "parse Ctags-JSON output into iter of dictionaries"
    return map(json.loads, filter(None, blob.split("\n")))


def list_paths(repo):
    return repo.git.ls_files().split("\n")


# TODO make more general
def is_source_path(path):
    return Path(path).suffix in (".py", ".c")


# TODO make more general
def is_interesting(path):
    return not re.search(r"(docs|examples|migrations|tests)/", path)


def is_interesting_source(path):
    return is_source_path(path) and is_interesting(path)


def make_file_info(entry):
    "return dict of information for single source file"
    return {"path": entry.path, "num_bytes": entry.size}


def make_tags_info(fullpath):
    """
    find info about all tags/symbols in a single source file
    Return: iter of dictionaries, one per symbol
    """
    return parse_ctags(run_ctags(fullpath))


def setup_db(db):
    db.execute("drop table if exists files")
    db.execute(
        """
        create table files (
            id integer primary key, -- TODO rowid?
            path text,
            byte_count int
            );
        """
    )
    db.execute("drop table if exists symbols")
    db.execute(
        """
        create table symbols (
            file_id int,
            name text,
            start_line int,
            end_line int,
            kind text,
            foreign key (file_id) references files(id));
        """
    )


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
    paths = filter(is_source_path, paths)
    paths = filter(is_interesting, paths)
    paths = list(paths)
    paths = list(paths)


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


def cmd_index(project_path, temporary=False):
    project_dir = Path(project_path)
    print(project_dir)

    repo = git.Repo(project_dir)
    tree, source_paths = get_project(repo)
    if not source_paths:
        sys.exit("No source paths")
    con, cur = shotlib.get_db(temporary=temporary)

    con.execute("PRAGMA synchronous=OFF")
    con.execute("PRAGMA foreign_keys=ON")
    setup_db(cur)

    issues = []
    values = []
    for path in source_paths:
        try:
            item = make_file_info(tree[path])
            values.append((item["path"], item["num_bytes"]))
        except KeyError as err:
            issues.append((path, err))
            continue

    cur.executemany(
        """
    insert into files (path, byte_count) values (?, ?)
    """,
        values,
    )
    con.commit()

    num_files = shotlib.select1(cur, "select count(*) from files")
    print(f"NUM FILES: {num_files}")

    for path in source_paths:
        values = []
        fullpath = project_dir / path
        for tag in make_tags_info(fullpath):
            values.append((path, tag["name"], tag["line"], tag.get("end"), tag["kind"]))

        # TODO: optimize
        cur.executemany(
            """
        insert into symbols (file_id, name, start_line, end_line, kind) values (
            (select id from files where path=?),
            ?, -- name
            ?, -- start_line
            ?, -- end_line
            ? -- kind
            )
        """,
            values,
        )
        con.commit()

    shotlib.show_details(con)
    con.close()
    if issues:
        print(f"NOTE: {len(issues)} issues found")
