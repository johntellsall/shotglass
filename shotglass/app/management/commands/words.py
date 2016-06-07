#!/usr/bin/env python

import collections
import logging
import re
import sys

from django.core.management.base import BaseCommand

from app.models import SourceLine


logging.basicConfig(
    format="%(asctime)-15s %(levelname)-8s %(message)s",
    stream=sys.stderr,
    level=logging.DEBUG)

# disable db query logs
logging.getLogger('django.db.backends').propagate = False
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'beer'

    def add_arguments(self, parser):
        parser.add_argument('projects', nargs='+')

    def handle(self, *args, **options):
        camelcase_pat = re.compile('[A-Z][a-z]*')
        for project in options['projects']:
            print '*', project.upper()
            namepaths = SourceLine.objects.filter(
                project=project).values_list(
                    'name', 'path')
            path_words = collections.defaultdict(
                collections.Counter)

            for num,(name, path) in enumerate(namepaths):
                names = [name.lower()]
                if '_' in name:
                    names = name.lower().split('_')
                elif camelcase_pat.match(name):
                    names = camelcase_pat.findall(name.lower())
                path_words[path].update(filter(None, names))

            for path, words in sorted(path_words.iteritems()):
                relpath = re.sub('^.+?/', '', path)
                common = [(word, count)
                          for word, count in words.most_common(3)
                          if count > 1]
                if common:
                    print '{:30} {}'.format(relpath, common if common else '')