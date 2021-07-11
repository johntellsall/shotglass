"""
app/management/commands/render.py
"""

import logging

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
                print(f'{pos} {new_path}')
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


# pylint: disable=no-member
def render(symbols):
    """
    render skeleton, store in database
    """
    Skeleton.objects.all().delete()  # XX
    skel = make_skeleton(symbols)
    Skeleton.objects.bulk_create(skel)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("projects", nargs="*")

    def handle(self, *args, **options):
        projects = options["projects"]
        # if not projects:
        #     print(('PROJECTS: {} or "all"'.format(", ".join(all_projects))))
        #     return
        if projects == ["all"]:
            raise NotImplementedError("all: tbd")
            # projects = all_projects

        for project in projects:
            proj_symbols = Symbol.objects.filter(source_file__project=project)
            num_symbols = proj_symbols.count()
            print("render")
            print(f"{args=}")
            print(f"{options=}")
            print(f"{project}: {num_symbols} symbols")
            render(proj_symbols)

            count = Skeleton.objects.count()
            print(f"Skeleton: {count=}")
