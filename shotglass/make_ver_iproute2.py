#!/usr/bin/env python

'''
make_versions -- index many versions of a project

ALPHA code, will need modification for general use.
'''

import re
import subprocess
import sys

import git
from natsort import natsorted


PROJECT = 'iproute2'
PROJ_DIR = 'SOURCE/{}'.format(PROJECT)

bad_tag_re = re.compile(r'(rc|beta|alpha|jamal|ss)')

repos = git.Repo(PROJ_DIR)
tags = [tag.name for tag in repos.tags
    if tag.name.startswith('v') and not bad_tag_re.search(tag.name)]
tags = natsorted(tags)
print tags

checkout_cmd = 'cd {dir} ; git checkout {tag}'
index_cmd = './manage.py make_index --project={name}-{tag} {dir}'
for tag in tags:
    cmd = checkout_cmd.format(dir=PROJ_DIR, tag=tag)
    print '>>>', cmd
    if subprocess.call(cmd, shell=True):
        sys.exit(0)
    cmd = index_cmd.format(dir=PROJ_DIR, name=PROJECT, tag=tag)
    print '>>>', cmd
    out = subprocess.check_output(cmd, shell=True)
    print out
