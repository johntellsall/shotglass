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


# TODO make configurable
def is_interesting_name(name):
    return os.path.splitext(name)[-1] in ['.c', '.py']


# TODO make configurable
def is_interesting_path(path):
    if re.compile(r'^(docs|examples|scripts|tests)/').match(path):
        return False
    if re.compile('/testsuite/').search(path):
        return False
    return True

def is_interesting_item(item):
    return (item.type == 'blob' and
        is_interesting_path(item.path) and
        is_interesting_name(item.name))

def find_sources(tree):
    # "calc info about every file in tree"
    source_items = tree.traverse(predicate=lambda item,_: is_interesting_item(item))
    return source_items

def by_name(source):
    return source.name

def count_release(release):
    return len(list(find_sources(release.commit.tree)))


repo = Repo(sys.argv[1])
releases = natsorted(repo.tags, key=by_name)
print(f'releases: {len(releases)}')

num_first = count_release(releases[0])
num_last = count_release(releases[-1])
print(f'first: {releases[0]} num_files: {num_first}')
print(f'last: {releases[-1]} num_files: {num_last}')
sys.exit(1)
path_column = {}
for tag in natsorted(repo.tags, key=by_name):
    tag_label = f'{tag.name:6}'
    if 1:
        tag_label = Back.GREEN + Fore.BLACK + f'{tag.name:6}' + Style.RESET_ALL
    print(f'{tag_label}', end=' ')
    sources = list(find_sources(tag.commit.tree))
    adjust_columns(path_column, sources)
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
