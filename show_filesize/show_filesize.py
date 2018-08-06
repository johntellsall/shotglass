#!/usr/bin/env python

'''
show_filesize.py -- show source sizes over time
'''

import os
import re
import sys
from collections import namedtuple

from colorama import Back, Fore, Style
from git import Repo
from natsort import natsorted


Source = namedtuple('Source', 'path lines')


def count_lines(lines):
    return sum(1 for line in lines)


# TODO make configurable
def is_interesting_name(name):
    return os.path.splitext(name)[-1] in ['.py']


# TODO make configurable
def is_interesting_path(path):
    if re.compile(r'^(docs|examples|scripts|tests)/').match(path):
        return False
    if re.compile('/testsuite/').search(path):
        return False
    return True


def find_sources(tree):
    # "calc info about every file in tree"
    for item in tag.commit.tree.traverse():
        if item.type != 'blob':
            continue
        if not is_interesting_path(item.path):
            continue
        if not is_interesting_name(item.name):
            continue
        stream = item.data_stream.stream
        num_lines = count_lines(stream.readlines())
        yield Source(path=item.path, lines=num_lines)


def by_name(source):
    return source.name


# TODO only count the N-largest files in the last tag tree
repo = Repo(sys.argv[1])
path_column = {}
for tag in natsorted(repo.tags, key=lambda t: t.name):
    tag_label = Back.GREEN + Fore.BLACK + f'{tag.name:6}' + Style.RESET_ALL
    print(f'{tag_label}', end=' ')
    sources = list(find_sources(tag.commit.tree))
    # for source in sources:
    #     print(f'{source.lines:5} {source.path}')
    for source in sources:
        if source.path not in path_column:
            path_column[source.path] = len(path_column)
    # TODO count columns better, set math?
    row = [None]*len(path_column)
    for source in sources:
        row[path_column[source.path]] = source
    dash = '-'
    for item in row:
        if item is None:
            print(f'{dash:4}', end=' ')
        else:
            print(f'{item.lines:4}', end=' ')
    print()
