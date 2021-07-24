"""
app/management/commands/render.py
"""

import logging
import sys

from django.core.management.base import BaseCommand

from app import hilbert
from app.models import Skeleton, Symbol


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
        new_path = symbol.source_file.path
        if new_path != prev_path:
            if prev_path:
                print(f"{pos} {new_path}")
                pos += 5  # add black smudge TODO ??
            prev_path = new_path
        pos += symbol.length - 1


def make_skeleton(symbols):
    """
    make skeleton, annotate X,Y position of each symbol
    """
    skeleton = calc_sym_position(symbols)
    for num, (pos, symbol) in enumerate(skeleton):
        x, y = get_xy(pos)
        if num <= 5:
            print(f"position={pos}, x={x}, y={y}, {symbol=}")

        yield Skeleton(position=pos, x=x, y=y, symbol=symbol)


def zap_skeleton(project):
    Skeleton.objects.filter(symbol__source_file__project=project).delete()


# pylint: disable=no-member
def render(symbols):
    """
    render skeleton, store in database
    """
    skel = make_skeleton(symbols)
    Skeleton.objects.bulk_create(skel)


def render_project(project):
    proj_symbols = Symbol.objects.filter(source_file__project=project)

    num_symbols = proj_symbols.count()
    print("render")
    print(f"{project}: {num_symbols} symbols")

    if num_symbols < 1:
        sys.exit(f"{project}: no symbols")

    zap_skeleton(project)

    render(project, proj_symbols)

    count = Skeleton.objects.count()
    print(f"{project}: Skeleton.{count=}")


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("projects", nargs="*")

    def handle(self, *args, **options):
        projects = options["projects"]
        if projects == ["all"]:
            raise NotImplementedError("all: tbd")

        for project in projects:
            render_project(project)
