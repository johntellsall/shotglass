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
        pass # parser.add_argument('projects', nargs='+')

    def handle(self, *args, **options):
        camelcase_pat = re.compile('[A-Z][a-z]*')
        namepaths = SourceLine.objects.filter(
            project='flask').values_list(
            'name', 'path')
        path_words = collections.defaultdict(
            collections.Counter)

        for num,(name, path) in enumerate(namepaths):
            names = [name]
            if '_' in name:
                names = name.split('_')
            elif camelcase_pat.match(name):
                names = camelcase_pat.findall(name)
            path_words[path].update(filter(None, names))
            if num > 500:
                break

        for path, words in sorted(path_words.iteritems()):
            print path, words.most_common(3)
