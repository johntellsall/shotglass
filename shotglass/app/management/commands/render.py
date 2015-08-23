import colorsys
import sys
from collections import Counter

import ctags
from django.core.management.base import BaseCommand, CommandError
from PIL import Image, ImageColor, ImageDraw

from app.models import SourceLine

class Grid(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, x, y, pen):
        print 'draw: {}, {}, {}'.format(x, y, pen)

    def render(self, *args):
        pass
    
class ScreenGrid(Grid):
    def __init__(self, width, height):
        self.blank_row = ['.'] * width
        self.data = []
        super(ScreenGrid, self).__init__(width, height)

    def draw(self, x, y, pen):
        if y >= len(self.data):
            self.data.append(self.blank_row[:])
        try:
            self.data[y][x] = pen
        except IndexError:
            pass
        
    def render(self, *args):
        for row in self.data:
            print ''.join(row)

class ImageGrid(Grid):
    def __init__(self, width, height):
        self.im = Image.new('RGB', (width, height))
        self.im_draw = ImageDraw.Draw(self.im)
        super(ImageGrid, self).__init__(width, height)

    def draw(self, x, y, pen):
        self.im_draw.point([x, y], pen)

    def render(self, path):
        self.im.save(path)
        
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
        grid = ImageGrid(120, 80)
        cursor = Cursor(grid)
        prev_path = None
        for symbol in symbols:
            # ScreenGrid: cursor.step(symbol.name[0])
            pen = ImageColor.getrgb('hsl(0,100%,50%)')
            cursor.step(pen)
            if prev_path != symbol.path:
                if prev_path:
                    cursor.step(ImageColor.getrgb('white'))
                    print prev_path,
                prev_path = symbol.path
        grid.render('{}.png'.format(options['project']))
