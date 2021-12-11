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
    #
    # PROJECTS
    #
    # db.execute("drop table if exists projects")
    db.execute(
        """
        create table projects (
            id integer primary key,
            name text
            );
        """
    )
    # db.execute("drop table if exists projects")
    db.execute(
        """
        create table files (
            id integer primary key,
            path text,
            byte_count int,
            project_id int,
            foreign key (project_id) references projects(id)
            );
        """
    )
    #
    # SYMBOLS
    # TODO: add id? use rowid?
    # db.execute("drop table if exists symbols")
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
    #
    # RELEASES
    #
    # db.execute("drop table if exists releases")
    db.execute(
        """
        create table releases (
            tag text,
            creator_dt text -- ISO8601
        )
        """
    )


def make_releases_info(project_dir, verbose=False):
    """
    get info for releases (Git tags)
    """
    git_dir = Path(project_dir) / ".git"
    cmd = (
        "git",
        f"--git-dir={git_dir}",
        "for-each-ref",
        "--format=%(refname:short),%(creatordate:iso-strict)",
        "refs/tags/*",
    )
    if verbose:
        print(" ".join(cmd))
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    # TODO: simplify
    lines = filter(None, proc.stdout.split("\n"))
    return [line.split(",") for line in lines]


def make_tags_info_paths(project_dir, source_paths):
    """
    calc info for source code tags/symbols
    """
    values = []
    for path in source_paths:
        fullpath = project_dir / path
        for tag in make_tags_info(fullpath):
            values.append((path, tag["name"], tag["line"], tag.get("end"), tag["kind"]))
    return values


def make_file_info_paths(tree, source_paths):
    issues, values = [], []
    for path in source_paths:
        try:
            item = shotlib.make_file_info(tree[path])
            values.append((item["path"], item["num_bytes"]))
        except KeyError as err:
            issues.append((path, err))
    return issues, values


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


# TODO: merge with cmd_info?
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

    issues, values = make_file_info_paths(tree, source_paths)

    cur.executemany(
        """
    insert into files (path, byte_count) values (?, ?)
    """,
        values,
    )
    con.commit()

    num_files = shotlib.select1(cur, "select count(*) from files")
    print(f"NUM FILES: {num_files}")

    values = make_tags_info_paths(project_dir, source_paths)

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

    num_symbols = shotlib.select1(cur, "select count(*) from symbols")
    print(f"NUM SYMBOLS: {num_symbols}")

    values = make_releases_info(project_dir)
    print(values)
    cur.executemany(
        """
    insert into releases (tag, creator_dt) values (?, ?)
    """,
        values,
    )
    con.commit()

    num_releases = shotlib.select1(cur, "select count(*) from releases")
    print(f"NUM RELEASES: {num_releases}")

    shotlib.show_details(con)
    con.close()
    if issues:
        print(f"NOTE: {len(issues)} issues found")


def cmd_ctags(file_path):
    print(f"== {file_path}")
    for tag_info in make_tags_info(file_path):
        print(tag_info)
