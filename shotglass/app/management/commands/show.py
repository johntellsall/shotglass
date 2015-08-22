import sys
from collections import Counter

import ctags
from django.core.management.base import BaseCommand, CommandError

from app.models import SourceLine


class Command(BaseCommand):
    help = 'beer'

    def add_arguments(self, parser):
        parser.add_argument('--project', default='django')
        # parser.add_argument('--prefix', default='')
        # parser.add_argument('--verbose', action='store_true')

    def handle(self, *args, **options):
        # , kind__in=('function', 'member')
        my_symbols = SourceLine.objects.filter(project=options['project'])
        symbols = my_symbols.order_by('path')
        count_kind = Counter()
        for symbol in symbols:
            count_kind[symbol.kind] += 1
            if 0:
                nice = dict((key, value) for key, value in line.__dict__.iteritems() if not key.startswith('_'))
                print '{name:40} {kind:12} {path}:{line_number}'.format(**nice)
        print 'files:', len(set(my_symbols.values_list('path')))
        print 'total:', sum(count_kind.values())
        print count_kind
        
