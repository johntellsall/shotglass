# app/render.py

import colorsys
import itertools
import json
import logging
import math

from django.db.models import Sum
from PIL import Image, ImageColor, ImageDraw

from app import hilbert
from app.models import DiagramSymbol, SourceLine


logger = logging.getLogger(__name__)


class Grid(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, xy, color):
        print 'draw: {}, {}'.format(xy, color)

    def get_symbol_color(self, symbol):
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

    def draw(self, xy, color):
        x,y = xy
        if y >= len(self.data):
            self.data.append(self.blank_row[:])
        try:
            self.data[y][x] = color
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


def calc_width(project):
    lines_total = SourceLine.objects.filter( # pylint: disable=no-member
        project=project).aggregate(Sum('length'))['length__sum']
    if not lines_total:
        print 'WARNING: {} is empty'.format(project)
        return 0
    return int(math.sqrt(lines_total) + 1)


# X RGB values are off by one
def color_hsl_hex(hue, saturation, lightness):
    r,g,b = colorsys.hls_to_rgb(hue/99., lightness/99., saturation/99.)
    return '#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255))


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
        color = color_hsl_hex(hue, saturation, highlight)
        yield pos, symbol, arg, color


def draw_symbol(grid, pos, symbol_length, color):
    grid.draw(get_xy(pos), color)
    if symbol_length <= 1:
        return
    grid.moveto(get_xy(pos + 1))
    for offset in xrange(symbol_length):
        grid.drawto(get_xy(pos + offset + 1), color)


# X: unused
def draw_highlight(grid, diagram):
    folder_pos = [pos for pos, symbol, _, _ in diagram
                  if symbol.path.endswith('/setup.py')]
    folder_range = xrange(min(folder_pos), max(folder_pos))
    grid.draw_many((get_xy(pos) for pos in folder_range),
                   ImageColor.getrgb('white'))


def draw_box(grid, dsymbols, outline='white', fill=None):
    try:
        upleft_x = min(dsym.x for dsym in dsymbols)
        upleft_y = min(dsym.y for dsym in dsymbols)
        downright_x = max(dsym.x for dsym in dsymbols)
        downright_y = max(dsym.y for dsym in dsymbols)
    except ValueError:
        logger.warning('empty box: no symbols')
        return
    # 2? XX
    grid.im_draw.rectangle(
        [upleft_x*2, upleft_y*2, downright_x*2, downright_y*2],
        fill=fill, outline=outline)


class Diagram(list):
    @classmethod
    # pylint: disable=no-member
    def FromDB(cls):
        return Diagram(DiagramSymbol.objects.all())

    def render(self, symbols, argname, depth):
        def make_symbols(items):
            for pos, symbol, arg, color in items:
                x,y = get_xy(pos)
                yield DiagramSymbol(
                    color=color, position=pos, x=x, y=y, sourceline=symbol)

        skeleton = make_skeleton(symbols, argname, depth)
        items = add_color(skeleton)
        self[:] = make_symbols(items)

    def draw(self, grid):
        for dsymbol in self:
            draw_symbol(grid,
                        dsymbol.position,
                        symbol_length=dsymbol.sourceline.length,
                        color=dsymbol.color)

    # pylint: disable=no-member
    def dbsave(self):
        DiagramSymbol.objects.all().delete() # XX
        DiagramSymbol.objects.bulk_create(self)


def render(project, argname='path', depth=None):
    symbols = SourceLine.objects.filter( # pylint: disable=no-member
        project=project
    ).order_by('tags_json', 'path', 'line_number')

    if argname == 'tags':
        argname = 'tags_json'

    diagram = Diagram()
    diagram.render(symbols, argname, depth)
    diagram.dbsave()


def draw(project):
    width = calc_width(project)
    width *= 4                  # XX?
    grid = ImageGrid(width, width)

    diagram = Diagram.FromDB()
    diagram.draw(grid)
    grid.finalize()
    return grid


def draw_bbox(project):
    width = calc_width(project)
    width *= 4                  # XX?
    grid = ImageGrid(width, width)

    diagram = Diagram.FromDB()

    for path in set(dsym.sourceline.path for dsym in diagram):
        syms = [dsym for dsym in diagram
                if dsym.sourceline.path == path]
        draw_box(grid, syms, fill=syms[0].color)

    grid.finalize()
    return grid


def get_index(project):         # X
    # pylint: disable=no-member
    return DiagramSymbol.objects.order_by(
        'sourceline__name')
