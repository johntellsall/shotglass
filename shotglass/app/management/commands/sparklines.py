#!/usr/bin/env python

'''
sparklines -- XX
'''

# pylint: disable=bad-builtin

import logging
import sys

import django.db
import sparklines
from django.core.management.base import BaseCommand

from app.models import SourceFile
from app import render


logging.basicConfig(
    stream=sys.stderr,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


def plot(project):
    WIDTH = 20
    query = SourceFile.objects.order_by(
        '-num_lines').values_list('num_lines', flat=True)
    largest, count = query.first(), query.count()
    print '{project}: {count} Python files, largest = {largest} lines'.format(
        **locals())

    def make_sparkline():
        for i in range(0, len(query), len(query)/WIDTH):
            yield query[i]
    import ipdb ; ipdb.set_trace()
    print sparklines.sparklines(make_sparkline())


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('projects', nargs='+')
        # parser.add_argument('--project')
        # # parser.add_argument('--tags')

    def handle(self, *args, **options):
        for project in options['projects']:
            print project
            plot(project)
