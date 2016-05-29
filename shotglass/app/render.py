# app/render.py

import itertools
import json
import math

from django.db.models import Sum
from PIL import Image, ImageColor, ImageDraw

from app import hilbert
from app.models import SourceLine


class Grid(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, xy, pen):
        print 'draw: {}, {}'.format(xy, pen)

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

    def draw(self, xy, pen):
        x,y = xy
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

    def draw_many(self, xy_iter, pen):
        self.moveto(xy_iter.next())
        for xy in xy_iter:
            self.drawto(xy, pen)

    def finalize(self):
        self.im = self.im.crop(self.im.getbbox())

    def render(self, path):
        self.im.save(path)

    def make_pen(self, args):
        return ImageColor.getrgb('hsl({0}, {1}%, {2}%)'.format(
            int(args[0]), args[1], args[2]))


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


def make_hilbert_iter():
    index_ = 0
    while True:
        yield tuple(hilbert.int_to_Hilbert(index_))
        index_ += 1


def make_step_iter(step, max_):
    num = 0
    while True:
        yield num
        num = (num + step) % max_


def get_xy(pos):
    return hilbert.int_to_Hilbert(pos)


def make_skeleton(symbols, argname, depth):
    """
    calculate position of each symbol
    """
    def arg_iter():
        'iterate by "args", generally filenames'
        for symbol in symbols:
            arg = getattr(symbol, argname)
            if depth and arg and argname.endswith('_json'):
                yield (symbol, json.loads(arg)[:depth])
            else:
                yield (symbol, arg)

    prev_path = None
    pos = 0
    for symbol, arg in arg_iter():
        yield pos, symbol, arg
        pos += 1
        if symbol.path != prev_path:
            if prev_path:
                pos += 2        # add black smudge
            prev_path = symbol.path
        pos += symbol.length - 1


def add_color(skeleton):
    prev_arg = None
    highlight = 40
    hue,saturation = 0, 0
    hue_iter = make_step_iter(50, 360)
    saturation_iter = itertools.cycle([30, 60, 80])
    highlight_iter = itertools.cycle([40, 60])

    for pos, symbol, arg in skeleton:
        # change color with new arg (file)
        if prev_arg != arg:
            hue = hue_iter.next()
            prev_arg = arg
            highlight = highlight_iter.next() # X?
        # alternate symbols: different saturation
        saturation = saturation_iter.next()
        pen = color_hsl(hue, saturation, highlight)
        yield pos, symbol, arg, pen


def draw_symbol(grid, pos, symbol, pen):
    grid.draw(get_xy(pos), pen)
    if symbol.length <= 1:
        return
    grid.moveto(get_xy(pos + 1))
    for offset in xrange(symbol.length):
        grid.drawto(get_xy(pos + offset + 1), pen)


class Diagram(list):
    def render(self, symbols, argname, depth):
        skeleton = make_skeleton(symbols, argname, depth)
        self[:] = list(add_color(skeleton))


def grid_hilbert_arg(project, width, argname='path', depth=None):
    symbols = SourceLine.objects.filter( # pylint: disable=no-member
        project=project
    ).order_by('tags_json', 'path', 'line_number')

    if argname == 'tags':
        argname = 'tags_json'

    diagram = Diagram()
    diagram.render(symbols, argname, depth)
    width *= 4                  # XX?
    grid = ImageGrid(width, width)

    for pos, symbol, _, pen in diagram:
        draw_symbol(grid, pos, symbol, pen)

    if 1:
        folder_pos = [pos for pos, symbol, _, _ in diagram
                      if symbol.path.endswith('/setup.py')]
        folder_range = xrange(min(folder_pos), max(folder_pos))
        grid.draw_many((get_xy(pos) for pos in folder_range),
                       ImageColor.getrgb('white'))

    grid.finalize()
    return grid
