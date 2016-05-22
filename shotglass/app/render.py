# app/render.py

import itertools
import json
import math
import random

from django.db.models import Sum
from PIL import Image, ImageColor, ImageDraw

from app import hilbert
from app.models import SourceLine


class Grid(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, x, y, pen):
        print 'draw: {}, {}, {}'.format(x, y, pen)

    def get_symbol_pen(self, symbol):
        return symbol.name[0]

    def finalize(self):
        pass

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

    def finalize(self):
        self.im = self.im.crop(self.im.getbbox())

    def render(self, path):
        self.im.save(path)

    def make_pen(self, args):
        return ImageColor.getrgb('hsl({0}, {1}%, {2}%)'.format(
            int(args[0]), args[1], args[2]))


# XX unused
class Theme(object):
    def get_symbol_hsl(self, symbol):
        if symbol.kind not in ('function', 'member'):
            return (0, 25, 25)
        hue = random.randint(0, 360)
        return (hue, 75, 25)


# XX unused
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
    lines_total = SourceLine.objects.filter( # pylint: disable=no-member
        project=project).aggregate(Sum('length'))['length__sum']
    if not lines_total:
        print 'WARNING: {} is empty'.format(project)
        return 0
    return int(math.sqrt(lines_total) + 1)


def color_hsl(hue, saturation, lightness):
    return ImageColor.getrgb('hsl({}, {}%, {}%)'.format(
        hue, saturation, lightness))


def thispoint_iter():
    index_ = 0
    while True:
        yield tuple(hilbert.int_to_Hilbert(index_))
        index_ += 1


def make_step_iter(step, max_):
    num = 0
    while True:
        yield num
        num = (num + step) % max_


def grid_hilbert_arg(project, width, argname='path', depth=None):
    symbols = SourceLine.objects.filter( # pylint: disable=no-member
        project=project
    ).order_by('tags_json', 'path', 'line_number')
    width *= 4                  # XX?
    grid = ImageGrid(width, width)

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
    grid.finalize()
    return grid
