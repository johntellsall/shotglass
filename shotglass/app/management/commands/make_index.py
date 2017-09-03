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
# from radon.complexity import cc_visit

from app import models
from app import render


INDEX_SUFFIXES = ('.c', '.py')
BORING_DIRS = ('.pc',) # TODO: make configurable

logging.basicConfig(
    stream=sys.stderr,
    level=logging.DEBUG,
    format='%(levelname)s %(module)s %(message)s',
)
logger = logging.getLogger(__name__)


def format_project_name(project_dir):
    return os.path.basename(project_dir.rstrip('/'))

def test_format_project_name():
    assert format_project_name('/a/b/') == 'b'

def walk_type(topdir, name_func):
    for root, dirs, names in os.walk(topdir, topdown=True):
        # don't scan boring directories
        dirs[:] = [mydir for mydir in dirs if mydir not in BORING_DIRS]
        paths = [os.path.join(root, name) for name in names
            if name_func(name)]
        for path in paths:
            yield path

def make_index(project, project_dir):
    is_python = re.compile(r'\.py$').search
    
    if django.db.connection.vendor == 'sqlite':
        django.db.connection.cursor().execute('PRAGMA synchronous=OFF')

    # XX: delete project's index
    # pylint: disable=no-member
    logger.info("project %s", project)
    if 1:
        logger.info("%s: zapping old data", project)
        proj_symbols = models.SourceLine.objects.filter(project=project)
        proj_symbols.delete()
 
    py_paths = list(walk_type(project_dir, is_python))
    logger.info('%s: %d Python files', project, len(py_paths))

#     render.render(proj_symbols)

class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('project_dirs', metavar='FILE', nargs='+')
        parser.add_argument('--project')
        # parser.add_argument('--tags')

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

            # pylint: disable=no-member
            project_source = models.SourceLine.objects.filter(
                project=project_name)
            # X: 0 because of PRAGMA SYNC
            logger.info('%s: %s symbols', project_name,
                        '{:,}'.format(project_source.count()))

            logger.debug('%s: done', project_name)
