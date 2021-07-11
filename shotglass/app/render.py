"""
app/render.py
"""
# XXXXX there are two! TODO resolve

import logging

from app import hilbert
from app.models import Skeleton


logger = logging.getLogger(__name__)


get_xy = hilbert.int_to_Hilbert


def calc_sym_position(symbols):
    """
    calculate position of each symbol
    """
    prev_path = None
    pos = 0
    for symbol in symbols:
        yield pos, symbol
        pos += 1
        if symbol.path != prev_path:
            if prev_path:
                pos += 2  # add black smudge
            prev_path = symbol.path
        pos += symbol.length - 1


def make_skeleton(symbols):
    """
    make skeleton, annotate X,Y position of each symbol
    """
    skeleton = calc_sym_position(symbols)
    for pos, symbol in skeleton:
        x, y = get_xy(pos)  # pylint: disable=invalid-name
        yield Skeleton(position=pos, x=x, y=y, symbol=symbol)


# # pylint: disable=no-member
# def render(symbols):
#     """
#     render skeleton, store in database
#     """
#     # Skeleton.objects.all.delete() # XX
#     skel = make_skeleton(symbols)
#     Skeleton.objects.bulk_create(skel)
