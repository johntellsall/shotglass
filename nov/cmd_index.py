# cmd_index.py

import json
import logging
import subprocess
import sys
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


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


# TODO: pylint: disable=too-many-locals
def cmd_index(project_path, temporary=False):
    project_dir = Path(project_path)
    print(project_dir)

    repo = git.Repo(project_dir)
    tree, source_paths = shotlib.get_project(repo)
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
            item = shotlib.make_file_info(tree[path])
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


def cmd_ctags(file_path):
    print(f"== {file_path}")
    for tag_info in make_tags_info(file_path):
        print(tag_info)
