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
        def compile_words(word_list):
            if not word_list:
                return None
            words_pipes = "|".join(word_list)
            return re.compile(r"\b(" + words_pipes + r")\b")

        if not isinstance(arg, Mapping):
            arg = yaml.load(arg)
        self.config = arg
        self.dull_path_regex = compile_words(self.config.get("dull_words"))
        self.dull_tag_regex = compile_words(self.config.get("dull_tag_patterns"))

    def list_interesting_tags(self, repo):
        tags = repo.tags
        if not self.dull_tag_regex:
            return tags
        return [tag for tag in tags if not self.dull_tag_regex.search(tag.name)]

    def is_interesting_item(self, item):
        def is_interesting_name(name):
            return os.path.splitext(name)[-1] in self.config["source_extensions"]

        def is_interesting_path(path):
            return self.dull_path_regex is None or not self.dull_path_regex.search(path)

        return (
            item.type == "blob"
            and is_interesting_path(item.path)
            and is_interesting_name(item.name)
        )


def find_sources(tree, proj):
    return tree.traverse(predicate=lambda item, _: proj.is_interesting_item(item))


def find_files(tree):
    return tree.traverse(predicate=lambda item, _: item.type == "blob")


def count(release, findfunc):
    return len(list(findfunc(release.commit.tree)))


def by_name(source):
    return source.name


def count_release(release):
    return len(list(find_sources(release.commit.tree)))


# def show_info(repo):
#     releases = natsorted(repo.tags, key=by_name)
#     print(f"releases: {len(releases)}")

#     num_first = count_release(releases[0])
#     num_last = count_release(releases[-1])
#     print(f"first: {releases[0]} num_source_files: {num_first}")
#     print(f"last: {releases[-1]} num_source_files: {num_last}")

#     prev = set()
#     for tag in natsorted(repo.tags, key=by_name):
#         tag_label = f"{tag.name:10}"
#         if 1:
#             tag_label = Back.GREEN + Fore.BLACK + f"{tag.name:6}" + Style.RESET_ALL
#         # show release date
#         # TODO check first commit date is really the release date
#         if 1:
#             tag_label += " " + tag.commit.committed_datetime.strftime("%x")
#         print(f"{tag_label}", end=" ")
#         sources = set(map(by_name, find_sources(tag.commit.tree)))
#         print(f"num_source_files: {len(sources)}")
#         # TODO show adds and deletes
#         if len(sources - prev):
#             print(f"new files: {sorted(sources - prev)}")
#         prev = sources


def get_last_tag(repo, proj):
    tags = proj.list_interesting_tags(repo)
    return tags[-1]


def show_info(repo_path):
    proj = Project(dict(source_extensions=[".c", ".py"]))
    proj_name = os.path.basename(repo_path)
    if not proj_name:
        proj_name = os.path.basename(os.path.dirname(repo_path))
    proj_conf = proj_name + ".yaml"
    if os.path.exists(proj_conf):
        proj = Project(open(proj_conf))
    else:
        print(f"{proj_conf} - using default config")

    repo = Repo(repo_path)
    last_tag = get_last_tag(repo=repo, proj=proj)
    num_files = count(release=last_tag, findfunc=find_files)
    num_source = count(release=last_tag, findfunc=lambda tree: find_sources(tree, proj))

    print(f"{proj_name:12} {str(last_tag):12} {num_files:6} {num_source:6}")


def main():
    for repo_path in sys.argv[1:]:
        show_info(repo_path)


if __name__ == "__main__":
    main()
