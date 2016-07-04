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
    if argname:
        def arg_iter():
            'iterate by "args", generally filenames'
            for symbol in symbols:
                arg = getattr(symbol, argname)
                if depth and arg and argname.endswith('_json'):
                    yield (symbol, json.loads(arg)[:depth])
                else:
                    yield (symbol, arg)
    else:
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


def make_dsymbols(symbols, argname, depth):
    """
    make skeleton, annotate X,Y position of each symbol
    """
    skeleton = make_skeleton(symbols, argname, depth)
    for pos, symbol, arg in skeleton:
        x,y = get_xy(pos)
        yield DiagramSymbol(position=pos, x=x, y=y, sourceline=symbol)


# pylint: disable=no-member
def render(symbols, argname, depth):
    """
    render skeleton, store in database
    """
    DiagramSymbol.objects.all.delete() # XX
    dsyms = make_dsymbols(symbols, argname, depth)
    DiagramSymbol.objects.bulk_create(dsyms)
