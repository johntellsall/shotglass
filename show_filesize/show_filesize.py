#!/usr/bin/env python

'''
show_filesize.py -- show source sizes over time
'''

import os
import re
import sys

from colorama import Fore, Style
from git import Repo
from natsort import natsorted


def count_lines(path):
    return sum(1 for line in open(path, newline=None))


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


repo = Repo(sys.argv[1])
for tag in natsorted(repo.tags, key=lambda t: t.name):
    print(Fore.GREEN + f'### {tag.name}' + Style.RESET_ALL)

    for item in tag.commit.tree.traverse():
        if item.type != 'blob':
            continue
        if not is_interesting_path(item.path):
            continue
        if not is_interesting_name(item.name):
            continue
        # import ipdb ; ipdb.set_trace()
        num_bytes = item.size
        print(f'{num_bytes:5} {item.path}')
