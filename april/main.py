"""
function(path) -> data
"""

import logging
import subprocess
import click
import json

# Universal Ctags
CTAGS_ARGS = "ctags --output-format=json --fields=*-P -o -".split()

logging.basicConfig(format="%(asctime)-15s %(message)s", level=logging.INFO)


def run_ctags(path, verbose=False):
    "return fulltext of Ctags command output"
    cmd = CTAGS_ARGS + [path]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    assert proc.returncode == 0
    if verbose:
        print(f"-- RAW\n{proc.stdout[:300]}\n-- ENDRAW")
    return map(json.loads, proc.stdout.rstrip().split("\n"))


def run_blob(cmd):
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
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


def git_tag_list(path):
    return run(f"git -C {path} tag --list")


@click.command()
@click.argument("name")
def hello(name):
    click.echo(f"Hello {name}!")
    run_ctags("../SOURCE/flask/src/flask/app.py", verbose=True)
