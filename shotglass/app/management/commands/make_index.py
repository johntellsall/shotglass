#!/usr/bin/env python

import logging
import json
import os
import re
import subprocess
import sys

import ctags
import django.db
from django.core.management.base import BaseCommand
from radon.complexity import cc_visit

from app.models import SourceLine


INDEX_SUFFIXES = ('.c', '.py')

logging.basicConfig(
    format="%(asctime)-15s %(levelname)-8s %(message)s",
    stream=sys.stderr,
    level=logging.DEBUG)

# disable db query logs
logging.getLogger('django.db.backends').propagate = False
logger = logging.getLogger(__name__)


def calc_radon(path):
    code = open(path).read()
    funcs_data = cc_visit(code)
    # TODO: lines = max(func.endline for func in funcs_data)
    return dict((func.name, func.complexity)
        for func in funcs_data)


def calc_path_tags(path):
    tags = path.split('/')[:-1]
    return tags


def index_ctags(project, ctags_path):
    tagFile = ctags.CTags(ctags_path)
    entry = ctags.TagEntry()

    if not tagFile.find(entry, '', ctags.TAG_PARTIALMATCH):
        sys.exit('no tags?')

    while True:
        if entry['kind']:
            path = entry['file']
            tags = {'path': calc_path_tags(path)}
            try:
                SourceLine(name=entry['name'],
                           project=project,
                           path=path,
                           length=0, # XX should be None
                           line_number=entry['lineNumber'],
                           kind=entry['kind'],
                           tags_json=json.dumps(tags)).save()
            except django.db.utils.ProgrammingError:
                logger.error('%s: uhoh', entry['name'])
        status = tagFile.findNext(entry)
        if not status:
            break


# X: doesn't calc last symbol of each file correctly
def index_symbol_length(project):
    logger.debug('%s: calculating symbol lengths', project)
    source = SourceLine.objects.filter(project=project
        ).order_by('path', 'line_number')
    prev_path = None
    prev_symbol = None
    for symbol in source:
        if symbol.path != prev_path:
            prev_symbol = None
            prev_path = symbol.path
        if prev_symbol:
            prev_symbol.length = symbol.line_number - prev_symbol.line_number
            if prev_symbol.kind in ('variable', 'class'):
                prev_symbol.length = 1
            prev_symbol.save()
        prev_symbol = symbol


class Command(BaseCommand):
    help = 'beer'

    def add_arguments(self, parser):
        parser.add_argument('project_dir', metavar='FILE')
        parser.add_argument('--project')
        parser.add_argument('--tags')
        parser.add_argument('--list_path')

    def find_source_paths(self, top):
        # XX
        bad_dir_pat = re.compile(
            r'(contrib|debian|conf/locale|\.pc|pl|tests)')
        for root, _, names in os.walk(top):
            if bad_dir_pat.search(root):
                continue
            names = (name for name in names if name.endswith(INDEX_SUFFIXES))
            for path in (os.path.join(root, name) for name in names):
                yield path

    def find_source(self, project_dir, project):
        """
        find source code in tree, write to list file
        """
        paths = self.find_source_paths(top=project_dir)
        list_path = '{}.lst'.format(project)
        with open(list_path, 'w') as listf:
            listf.write('\n'.join(paths))
        return list_path

    def find_tags(self, project, list_path):
        """
        from selected source, find symbols
        """
        # Python: classes, functions, members, variables
        cmd = 'ctags --fields=afmikKlnsStz -L {} -o {}'
        tags_path = '{}.tags'.format(project)
        subprocess.check_call(
            cmd.format(list_path, tags_path), shell=True)
        return tags_path

    def make_index(self, project, tags_path):

        if django.db.connection.vendor == 'sqlite':
            django.db.connection.cursor().execute('PRAGMA synchronous=OFF')

        # XX: delete project's index
        # pylint: disable=no-member
        SourceLine.objects.filter(project=project).delete()
        index_ctags(project, tags_path)
        index_symbol_length(project)

    def format_project_name(self, project_dir):
        return project_dir.lstrip('./').rstrip('/')

    def handle(self, *args, **options):
        project_dir = options['project_dir']
        if not os.path.isdir(project_dir):
            sys.exit('{}: project must be directory'.format(project_dir))
        project_name = options.get(
            'project', self.format_project_name(project_dir))

        logger.info('%s: start', project_name)
        if not options['list_path']:
            logger.debug('%s: finding source', project_name)
            options['list_path'] = self.find_source(
                project_dir=project_dir, project=project_name)
        if not options['tags']:
            logger.debug('%s: finding tags', project_name)
            options['tags'] = self.find_tags(
                project_name, options['list_path'])

        self.make_index(project_name, options['tags'])
        # pylint: disable=no-member
        project_source = SourceLine.objects.filter(project=project_name)
        logger.info('%s: %s symbols', project_name,
                    '{:,}'.format(project_source.count()))

        logger.debug('%s: done', project_name)
