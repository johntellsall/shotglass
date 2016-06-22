# app/render.py

import colorsys
import itertools
import json
import logging

from palettable import colorbrewer
from radon.complexity import cc_rank

from app import hilbert
from app.grid import ImageGrid
from app.models import DiagramSymbol, SourceLine


COLOR_CC_UNKNOWN = 'gray'

logger = logging.getLogger(__name__)


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


get_xy = hilbert.int_to_Hilbert


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


def jm_add_color(skeleton):
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


# palette examples
# https://jiffyclub.github.io/palettable/colorbrewer/diverging/#brbg_11
def pal_add_color(skeleton):
    # pylint: disable=no-member
    colors = colorbrewer.diverging.RdBu_11_r.hex_colors
    prev_arg = None
    color_iter = itertools.cycle(colors)
    for pos, symbol, arg in skeleton:
        # change color with new arg (file)
        if prev_arg != arg:
            color = color_iter.next()
            prev_arg = arg
        yield pos, symbol, arg, color


def cc_add_color(skeleton):
    # pylint: disable=no-member
    colors = colorbrewer.diverging.RdBu_5_r.hex_colors 
    colormap = dict(zip('ABCDE', colors))
    colormap['F'] = colormap['E']

    # X: speedup w/ queryset.select_related('progpmccabe')
    for pos, symbol, arg in skeleton:
        cc_value = None
        try:
            cc_value = symbol.progpmccabe.mccabe
        except AttributeError:
            try:
                cc_value = symbol.progradon.complexity
            except AttributeError:
                pass
        if cc_value is None:
            # symbol lacks complexity value
            yield pos, symbol, arg, COLOR_CC_UNKNOWN
        else:
            try:
                color = colormap[cc_rank(cc_value)]
                yield pos, symbol, arg, color
            except (KeyError, TypeError):
                logger.debug('? %s', symbol.name)
                yield pos, symbol, arg, COLOR_CC_UNKNOWN
        
add_color = cc_add_color


def draw_symbol(grid, pos, symbol_length, color):
    if symbol_length <= 1:
        return
    # draw white "grain of rice" at start of symbol
    grid.moveto(get_xy(pos))
    grid.drawto(get_xy(pos + 1), '#fff')
    for offset in xrange(symbol_length):
        grid.drawto(get_xy(pos + offset + 1), color)


# X: unused
def draw_highlight(grid, diagram):
    folder_pos = [pos for pos, symbol, _, _ in diagram
                  if symbol.path.endswith('/setup.py')]
    folder_range = xrange(min(folder_pos), max(folder_pos))
    grid.draw_many((get_xy(pos) for pos in folder_range),
                   ImageColor.getrgb('white'))


# X BUG: doesn't account for symbol length
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
        return Diagram(DiagramSymbol.objects.select_related('sourceline'))

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
    """
    render given project to database
    """
    symbols = SourceLine.objects.filter( # pylint: disable=no-member
        project=project
    ).order_by('path', 'line_number')

    diagram = Diagram()
    diagram.render(symbols, argname, depth)
    diagram.dbsave()


def draw(project):
    """
    draw rendered project into a grid/image
    """
    grid = ImageGrid.FromProject(project)

    diagram = Diagram.FromDB()

    # tags = sorted(set(dsym.sourceline.tags_json for dsym in diagram))

    diagram.draw(grid)
    # tag_num = 6
    # if tag_num is not None:
    #     try:
    #         selected_tag = tags[tag_num]
    #         print tag_num, selected_tag
    #         selected = [dsym for dsym in diagram
    #             if dsym.sourceline.tags_json == selected_tag]
    #         print [dsym.sourceline.name for dsym in selected]
    #         draw_box(grid, selected)
    #     except IndexError:
    #         pass

    grid.finalize()
    return grid


def draw_bbox(project):
    grid = ImageGrid.FromProject(project)

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
