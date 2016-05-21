import sys
from collections import Counter

import ctags
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Avg, Max, Sum

from app.models import SourceLine


class Command(BaseCommand):
    help = 'beer'

    HEADER = '{:20} {:>7} {:>5} {:>4} {:>8}'.format(
        'project', 'symbols', 'max', 'avg', 'total')
    FORMAT = ('{project:20} {num_symbols:7,} {max_length:5}'
              ' {avg_length:4} {total_length:8,}')

    def add_arguments(self, parser):
        parser.add_argument('projects', nargs='*')

    def get_all_projects(self):
        projects = SourceLine.objects.values('project').distinct(
        ).values_list('project', flat=True)
        return sorted(filter(None, projects))

    def handle(self, *args, **options):
        if not options['projects']:
            all_projects = self.get_all_projects()
            print('PROJECTS: {}'.format(', '.join(all_projects)))
            print('or "all"')
            return
        projects = options['projects']
        if projects == ['all']:
            projects = self.get_all_projects()

        print self.HEADER
        for project in projects:
            symbols = SourceLine.objects.filter(project=project)
            num_symbols = symbols.count()
            num_functions = symbols.filter(kind__in=('function', 'member')).count()
            # TODO: optimize
            if not num_symbols:
                max_length = avg_length = total_length = 0
            else:
                max_length = symbols.aggregate(Max('length')).values()[0]
                avg_length = int(symbols.aggregate(Avg('length')).values()[0])
                total_length = symbols.aggregate(Sum('length')).values()[0]
            print self.FORMAT.format(**locals())
