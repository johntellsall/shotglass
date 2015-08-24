#!/usr/bin/env python

import sys

import ctags
from django.core.management.base import BaseCommand, CommandError
from django.db import connection

from app.models import SourceLine


class Command(BaseCommand):
    help = 'beer'

    def add_arguments(self, parser):
        parser.add_argument('--project')
        parser.add_argument('--prefix', default='')
        parser.add_argument('--verbose', action='store_true')

    def handle(self, *args, **options):
        tagFile = ctags.CTags('tags')
        entry = ctags.TagEntry()

        if not tagFile.find(entry, '', ctags.TAG_PARTIALMATCH):
            sys.exit('no tags?')
            
        prefix = options['prefix']
        rows = []
        while True:
            if entry['kind']:
                path = entry['file']
                if prefix and path.startswith(prefix):
                    path = path[len(prefix):].lstrip('/')
                rows.append(SourceLine(name=entry['name'],
                                       project=options['project'],
                                       path=path,
                                       length=0, # XX should be None
                                       line_number=entry['lineNumber'],
                                       kind=entry['kind']))
                if options['verbose']:
                    print rows[-1].__dict__
            status = tagFile.findNext(entry)
            if not status:
                break

        SourceLine.objects.filter(project=options['project']).delete() # XX
        SourceLine.objects.bulk_create(rows)
        
        source = SourceLine.objects.filter(project=options['project']).order_by('path', 'line_number')
        if connection.vendor == 'sqlite':
            connection.cursor().execute('PRAGMA synchronous=OFF')
        prev_path = None
        prev_symbol = None
        for symbol in source:
            if symbol.path != prev_path:
                prev_symbol = None
                prev_path = symbol.path
            if prev_symbol:
                prev_symbol.length = symbol.line_number - prev_symbol.line_number
                prev_symbol.save()
            prev_symbol = symbol
