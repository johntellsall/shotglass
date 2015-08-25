import sys
from collections import Counter

import ctags
from django.core.management.base import BaseCommand, CommandError

from app.models import SourceLine


class Command(BaseCommand):
    help = 'beer'

    def add_arguments(self, parser):
        parser.add_argument('--project', default='django')

    def handle(self, *args, **options):
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
        
        
