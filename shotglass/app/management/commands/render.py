# pylint: disable=no-member

# import itertools
# import logging
# import json
# import math
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Avg, Max, Sum

from app import render
from app.models import SourceLine


class Command(BaseCommand):
    help = 'beer'

    def add_arguments(self, parser):
        parser.add_argument('projects', nargs='+', default=['flask'])
        parser.add_argument('--grid', default='screen')
        parser.add_argument('--width', type=int)
        parser.add_argument('--arg', choices=('path', 'tags'),
                            default='path')
        parser.add_argument('--depth', type=int, default=0)

    def get_projects(self, projects):
        if projects != ['all']:
            return projects
        return SourceLine.projects()

    def handle(self, *args, **options):
        argname = options['arg']
        if argname == 'tags':
            argname = 'tags_json'
        depth = options['depth']

        for project in self.get_projects(options['projects']):
            print '***', project
            width = options['width'] or render.calc_width(project)
            if not width:
                continue
            grid = render.grid_hilbert_arg(project, width, argname, depth)

            detail = '_{}'.format(depth) if depth else ''
            argname2 = argname.split('_')[0]
            path = '{}_{}{}.png'.format(project, argname2, detail)
            grid.render(path)
            print path
