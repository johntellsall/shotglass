#!/usr/bin/env python

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
        for num,(name, path) in enumerate(namepaths):
            if '_' in name:
                print name.split('_')
            elif camelcase_pat.match(name):
                print camelcase_pat.findall(name)
            else:
                print name
            if num > 500:
                break
