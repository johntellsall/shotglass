#!/usr/bin/env python

"""
make_versions -- index many versions of a project

ALPHA code, will need modification for general use.
"""

import subprocess
import sys

checkout_cmd = "cd django ; git checkout stable/1.{minor}.x"
index_cmd = "./manage.py make_index --project=django-1.{minor} django"
for minor in range(0, 20):
    cmd = checkout_cmd.format(minor=minor)
    print(">>>", cmd)
    if subprocess.call(cmd, shell=True):
        sys.exit(0)
    cmd = index_cmd.format(minor=minor, shell=True)
    print(">>>", cmd)
    out = subprocess.check_output(cmd, shell=True)
    print(out)
