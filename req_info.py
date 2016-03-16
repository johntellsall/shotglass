#!/usr/bin/env python

'''
req_info.py -- calc size of Python packages
'''

import glob
import os
import subprocess


def is_interesting(dir_path):
    return os.path.isdir(dir_path) and not dir_path.endswith('-info')

def total_lines(path_format):
    """
    return total number of lines for all files that match "path_format" shell pattern
    """
    # X: shell errors out if path_format includes nonexistent subdirectories
    cmd = 'wc -l {} 2> /dev/null || true'.format(path_format)
    total_line = subprocess.check_output(cmd, shell=True, stderr=open(os.devnull)).strip().split('\n')[-1]
    return int(total_line.split()[0])
    
package_dir = os.path.join(os.environ['VIRTUAL_ENV'], 'lib/python*/site-packages')
for libdir in filter(is_interesting, glob.glob('{}/*'.format(package_dir))):
    print libdir
    print total_lines('{0}/*.py {0}/*/*.py'.format(libdir))
    blam
    
    
