# app/render.py

import itertools
import json
import logging

from app import hilbert
from app.grid import ImageGrid
from app.models import DiagramSymbol, SourceLine
from app.utils import make_step_iter


logger = logging.getLogger(__name__)


def make_hilbert_iter():
    index_ = 0
    while True:
        yield tuple(hilbert.int_to_Hilbert(index_))
        index_ += 1


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
    if not argname:
        def arg_iter():
            return ((sym, None) for sym in symbols)

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


class Diagram(list):
    @classmethod
    # pylint: disable=no-member
    def FromDB(cls):
        return Diagram(DiagramSymbol.objects.select_related('sourceline'))

    def render(self, symbols, argname, depth, color_func):
        self[:] = []
        skeleton = make_skeleton(symbols, argname, depth)
        for pos, symbol, arg in skeleton:
            x,y = get_xy(pos)
            self.append(DiagramSymbol(
                color=color_func(symbol),
                position=pos, x=x, y=y, 
                sourceline=symbol))

    def draw(self, grid):
        """
        draw symbols onto grid
        """
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
    diagram.render(symbols, argname, depth,
        color_func=ThemeComplexity.calc_sym_color)
    diagram.dbsave()


