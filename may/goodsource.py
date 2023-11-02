# goodsource.py
"""
Given a Git tag/release, is it interesting enough to capture?
- likewise, files and directories
"""

import re
import subprocess
from distutils.version import LooseVersion
from pathlib import PurePath

import run


def git_ls_tree(project_path, release):
    """
    get Git info about all files in given release
    """

    def to_item(row):
        pre, path = row.split("\t")
        _mode, _type, filehash, size_bytes = pre.split()
        return dict(hash=filehash, path=path, size_bytes=size_bytes)

    cmd = f"git -C {project_path} ls-tree  -r --long '{release}'"
    try:
        return map(to_item, run.run(cmd))
    except subprocess.CalledProcessError as error:
        print(f"?? {cmd} -- {error}")
        return []


def git_tag_list(project_path):
    "list tags (~ releases)"
    return run.run(f"git -C {project_path} tag --list")


def sort_versions(mylist):
    mylist.sort(key=LooseVersion)


# TODO: make flexible
def is_source(path):
    return PurePath(path).suffix in [".c", ".py"]


# TODO: make flexible
# TODO: add "+package+"
def is_interesting(path):
    DULL_DIRS = set([".github", "doc", "docs", "examples", "scripts", "test", "tests"])
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
    """
    iterate over source files that are 'interesting'
    E.g.: only source files; skip tests, docs, examples
    """
    for item in items:
        path = item["path"]
        if is_source(path) and is_interesting(path):
            yield item


# TODO: make flexible
is_good_tag = re.compile(r"^[0-9]+\.[0-9]+$").match

# FIXME: conflicts with GoodSourceConfig
def get_good_tags(path):
    raw_tags = git_tag_list(path)
    tags = list(filter(is_good_tag, raw_tags))
    return tags


class SourceConfig:
    def __init__(self, path):
        self.path = path

    def get_tags(self):
        return git_tag_list(self.path)


class AllSourceConfig(SourceConfig):
    pass


class GoodSourceConfig(SourceConfig):
    # TODO: make flexible
    is_good_tag = re.compile(r"^[0-9]+\.[0-9]+$").match

    def get_tags(self):
        raw_tags = git_tag_list(self.path)
        tags = list(filter(self.is_good_tag, raw_tags))
        # tags = tags[:10]
        return tags
