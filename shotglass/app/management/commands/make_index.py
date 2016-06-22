#!/usr/bin/env python

'''
make_index -- compile data from tree of source files
'''

# pylint: disable=bad-builtin

import logging
import os
import re
import subprocess

import django.db
from django.core.management.base import BaseCommand
from radon.complexity import cc_visit
from radon import visitors

from app import models


INDEX_SUFFIXES = ('.c', '.py')

if 0:
    # XX: never flushes logs!
    logger = logging.getLogger(__name__)
else:
    class HackLogger(object):
        def logme(self, myformat, *args):
            print '*', myformat % args
        debug = info = warning = logme
    logger = HackLogger()


def calc_radon(path):
    code = open(path).read()
    return cc_visit(code) # iter of blocks


def calc_path_tags(path):
    tags = path.split('/')[:-1]
    return tags


def format_project_name(project_dir):
    pdir = os.path.basename(project_dir.rstrip('/'))
    return pdir


def walk_type(topdir, name_func):
    for root, _, names in os.walk(topdir):
        paths = [os.path.join(root, name) for name in names
            if name_func(name)]
        for path in paths:
            yield path


# pylint: disable=no-member
def index_py_radon(project, paths):
    # X: Radon only supports Python
    for path in paths:
        for block in calc_radon(path):
            sourceline = models.SourceLine.objects.create(
                project=project,
                path=path,
                name=block.fullname,
                line_number=block.lineno,
                length=block.endline - block.lineno)
            assert block.letter in 'CFM'
            models.ProgRadon.objects.create(
                sourceline=sourceline,
                kind=block.letter,
                complexity=block.complexity)


# pylint: disable=no-member
def index_c_mccabe(project, paths):
    pmccabe_pat = re.compile(
        r'^(?P<data> [0-9\t]+)'
        r'(?P<path> .+?)'
        r'\( (?P<definition_line> \d+) \): \s+ '
        r'(?P<function> .+)',
        re.VERBOSE)

    paths = list(paths)
    logger.debug('%s: calculating C complexity, %d files',
        project, len(paths))
    if not paths:
        return

    output = subprocess.check_output(
        ['pmccabe'] + paths).split('\n')

    for match in filter(None, (map(pmccabe_pat.match, output))):
        data = [int(field) for field in match.group('data').split()]
        num_lines = data[4]
        definition_line = int(match.group('definition_line'))
        sourceline = models.SourceLine.objects.create(
            project=project,
            path=match.group('path'),
            name=match.group('function'),
            line_number=definition_line,
            length=num_lines)
        models.ProgPmccabe.objects.create(
            sourceline=sourceline,
            first_line=data[3],
            modified_mccabe=data[0],
            mccabe=data[1],
            num_statements=data[2],
            # overlap w/ SourceLine
            num_lines=num_lines,
            definition_line=definition_line)


def make_index(project, project_dir):
    is_c = re.compile(r'\.c$').search
    is_python = re.compile(r'\.py$').search
    
    if django.db.connection.vendor == 'sqlite':
        django.db.connection.cursor().execute('PRAGMA synchronous=OFF')

    # XX: delete project's index
    # pylint: disable=no-member
    models.SourceLine.objects.filter(project=project).delete()
    
    c_paths = list(walk_type(project_dir, is_c))
    logger.info('%s: %d C files', project, len(c_paths))
    index_c_mccabe(project, c_paths)
    # shows as "0" because of the PRAGMA SYNC above

    py_paths = list(walk_type(project_dir, is_python))
    logger.info('%s: %d Python files', project, len(py_paths))
    index_py_radon(project, py_paths)


class Command(BaseCommand):
    help = 'beer'

    def add_arguments(self, parser):
        parser.add_argument('project_dirs', metavar='FILE', nargs='+')
        parser.add_argument('--project')
        parser.add_argument('--tags')

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
