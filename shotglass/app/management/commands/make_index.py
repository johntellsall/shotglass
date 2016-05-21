#!/usr/bin/env python

import argparse
import fnmatch
import logging
import json
import os
import pprint
import re
import sys

import ctags
import django.db
from django.core.management.base import BaseCommand, CommandError

from app.models import SourceLine


logging.basicConfig(
    format="%(asctime)-15s %(levelname)-8s %(message)s",
    stream=sys.stderr,
    level=logging.DEBUG)
# disable db queries
logging.getLogger('django.db.backends').propagate = False
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'beer'

    def add_arguments(self, parser):
        # parser.add_argument('--paths', type=argparse.FileType('w'))
        parser.add_argument('--index', type=str) # XX
        parser.add_argument('--project')
        parser.add_argument('--prefix', default='')
        parser.add_argument('--tags', default='tags')
        parser.add_argument('--verbose', action='store_true')

        # $ find ./python-django-*/django
        # | egrep -v '/(contrib|debian|conf/locale|\.pc|tests)/' > django.lst

        # $ ctags --fields=afmikKlnsStz --languages=python -L django.lst -o django.tags
    def find_source_paths(self, top):
        # XX
        bad_dir_pat = re.compile(
            r'(contrib|debian|conf/locale|\.pc|pl|tests)')
        for root, dirs, names in os.walk(top):
            if bad_dir_pat.search(root):
                continue
            names = (name for name in names if name.endswith(('.c', '.py')))
            for path in (os.path.join(root, name) for name in names):
                yield path

    def handle(self, *args, **options):
        paths = self.find_source_paths(options['index'])
        index_name = os.path.basename(options['index'])
        list_path = '{}.lst'.format(index_name)
        with open(list_path, 'w') as sourcef:
            sourcef.write('\n'.join(paths))
            sourcef.write('\n')
        sys.exit(0)

        tagFile = ctags.CTags(options['tags'])
        entry = ctags.TagEntry()

        if not tagFile.find(entry, '', ctags.TAG_PARTIALMATCH):
            sys.exit('no tags?')

        if django.db.connection.vendor == 'sqlite':
            django.db.connection.cursor().execute('PRAGMA synchronous=OFF')

        SourceLine.objects.filter(project=options['project']).delete() # XX

        prefix = options['prefix']
        logger.debug('scanning source')
        while True:
            if entry['kind']:
                path = entry['file']
                if prefix and path.startswith(prefix):
                    path = path[len(prefix):].lstrip('/')
                tags = path.split('/')[:-1]
                tags_json = json.dumps(tags) if tags else None
                try:
                    SourceLine(name=entry['name'],
                               project=options['project'],
                               path=path,
                               length=0, # XX should be None
                               line_number=entry['lineNumber'],
                               kind=entry['kind'],
                               tags_json=tags_json).save()
                except django.db.utils.ProgrammingError:
                    logger.error('%s: uhoh', entry['name'])
            status = tagFile.findNext(entry)
            if not status:
                break

        # SourceLine.objects.bulk_create(rows)

        logger.debug('calculating sizes')
        source = SourceLine.objects.filter(project=options['project']).order_by('path', 'line_number')
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
        logger.debug('done')
