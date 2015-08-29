import sys
from collections import Counter

import ctags
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Avg, Max, Sum

from app.models import SourceLine


class Command(BaseCommand):
    help = 'beer'

    def add_arguments(self, parser):
        parser.add_argument('projects', nargs='+', default=['django'])

    def old_handle(self, *args, **options):
        my_symbols = SourceLine.objects.filter(project=options['project'])
        symbols = my_symbols.order_by('path')
        count_kind = Counter()
        paths = set()
        for symbol in symbols:
            count_kind[symbol.kind] += 1
            paths.add(symbol.path)

        # TODO: calc in database
        print 'files:', len(set(my_symbols.values_list('path')))
        print 'symbols:'
        for name, value in sorted(count_kind.iteritems()):
            print '\t{} {}'.format(name, value)
        print '\ttotal:', sum(count_kind.values())
        

    HEADER = ''
    FORMAT = '{project:12} {num_symbols:6} {max_length:5} {avg_length:4} {total_length:6}'
    def handle(self, *args, **options):
        projects = options['projects']
        # if projects == ['all']:
        #     projects = 
        for project in projects:
            symbols = SourceLine.objects.filter(project=project)
            num_symbols = symbols.count()
            num_functions = symbols.filter(kind__in=('function', 'member')).count()
            # TODO: optimize
            max_length = symbols.aggregate(Max('length')).values()[0]
            avg_length = int(symbols.aggregate(Avg('length')).values()[0])
            total_length = symbols.aggregate(Sum('length')).values()[0]
            print self.FORMAT.format(**locals())
