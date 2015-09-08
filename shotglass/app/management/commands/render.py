import logging
import math
import random
import sys
from collections import Counter

import ctags
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Avg, Max, Sum
from PIL import Image, ImageColor, ImageDraw

from app.models import SourceLine

class Grid(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, x, y, pen):
        print 'draw: {}, {}, {}'.format(x, y, pen)

    def get_symbol_pen(self, symbol):
        return symbol.name[0]
    
    def render(self, *args):
        pass
    
class TextGrid(Grid):
    def __init__(self, width, height):
        self.blank_row = ['.'] * width
        self.data = []
        super(TextGrid, self).__init__(width, height)

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
        self.last = (0, 0)
        super(ImageGrid, self).__init__(width, height)

    def moveto(self, xy):
        self.last = (xy[0]*2, xy[1]*2)
        
    def draw(self, xy, pen):
        self.im_draw.point((xy[0]*2, xy[1]*2), pen)

    def drawto(self, xy, pen):
        xy = (xy[0]*2, xy[1]*2)
        if self.last:
            self.im_draw.line((self.last, xy), pen)
        self.last = xy

    def render(self, path):
        self.im.save(path)

    def make_pen(self, args):
        return ImageColor.getrgb('hsl({0}, {1}%, {2}%)'.format(
            int(args[0]), args[1], args[2]))

class Theme(object):
    def get_symbol_hsl(self, symbol):
        if symbol.kind not in ('function', 'member'):
            print symbol.__dict__
            return (0, 100, 50)
        hue = random.randint(0, 360)
        return (hue, 75, 25)
    
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
        
def calc_width(project):
    lines_total = SourceLine.objects.filter(
        project=project).aggregate(Sum('length'))['length__sum']

    return int(math.sqrt(lines_total) + 1)

def color_hsl(hue, saturation, lightness):
    return ImageColor.getrgb('hsl({}, {}%, {}%)'.format(
        hue, saturation, lightness))

def grid_hilbert(project, width):
    from .hilbert import int_to_Hilbert
    theme = Theme()
    symbols = SourceLine.objects.filter(project=project
    ).order_by('path', 'line_number')
    index_ = 0
    point = (0, 0)
    width *= 2
    grid = ImageGrid(width, width)
    first_spot = color_hsl(0, 0, 75) # light gray

    def thispoint_iter():
        for index_ in xrange(100000):
            yield tuple(int_to_Hilbert(index_))
    
    thispoint = thispoint_iter()
    for num,symbol in enumerate(symbols):
        pen_hsl = theme.get_symbol_hsl(symbol)
        pen = color_hsl(*pen_hsl)
        if 0:
            print '{:6} {:9} {:8}'.format(index_, point, pen),
            print symbol.path, symbol.name, symbol.length
        grid.draw(thispoint.next(), first_spot)
        if symbol.length <= 1:
            continue
        grid.moveto(thispoint.next())
        for _ in xrange(symbol.length-1):
            grid.drawto(thispoint.next(), pen)

    grid.render('{}.png'.format(project))
        
def render_project(project, text_mode, width):
    my_symbols = SourceLine.objects.filter(project=project)
    symbols = my_symbols.order_by('path', 'line_number')

    grid = TextGrid(width, 0) if text_mode else ImageGrid(width, width)

    cursor = Cursor(grid)
    prev_path = None

    for symbol in symbols:
        highlight = not text_mode and symbol.path=='fs.c' # XX
        color = grid.get_symbol_hsl(symbol)
        if highlight:
            color = (color[0], 75, 75)
        pen = grid.make_pen(color)
        cursor.step(pen, count=symbol.length)
        if prev_path != symbol.path:
            if prev_path:
                if not text_mode:
                    cursor.step(ImageColor.getrgb('black'))
                    cursor.step(ImageColor.getrgb('black'))
            prev_path = symbol.path
    if not text_mode:
        name = '{}.png'.format(project)
        grid.render(name)
        print name
    else:
        grid.render()
            
    
class Command(BaseCommand):
    help = 'beer'

    def add_arguments(self, parser):
        parser.add_argument('projects', nargs='+', default=['flask'])
        parser.add_argument('--grid', default='screen')
        parser.add_argument('--width', type=int)

    def get_projects(self, projects):
        if projects != ['all']:
            return projects
        projects = SourceLine.objects.values('project').distinct(
        ).values_list('project', flat=True)
        return sorted(filter(None, projects))
    
    def handle(self, *args, **options):
        width = options['width'] or calc_width(options['projects'][0])
        # import ipdb ; ipdb.set_trace()
        grid_hilbert(options['projects'][0], width)
# do_hilbert(options['projects'], width)
        return
        projects = self.get_projects(options['projects'])

        for project in projects:
            print project, 

            # default make square image
            width = options['width'] or calc_width(project)

            text_mode = options['grid'] == 'text'
            render_project(project, text_mode, width)
            
            
