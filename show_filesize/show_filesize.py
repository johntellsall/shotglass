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


def calc_stripe(tree):
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


repo = Repo(sys.argv[1])
column = {}
for tag in natsorted(repo.tags, key=lambda t: t.name):
    print(Back.GREEN + Fore.BLACK + f'### {tag.name}' + Style.RESET_ALL)
    stripe = calc_stripe(tag.commit.tree)
    for source in stripe:
        print(f'{source.lines:5} {source.path}')
