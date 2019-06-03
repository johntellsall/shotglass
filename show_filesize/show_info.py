#!/usr/bin/env python

"""
show_info.py -- show source sizes over time
"""

import os
import re
import sys
from collections import Mapping, namedtuple

import yaml
from colorama import Back, Fore, Style
from git import Repo
from natsort import natsorted


class Project:
    config = None

    def parse_yaml(self, obj):
        self.config = yaml.load(obj)

    def __init__(self, arg):
        if not isinstance(arg, Mapping):
            arg = yaml.load(arg)
        self.config = arg
        dull_words = "|".join(self.config.get("dull_words", ""))
        self.dull_regex = re.compile(r"\b(" + dull_words + r")\b")

    def is_interesting_item(self, item):
        def is_interesting_name(name):
            return os.path.splitext(name)[-1] in self.config["source_extensions"]

        def is_interesting_path(path):
            return not self.dull_regex.search(path)

        return (
            item.type == "blob"
            and is_interesting_path(item.path)
            and is_interesting_name(item.name)
        )


def find_sources2(tree):
    proj = Project(
        dict(
            dull_words=[
                "docs",
                "examples",
                "scripts",
                "testsuite",
                "tests",
                "__init__.py",
            ],
            source_extensions=[".c", ".py"],
        )
    )
    return tree.traverse(predicate=lambda item, _: proj.is_interesting_item(item))


def find_sources(tree, proj):
    # proj = Project(open("flask.yaml"))
    return tree.traverse(predicate=lambda item, _: proj.is_interesting_item(item))


repo_path = sys.argv[1]
proj = Project(dict(source_extensions=[".c", ".py"]))
proj_name = os.path.basename(repo_path) + ".yaml"
if os.path.exists(proj_name):
    proj = Project(open(proj_name))

repo = Repo(repo_path)
last = repo.tags[-1]
print(last)
tree = last.commit.tree
paths = set(x.path for x in find_sources(tree, proj))
print(paths)
sys.exit(0)


def by_name(source):
    return source.name


def count_release(release):
    return len(list(find_sources(release.commit.tree)))


repo = Repo(sys.argv[1])
releases = natsorted(repo.tags, key=by_name)
print(f"releases: {len(releases)}")

num_first = count_release(releases[0])
num_last = count_release(releases[-1])
print(f"first: {releases[0]} num_source_files: {num_first}")
print(f"last: {releases[-1]} num_source_files: {num_last}")

prev = set()
for tag in natsorted(repo.tags, key=by_name):
    tag_label = f"{tag.name:10}"
    if 1:
        tag_label = Back.GREEN + Fore.BLACK + f"{tag.name:6}" + Style.RESET_ALL
    # show release date
    # TODO check first commit date is really the release date
    if 1:
        tag_label += " " + tag.commit.committed_datetime.strftime("%x")
    print(f"{tag_label}", end=" ")
    sources = set(map(by_name, find_sources(tag.commit.tree)))
    print(f"num_source_files: {len(sources)}")
    # TODO show adds and deletes
    if len(sources - prev):
        print(f"new files: {sorted(sources - prev)}")
    prev = sources
