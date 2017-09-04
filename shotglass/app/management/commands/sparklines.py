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


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('projects', nargs='+')
        # parser.add_argument('--project')
        # # parser.add_argument('--tags')

    def handle(self, *args, **options):
        for project in options['projects']:
            print project
        # for project_dir in map(os.path.expanduser, options['project_dirs']):
        #     if not os.path.isdir(project_dir):
        #         logger.warning(
        #             '%s: project must be directory, skipping', project_dir)
        #         continue
            
        #     # X: doesn't support multiple dirs
        #     project_name = (options.get('project')
        #         or format_project_name(project_dir))

        #     logger.info('%s: start', project_name)
        #     make_index(project_name, project_dir)

        #     logger.debug('%s: done', project_name)
