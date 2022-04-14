#!/usr/bin/env python3
#
"""
function(path) -> data
"""

import json
import logging
import pprint
import subprocess
import re
from pathlib import PurePath
import click
from distutils.version import LooseVersion

# Universal Ctags
CTAGS_ARGS = "ctags --output-format=json --fields=*-P -o -".split()

logging.basicConfig(format="%(asctime)-15s %(message)s", level=logging.INFO)


def run_ctags(path, verbose=False):
    "Ctags command output -- iter of dictionaries, one per symbol"
    cmd = CTAGS_ARGS + [path]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    assert proc.returncode == 0
    if verbose:
        print(f"-- RAW\n{proc.stdout[:300]}\n-- ENDRAW")
    return map(json.loads, proc.stdout.rstrip().split("\n"))


def run_blob(cmd):
    proc = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, check=True
    )  # noqa: E501
    return proc.stdout


def run(cmd):
    out_blob = run_blob(cmd)
    out_lines = out_blob.rstrip("\n").split("\n")
    return out_lines


def git_ls_tree(project_path, release="2.0.0"):
    """
    get Git info about all files in given release
    """

    def to_item(row):
        pre, path = row.split("\t")
        _mode, _type, hash, size_bytes = pre.split()
        return dict(hash=hash, path=path, size_bytes=size_bytes)

    cmd = f"git -C {project_path} ls-tree  -r --long '{release}'"
    return map(to_item, run(cmd))


def git_tag_list(project_path):
    "list tags (~ releases)"
    return run(f"git -C {project_path} tag --list")


# :::::::::::::::::::: APP-CENTRIC FUNCTIONS


# TODO: make flexible
def is_source(path):
    return PurePath(path).suffix in [".c", ".py"]


# TODO: make flexible
def is_interesting(path):
    dull_dirs = set(["docs", "examples", "scripts", "tests"])
    if "/" in path:
        first, _ = path.split("/", 1)
        if first in dull_dirs:
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


# ::::::::::::::::::::


@click.group()
def cli():
    pass


@cli.command()
# @click.argument("path")
def april():
    path = "../SOURCE/flask"
    click.echo(f"List Tags {path}")
    tags = get_good_tags(path)
    tags.sort(key=LooseVersion)

    hashes = set()
    for tag in tags:
        click.secho(f"release: {tag}", bg="yellow")
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

        click.secho(f"+/- {len(changed_items)} changed source", fg="yellow")

        for item in changed_items:
            click.secho(f"- {item['path']}")


@cli.command()
@click.argument("path")
def ls_tags(path):
    click.echo(f"List Tags {path}")
    tags = git_tag_list(path)
    pprint.pprint(tags)


@cli.command()
@click.argument("path")
def ctags(path):
    click.echo(f"Ctags {path}")
    symbols = list(run_ctags(path))
    pprint.pprint(symbols)
    # run_ctags("../SOURCE/flask/src/flask/app.py", verbose=True)


if __name__ == "__main__":
    cli()
