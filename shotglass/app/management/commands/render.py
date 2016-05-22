# pylint: disable=no-member

import itertools
import logging
import json
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
            return (0, 25, 25)
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
    if not lines_total:
        print 'WARNING: {} is empty'.format(project)
        return 0
    return int(math.sqrt(lines_total) + 1)

def color_hsl(hue, saturation, lightness):
    return ImageColor.getrgb('hsl({}, {}%, {}%)'.format(
        hue, saturation, lightness))

def thispoint_iter():
    from .hilbert import int_to_Hilbert
    index_ = 0
    while True:
        yield tuple(int_to_Hilbert(index_))
        index_ += 1

def make_step_iter(step, max_):
    num = 0
    while True:
        yield num
        num = (num + step) % max_


def grid_hilbert_arg(project, width, argname='path', depth=None):
    theme = Theme()
    symbols = SourceLine.objects.filter(project=project
    ).order_by('tags_json', 'path', 'line_number')
    point = (0, 0)
    width *= 4                  # XX?
    grid = ImageGrid(width, width)
    first_spot = color_hsl(0, 0, 75) # light gray

    prev_arg = None
    prev_path = None
    highlight = 40
    hue,saturation = 0, 0
    hue_iter = make_step_iter(50, 360)
    saturation_iter = itertools.cycle([25, 70])
    highlight_iter = itertools.cycle([40, 60])
    thispoint = thispoint_iter()

    def arg_iter():
        for symbol in symbols:
            arg = getattr(symbol, argname)
            if depth and arg and argname.endswith('_json'):
                yield (symbol, json.loads(arg)[:depth])
            else:
                yield (symbol, arg)

    for symbol,arg in arg_iter():
        if symbol.path != prev_path:
            if prev_path:
                for _ in xrange(3):
                    thispoint.next()
            prev_path = symbol.path
        if prev_arg != arg:
            hue = hue_iter.next()
            print arg
            prev_arg = arg
            highlight = highlight_iter.next() # alternate args
        saturation = saturation_iter.next() # alternate symbols
        pen_hsl = (hue, saturation, highlight)
        pen = color_hsl(*pen_hsl)
        grid.draw(thispoint.next(), pen)
        if symbol.length <= 1:
            continue
        grid.moveto(thispoint.next())
        for _ in xrange(symbol.length-1):
            grid.drawto(thispoint.next(), pen)

    detail = ''
    if depth:
        detail = '_{}'.format(depth)
    argname = argname.split('_')[0]
    path = '{}_{}{}.png'.format(project, argname, detail)
    grid.render(path)
    print path


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
        projects = SourceLine.objects.values('project').distinct(
        ).values_list('project', flat=True)
        return sorted(filter(None, projects))

    def handle(self, *args, **options):
        if options['arg'] == 'tags':
            options['arg'] = 'tags_json'
        for project in self.get_projects(options['projects']):
            print '***', project
            width = options['width'] or calc_width(project)
            if not width:
                continue
            grid_hilbert_arg(project, width, options['arg'], options['depth'])
