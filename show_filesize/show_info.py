#!/usr/bin/env python

'''
show_info.py -- show source sizes over time
'''

import os
import re
import sys
from collections import namedtuple

from colorama import Back, Fore, Style
from git import Repo
from natsort import natsorted

class Project:
    config = None
    def parse_yaml(self, obj):
        self.config = yaml.load(obj)

    def is_interesting_item(self, item):
        def is_interesting_name(name):
            return os.path.splitext(name)[-1] in ['.c', '.py']
        return (item.type == 'blob' and
        # is_interesting_path(item.path) and
        is_interesting_name(item.name))



# TODO make configurable
def is_interesting_path(path):
    if re.compile(r'^(docs|examples|scripts|tests|__init)/').match(path):
        return False
    if re.compile('/testsuite/').search(path):
        return False
    return True

def is_interesting_item(item):
    return (item.type == 'blob' and
        is_interesting_path(item.path) and
        is_interesting_name(item.name))
# TODO make configurable
def is_interesting_name(name):
    return os.path.splitext(name)[-1] in ['.c', '.py']


# TODO make configurable
def is_interesting_path(path):
    if re.compile(r'^(docs|examples|scripts|tests|__init)/').match(path):
        return False
    if re.compile('/testsuite/').search(path):
        return False
    return True

def is_interesting_item(item):
    return (item.type == 'blob' and
        is_interesting_path(item.path) and
        is_interesting_name(item.name))

def find_sources(tree):
    source_items = tree.traverse(predicate=lambda item,_: is_interesting_item(item))
    return source_items

def find_sources2(tree):
    proj = Project()
    proj.config = dict(path_extensions=['.c', '.py'])
    source_items = tree.traverse(predicate=lambda item,_: proj.is_interesting_item(item))
    return source_items

repo = Repo(sys.argv[1])
tree = repo.tags['0.8'].commit.tree
paths = set(x.path for x in find_sources(tree))
print(paths)
paths2 = set(x.path for x in find_sources2(tree))
print(paths2)
print('=>', len(set(paths) ^ set(paths2)))
sys.exit(0)

def by_name(source):
    return source.name

def count_release(release):
    return len(list(find_sources(release.commit.tree)))


repo = Repo(sys.argv[1])
releases = natsorted(repo.tags, key=by_name)
print(f'releases: {len(releases)}')

num_first = count_release(releases[0])
num_last = count_release(releases[-1])
print(f'first: {releases[0]} num_source_files: {num_first}')
print(f'last: {releases[-1]} num_source_files: {num_last}')

prev = set()
for tag in natsorted(repo.tags, key=by_name):
    tag_label = f'{tag.name:10}'
    if 1:
        tag_label = Back.GREEN + Fore.BLACK + f'{tag.name:6}' + Style.RESET_ALL
    # show release date
    # TODO check first commit date is really the release date
    if 1:
        tag_label += ' ' + tag.commit.committed_datetime.strftime('%x')
    print(f'{tag_label}', end=' ')
    sources = set(map(by_name, find_sources(tag.commit.tree)))
    print(f'num_source_files: {len(sources)}')
    # TODO show adds and deletes
    if len(sources - prev):
        print(f'new files: {sorted(sources - prev)}')
    prev = sources

