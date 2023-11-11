# goodsource.py
"""
Given a Git tag/release, is it interesting enough to capture?
- likewise, files and directories
- TODO: likewise, symbols/functions
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


# FIXME: make flexible
# TODO: add "+package+"
# TODO: merge interesting *files* with interesting *releases*?
DULL_DIRS = set([".github", "doc", "docs", "examples", "migrations", "scripts", "test", "tests", "testsuite"])
def is_interesting(path):
    parts = set(PurePath(path).parts)
    return not DULL_DIRS.intersection(parts)


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
class GoodSourceConfig:
    GOOD_PATS = {
        'major_minor': r"^[0-9]+\.[0-9]+$",
        'numbers': r"^[0-9.]+$"  # exclude "2.0.0rc1"
    }

    def __init__(self, path):
        self.path = path
        self.good_pat = None

    def set_good_pat(self, pat):
        if pat.startswith('^'):
            self.good_pat = pat # regex
        elif pat in (None, 'latest'):
            self.good_pat = pat # None=all tags; latest=latest
        else:
            self.good_pat = self.GOOD_PATS[pat]

    def _get_tags_latest(self, raw_tags):
        tags = list(raw_tags)
        return tags[-1:]

    def get_tags(self):
        raw_tags = git_tag_list(self.path)
        if self.good_pat == 'latest':
            return self._get_tags_latest(raw_tags)
        elif self.good_pat is None:
            return list(raw_tags)

        is_good_tag = re.compile(self.good_pat).match
        tags = list(filter(is_good_tag, raw_tags))
        return tags


def get_good_tags(path):
    good_source = GoodSourceConfig(path)
    return good_source.get_tags()