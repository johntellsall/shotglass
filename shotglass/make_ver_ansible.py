#!/usr/bin/env python

"""
make_versions -- index many versions of a project

ALPHA code, will need modification for general use.
"""

import re
import subprocess
import sys

import git


NAME = "ansible"

bad_tag_re = re.compile(r"(rc|beta|alpha)")
repos = git.Repo(NAME)
tags = [
    tag.name
    for tag in repos.tags
    if tag.name.startswith("v") and not bad_tag_re.search(tag.name)
]

checkout_cmd = "cd {name} ; git checkout {tag}"
index_cmd = "./manage.py make_index --project={name}-{tag} {name}"
for tag in tags:
    cmd = checkout_cmd.format(name=NAME, tag=tag)
    print(">>>", cmd)
    if subprocess.call(cmd, shell=True):
        sys.exit(0)
    cmd = index_cmd.format(name=NAME, tag=tag)
    print(">>>", cmd)
    out = subprocess.check_output(cmd, shell=True)
    print(out)
