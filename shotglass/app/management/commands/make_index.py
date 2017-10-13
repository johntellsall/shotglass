#!/usr/bin/env python

'''
make_index -- compile data from tree of source files
'''

# pylint: disable=bad-builtin

import logging
import os
import re
import subprocess
import sys

import django.db
from django.core.management.base import BaseCommand

from app.models import SourceFile
from app import render


LANGUAGE_TYPES = {
    '.c': 'c',
    '.cc': 'c++',
    '.go': 'golang',
    '.h': 'c',
    '.py': 'python',
}
BORING_DIRS = ('.pc',) # TODO: make configurable

logging.basicConfig(
    stream=sys.stderr,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


def format_project_name(project_dir):
    return os.path.basename(project_dir.rstrip('/'))

def test_format_project_name():
    assert format_project_name('/a/b/') == 'b'

def walk_type(topdir, name_func):
    "don't scan boring directories"
    for root, dirs, names in os.walk(topdir, topdown=True):
        dirs[:] = [mydir for mydir in dirs if mydir not in BORING_DIRS]
        paths = [os.path.join(root, name) for name in names
            if name_func(name)]
        for path in paths:
            yield path

def count_lines(project_dir, paths):
    cmd = ['wc', '-l']
    pat = re.compile(r'\s*(\d+)\s+(.+)')
    def is_interesting((num_str, path),):
       return num_str != '0' and path != 'total'

    result = subprocess.check_output(cmd + paths)
    lines = result.split('\n')[:-1]
    matches = (pat.match(line) for line in lines)
    info = filter(is_interesting, (m.groups() for m in matches if m))
    for num_str, path in info:
        rel_path = path.split(project_dir)[-1].lstrip('/')
        yield int(num_str), rel_path

def index_lines(project, num_path_iter):
    for num, rel_path in num_path_iter:
        name = os.path.split(rel_path)[-1]
        SourceFile.objects.create(
            project=project,
            name=name,
            path=rel_path,
            num_lines=num)

def make_index(project, project_dir, replace=True):
    def is_source(path):
        return os.path.splitext(path)[-1] in LANGUAGE_TYPES
    
    if django.db.connection.vendor == 'sqlite':
        django.db.connection.cursor().execute('PRAGMA synchronous=OFF')

    logger.info("project %s, directory %s", project, project_dir)
    if replace:
        logger.info("%s: zapping old data", project)
        proj_files = SourceFile.objects.filter(project=project)
        proj_files.delete()
 
    logger.info('%s: looking for source', project)
    paths = list(walk_type(project_dir, is_source))
    logger.info('%s: %d source files', 
        project, len(paths))

    proj_info = count_lines(project_dir, paths)
    index_lines(project, proj_info)
    logger.info('%s: indexed %d files', 
        project, SourceFile.objects.filter(project=project).count())

class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('project_dirs', metavar='FILE', nargs='+')

    def handle(self, *args, **options):
        for project_dir in map(os.path.expanduser, options['project_dirs']):
            if not os.path.isdir(project_dir):
                logger.warning(
                    '%s: project must be directory, skipping', project_dir)
                continue
            
            # X: doesn't support multiple dirs
            project_name = (options.get('project')
                or format_project_name(project_dir))

            logger.info('%s: start', project_name)
            make_index(project_name, project_dir)

            logger.info('%s: done', project_name)
