#!/usr/bin/env python

import logging
import sys

import ctags
from django.core.management.base import BaseCommand, CommandError
from django.db import connection

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
        parser.add_argument('--project')
        parser.add_argument('--prefix', default='')
        parser.add_argument('--tags', default='tags')
        parser.add_argument('--verbose', action='store_true')

    def handle(self, *args, **options):
        tagFile = ctags.CTags(options['tags'])
        entry = ctags.TagEntry()

        if not tagFile.find(entry, '', ctags.TAG_PARTIALMATCH):
            sys.exit('no tags?')
            
        if connection.vendor == 'sqlite':
            connection.cursor().execute('PRAGMA synchronous=OFF')

        SourceLine.objects.filter(project=options['project']).delete() # XX

        prefix = options['prefix']
        # rows = []
        logger.debug('scanning source')
        while True:
            if entry['kind']:
                path = entry['file']
                if prefix and path.startswith(prefix):
                    path = path[len(prefix):].lstrip('/')
                SourceLine(name=entry['name'],
                           project=options['project'],
                           path=path,
                           length=0, # XX should be None
                           line_number=entry['lineNumber'],
                           kind=entry['kind']).save()
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
