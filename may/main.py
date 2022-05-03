#!/usr/bin/env python3
#
"""
Shotglass: info about codebases over time
"""

import logging
import pprint
import re
from distutils.version import LooseVersion
from pathlib import PurePath

import click

import run
import state

logging.basicConfig(format="%(asctime)-15s %(message)s", level=logging.INFO)


def git_ls_tree(project_path, release="2.0.0"):
    """
    get Git info about all files in given release
    """

    def to_item(row):
        pre, path = row.split("\t")
        _mode, _type, hash, size_bytes = pre.split()
        return dict(hash=hash, path=path, size_bytes=size_bytes)

    cmd = f"git -C {project_path} ls-tree  -r --long '{release}'"
    return map(to_item, run.run(cmd))


def git_tag_list(project_path):
    "list tags (~ releases)"
    return run.run(f"git -C {project_path} tag --list")


# :::::::::::::::::::: APP-CENTRIC FUNCTIONS


# TODO: make flexible
def is_source(path):
    return PurePath(path).suffix in [".c", ".py"]


# TODO: make flexible
def is_interesting(path):
    DULL_DIRS = set(["docs", "examples", "scripts", "tests"])
    if "/" in path:
        first, _ = path.split("/", 1)
        if first in DULL_DIRS:
            return False
    if path.endswith("__init__.py"):
        return False
    if "/testsuite/" in path:
        return False
    return True


def filter_goodsource(items):
    for item in items:
        path = item["path"]
        if is_source(path) and is_interesting(path):
            yield item


# TODO: make flexible
is_good_tag = re.compile(r"^[0-9]+\.[0-9]+$").match


def get_good_tags(path):
    raw_tags = git_tag_list(path)
    tags = list(filter(is_good_tag, raw_tags))
    return tags


def db_add_releases(con, project_path):
    """
    for project, insert interesting (Git) tags into db
    """
    tags = get_good_tags(project_path)

    insert_release = "insert into release (label) values (:label)"
    items = [{"label": tag} for tag in tags]
    con.executemany(insert_release, items)


# TODO: add via *hash* not path
def db_add_files(con, path, release):
    """
    for project and release/tag, add interesting files into db
    """
    all_items = list(git_ls_tree(path, release=release))
    items = list(filter_goodsource(all_items))

    insert_file = (
        "insert into file (release, path, hash, size_bytes)"
        f" values ('{release}', :path, :hash, :size_bytes)"
    )
    con.executemany(insert_file, items)


# CTAGS
# {'_type': 'tag', 'name': 'Flask', 'path': '.temp.py', 'access': 'public',
# 'inherits': 'object', 'language': 'Python', 'line': 173, 'kind': 'class',
# 'roles': 'def', 'end': 655}


def db_add_symbols(con, project_path, hash, path, release):
    run.run_blob(f"git -C {project_path} show {hash} > .temp.py")
    items = list(run.run_ctags(".temp.py"))
    num = None
    for num, item in enumerate(items):
        pass  # click.echo(f"- {num:03d} {item}")
    click.echo(f"- {path}: {num} symbols")

    # insert_sym = "insert into symbol (name)" f" values (:name)"
    # con.executemany(insert_sym, items)


# :::::::::::::::::::: COMMANDS


@click.group()
def cli():
    pass


@cli.command()
def list_git():
    """
    list project Releases, and stats for each release
    TODO: make generic (now Flask only)
    """
    path = "../SOURCE/flask"  # TODO:
    click.echo(f"List Tags {path}")
    tags = get_good_tags(path)
    tags.sort(key=LooseVersion)

    hashes = set()
    # for each release
    for tag in tags:
        click.secho(f"release: {tag}", fg="black", bg="yellow")
        all_items = list(git_ls_tree(path, release=tag))
        click.secho(f"= {len(all_items)} total files", fg="yellow")

        items = list(filter_goodsource(all_items))
        click.secho(f"= {len(items)} source files", fg="yellow")

        changed_items = []
        for item in items:
            hash = item["hash"]
            if hash in hashes:
                continue
            hashes.add(hash)
            changed_items.append(item)

        # show count of files changed in this release
        click.secho(f"+/- {len(changed_items)} changed source", fg="yellow")

        # .. and the files
        for item in changed_items:
            click.secho(f"- {item['path']}")


@cli.command()
def demo():
    """
    list project Releases, and stats for each release
    TODO: make generic (now Flask only)
    """
    project_path = "../SOURCE/flask"  # TODO:
    con = state.get_db()
    click.echo(f"List Tags {project_path}")

    # Git releases -> database; show count
    db_add_releases(con, project_path)
    count = state.query1(con, table="release")
    click.echo(f"Tags: {count}")

    # Per release: add release files -> database
    for (label,) in con.execute("select label from release"):
        db_add_files(con, path=project_path, release=label)

    # Per release: show count of files
    for (label,) in con.execute("select label from release"):
        sql = "select count(*) from file where release = ?"
        result = list(con.execute(sql, [label]))
        click.secho(f"rel {label}: {result[0][0]}")

    # Per file: extract symbols
    # TODO: restrict to interesting releases+files
    sql = "select path, hash, release from file"
    for path, hash, release in con.execute(sql):
        click.secho(f"- {path=} {hash=}")
        # TODO: more work here
        db_add_symbols(con, project_path, hash=hash, path=path, release=release)


@cli.command()
@click.argument("path")
def ls_tags(path):
    """
    list tags in Git repos
    """
    click.echo(f"List Tags {path}")
    tags = git_tag_list(path)
    pprint.pprint(tags)


@cli.command()
@click.argument("path")
def ctags(path):
    """
    show symbols of single source file (from Ctags)
    """
    click.echo(f"Ctags {path}")
    symbols = list(run.run_ctags(path))
    pprint.pprint(symbols)


if __name__ == "__main__":
    cli()
