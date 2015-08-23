import sys
from collections import Counter

import ctags
from django.core.management.base import BaseCommand, CommandError

from app.models import SourceLine

class Grid(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, x, y, pen):
        print 'draw: {}, {}, {}'.format(x, y, pen)

    def render(self):
        pass
    
class ScreenGrid(Grid):
    def __init__(self, width, height):
        self.blank_row = ['.'] * width
        self.data = [] # self.blank_rowrow[:] for _ in xrange(height)]
        super(ScreenGrid, self).__init__(width, height)

    def draw(self, x, y, pen):
        if y >= len(self.data):
            self.data.append(self.blank_row[:])
        try:
            self.data[y][x] = pen
        except IndexError:
            pass
        
    def render(self):
        for row in self.data:
            print ''.join(row)
            
class Cursor(object):
    def __init__(self, grid):
        self.x = 0
        self.y = 0
        self.grid = grid
        self.dx = 1
        
    def step(self, pen, count=1):
        for _ in xrange(count):
            self.grid.draw(self.x, self.y, pen)
            self.x += self.dx
            if self.x >= self.grid.width:
                self.x = self.grid.width-1
                self.y += 1
                self.dx *= -1
            elif self.x < 0:
                self.x = 0
                self.y += 1
                self.dx *= -1
        
class Command(BaseCommand):
    help = 'beer'

    def add_arguments(self, parser):
        parser.add_argument('--project', default='django')
        # parser.add_argument('--prefix', default='')
        # parser.add_argument('--verbose', action='store_true')

    def handle(self, *args, **options):
        my_symbols = SourceLine.objects.filter(project=options['project'])
        symbols = my_symbols.order_by('path')
        grid = ScreenGrid(120, 20)
        cursor = Cursor(grid)
        for symbol in symbols:
            # print symbol.name
            cursor.step(symbol.name[0])
        grid.render()
