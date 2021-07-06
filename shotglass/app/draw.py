# app/draw.py

import colorsys
import itertools
import logging

from palettable import colorbrewer
from radon.complexity import cc_rank

from app import models
from app.grid import ImageGrid
from app.hilbert import int_to_Hilbert as get_xy
from app.utils import make_step_iter


COLOR_CC_UNKNOWN = "gray"

logger = logging.getLogger(__name__)


# X RGB values are off by one
def color_hsl_hex(hue, saturation, lightness):
    r, g, b = colorsys.hls_to_rgb(hue / 99.0, lightness / 99.0, saturation / 99.0)
    return "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))


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
            color = next(color_iter)
            prev_arg = arg
        yield pos, symbol, arg, color


# X: speedup w/ queryset.select_related('progpmccabe')
class Theme(object):
    def calc_sym_color(self, symbol):
        return "gray"


class ThemeRainbow(Theme):
    def __init__(self):
        self.hue_iter = make_step_iter(50, 360)
        self.saturation_iter = itertools.cycle([30, 60, 80])
        self.highlight_iter = itertools.cycle([40, 60])
        self.hue_sat_highlight = 0, 0, 40

    def calc_sym_color(self, symbol):
        # prev_arg = None

        # for symbol, arg in skeleton:
        # change color with new arg (file)
        # if prev_arg != arg:
        #     hue = hue_iter.next()
        #     prev_arg = arg
        #     highlight = highlight_iter.next() # X?
        # alternate symbols: different saturation
        hue, _, highlight = self.hue_sat_highlight
        saturation = next(self.saturation_iter)
        return color_hsl_hex(hue, saturation, highlight)


class ThemeComplexity(Theme):
    """
    give symbol a color based on code complexity
    Red=high complexity, blue=low.
    """

    COLOR_CC_UNKNOWN = "gray"

    def __init__(self):
        # pylint: disable=no-member
        colors = colorbrewer.diverging.RdBu_5_r.hex_colors
        self.colormap = dict(list(zip("ABCDE", colors)))
        self.colormap["F"] = self.colormap["E"]

    def calc_sym_color(self, symbol):
        def get_complexity(sym):
            try:
                return sym.progpmccabe.mccabe
            except AttributeError:
                try:
                    return sym.progradon.complexity
                except AttributeError:
                    pass
            return None

        cc_value = get_complexity(symbol)
        try:
            return self.colormap[cc_rank(cc_value)]
        except (KeyError, TypeError):
            return self.COLOR_CC_UNKNOWN


def draw_symbol(grid, skel, color):
    length = skel.sourceline.length
    if length < 1:
        return
    # draw white "grain of rice" at start of symbol
    pos = skel.position
    grid.moveto(get_xy(pos))
    grid.drawto(get_xy(pos + 1), "#fff")
    for offset in range(length):
        grid.drawto(get_xy(pos + offset + 1), color)


# X BUG: doesn't account for symbol length
def draw_box(grid, dsymbols, outline="white", fill=None):
    try:
        upleft_x = min(dsym.x for dsym in dsymbols)
        upleft_y = min(dsym.y for dsym in dsymbols)
        downright_x = max(dsym.x for dsym in dsymbols)
        downright_y = max(dsym.y for dsym in dsymbols)
    except ValueError:
        logger.warning("empty box: no symbols")
        return
    # 2? XX
    grid.im_draw.rectangle(
        [upleft_x * 2, upleft_y * 2, downright_x * 2, downright_y * 2],
        fill=fill,
        outline=outline,
    )


class DrawStyle(object):
    """
    draw rendered project onto a grid (image)
    """

    draw_diagram = NotImplementedError

    def draw(self, project, theme=None):
        grid = ImageGrid.FromProject(project)
        mytheme = theme or Theme()
        color_cb = mytheme.calc_sym_color
        skeletons = models.Skeleton.objects.filter(
            sourceline__project=project
        ).order_by("sourceline__path", "sourceline__name")

        for skeleton in skeletons:
            color = color_cb(skeleton)
            draw_symbol(grid, skel=skeleton, color=color)
        grid.finalize()
        return grid


class SimpleDraw(DrawStyle):
    def draw_diagram(self, grid, diagram):
        diagram.draw(grid)


class BoundingBoxDraw(DrawStyle):
    def draw_diagram(self, grid, diagram):
        for path in set(dsym.sourceline.path for dsym in diagram):
            syms = [dsym for dsym in diagram if dsym.sourceline.path == path]
            draw_box(grid, syms, fill=syms[0].color)


DRAW_STYLES = {"boundingbox": BoundingBoxDraw, "simple": SimpleDraw}
