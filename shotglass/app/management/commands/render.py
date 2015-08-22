import sys
from collections import Counter

import ctags
from django.core.management.base import BaseCommand, CommandError

from app.models import SourceLine

class Cursor(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dx = 1

    def draw(self, x, y, pen):
        print 'draw: {}, {}, {}'.format(x, y, pen)
        
    def step(self, pen, count=1):
        for _ in xrange(count):
            self.draw(self.x, self.y, pen)
            self.x += self.dx
            if self.x >= self.width:
                self.x = self.width-1
                self.y += 1
            elif self.x < 0:
                self.x = 0
                self.y += 1
        
class Command(BaseCommand):
    help = 'beer'

    def add_arguments(self, parser):
        parser.add_argument('--project', default='django')
        # parser.add_argument('--prefix', default='')
        # parser.add_argument('--verbose', action='store_true')

    def handle(self, *args, **options):
        my_symbols = SourceLine.objects.filter(project=options['project'])
        symbols = my_symbols.order_by('path')
        cursor = Cursor(0, 0, 20, 20)
        for symbol in symbols[:10]:
            print symbol.name
            cursor.step(symbol.name[0])
