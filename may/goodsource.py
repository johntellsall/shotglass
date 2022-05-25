# goodsource.py
"""
Given a Git tag/release, is it interesting enough to capture?
- likewise, files and directories
"""

import re
from pathlib import PurePath

import run


def git_ls_tree(project_path, release="2.0.0"):
    """
    get Git info about all files in given release
    """

    def to_item(row):
        pre, path = row.split("\t")
        _mode, _type, filehash, size_bytes = pre.split()
        return dict(hash=filehash, path=path, size_bytes=size_bytes)

    cmd = f"git -C {project_path} ls-tree  -r --long '{release}'"
    return map(to_item, run.run(cmd))


def git_tag_list(project_path):
    "list tags (~ releases)"
    return run.run(f"git -C {project_path} tag --list")


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
