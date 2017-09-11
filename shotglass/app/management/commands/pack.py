#!/usr/bin/env python

'''
pack -- 
'''

import logging
import operator
import math
import sys

import django.db
import rectpack
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


def box_dimensions(lines):
    dim = math.ceil(math.sqrt(lines))
    return [dim, dim]

def pack(project):
    "pack each file sized according to count of source lines"
    file_data = SourceFile.objects.filter(
        project=project).values_list('path', 'num_lines')
    total_lines = sum(item[1] for item in file_data)
    bin_lines = 2*total_lines # heuristic!
    
    packer = rectpack.newPacker()
    packer.add_bin(*box_dimensions(bin_lines))
    for path,num_lines in file_data:
        packer.add_rect(*box_dimensions(num_lines), rid=path)

    packer.pack()
    # (b, x, y, w, h, rid)
    for pack_info in packer.rect_list():
        print pack_info[1], pack_info[-1]



class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('projects', nargs='+')
        # parser.add_argument('--project')
        # # parser.add_argument('--tags')

    def handle(self, *args, **options):
        projects = options['projects']
        if projects == ['all']:
            projects = SourceFile.projects()

        for project in projects:
            pack(project)
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
