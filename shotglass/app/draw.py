# app/draw.py

import colorsys
import itertools
import logging
from pathlib import Path

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
    hsl = hue / 99.0, lightness / 99.0, saturation / 99.0
    r, g, b = colorsys.hls_to_rgb(*hsl)
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


# TODO provide "next symbol" vs "next file" vs "next directory"
# Observer pattern?


class ThemeZebra(Theme):
    """
    alternate between dark blue and white; by file
    """

    def __init__(self):
        self.color_iter = itertools.cycle(["#66c", "#fff"])
        self.prev_group = None
        self.color = None

    def calc_sym_color(self, skel):
        # if skel.symbol.source_file == self.prev_group:
        #     return self.color
        # self.prev_group = skel.symbol.source_file
        value = Path(skel.symbol.source_file.path).parent  # directory
        if value == self.prev_group:
            return self.color
        print(f"VALUE: {value}")
        self.prev_group = value
        self.color = next(self.color_iter)
        return self.color


def get_skel_directory(skel):
    return Path(skel.symbol.source_file.path).parent


def is_diff_directory(skel):
    prev_value = None
    value = Path(skel.symbol.source_file.path).parent
    if value == prev_value:
        return False
    prev_value = value
    return True


class ThemeRainbow(Theme):
    """
    draw symbols in color with different saturation
    """

    def __init__(self):
        self.hue_iter = make_step_iter(50, 360)
        self.saturation_iter = itertools.cycle([30, 60, 80])
        self.lightness_iter = itertools.cycle([40, 60])
        self.hue_sat_lightness = 0, 0, 40

    def calc_sym_color(self, symbol):
        # prev_arg = None

        # for symbol, arg in skeleton:
        # change color with new arg (file)
        # if prev_arg != arg:
        #     hue = hue_iter.next()
        #     prev_arg = arg
        #     lightness = lightness_iter.next() # X?
        # alternate symbols: different saturation
        hue, _, lightness = self.hue_sat_lightness
        saturation = next(self.saturation_iter)
        return color_hsl_hex(hue, saturation, lightness)


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
    """
    draw single symbol into grid (image)
    """
    length = skel.symbol.length
    if length < 1:
        return
    print(f"{skel=}")
    # draw white "grain of rice" at start of symbol
    pos = skel.position
    grid.moveto(get_xy(pos))
    grid.drawto(get_xy(pos + 1), "#fff")
    for offset in range(length):
        grid.drawto(get_xy(pos + offset + 1), color)


# X BUG: doesn't account for symbol length
def draw_box(grid, dsymbols, outline="white", fill=None):
    """
    draw box containing all given symbols
    """
    try:
        upleft_x = min(dsym.x for dsym in dsymbols)
        upleft_y = min(dsym.y for dsym in dsymbols)
        downright_x = max(dsym.x for dsym in dsymbols)
        downright_y = max(dsym.y for dsym in dsymbols)
    except ValueError:
        logger.warning("empty box: no symbols")
        return
    # 2? XX TODO
    grid.im_draw.rectangle(
        [upleft_x * 2, upleft_y * 2, downright_x * 2, downright_y * 2],
        fill=fill,
        outline=outline,
    )


class DrawStyle(object):
    """
    draw rendered project onto a grid (image)
    """

    # draw_diagram = NotImplementedError

    def draw(self, project, theme=None):
        grid = ImageGrid.FromProject(project)
        mytheme = theme or Theme()
        color_cb = mytheme.calc_sym_color
        skeletons = models.Skeleton.objects.filter(
            symbol__source_file__project=project
        )  # noqa: E501
        count = skeletons.count()
        print(f"{project} skeletons: {count}")
        skeletons = skeletons.order_by(
            "symbol__source_file__path", "symbol__source_file__name"
        )

        for skeleton in skeletons:
            color = color_cb(skeleton)
            draw_symbol(grid, skel=skeleton, color=color)
        grid.finalize()
        return grid


class SimpleDraw(DrawStyle):
    """
    draw a pixel or several for each symbol
    """

    # def draw_diagram(self, grid, diagram):
    #     diagram.draw(grid)


# class BoundingBoxDraw(DrawStyle):
#     """
#     draw bounding box around each source file
#     """

#     def draw_diagram(self, grid, diagram):
#         BLAM
#         for path in set(dsym.sourceline.path for dsym in diagram):
#             syms = [dsym for dsym in diagram if dsym.sourceline.path == path]
#             draw_box(grid, syms, fill=syms[0].color)


# DRAW_STYLES = {"boundingbox": BoundingBoxDraw, "simple": SimpleDraw}
DRAW_STYLES = {"simple": SimpleDraw}
