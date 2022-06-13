"""
render.py
"""

import logging

import click

import hilbert
import state

logger = logging.getLogger(__name__)
get_xy = hilbert.int_to_Hilbert

SYMBOL_SQL = "select name,path,line_start,line_end from symbol"


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


# def zap_skeleton(project):
#     Skeleton.objects.filter(symbol__source_file__project=project).delete()


# # pylint: disable=no-member
# def do_render(symbols):
#     """
#     render skeleton, store in database
#     """
#     skel = make_skeleton(symbols)
#     Skeleton.objects.bulk_create(skel)

# TODO: make flexible
def is_interesting(sym):
    "skip dull symbols"
    if sym["path"].startswith("test/"):
        return False
    if "testing/" in sym["path"]:
        return False
    if sym["name"].startswith("_"):
        return False
    return True


def stats_project(project):
    db = state.get_db(setup=False)
    interesting = 0
    total_size = 0

    for symbol in filter(is_interesting, db.execute(SYMBOL_SQL)):
        interesting += 1
        sym_size = 1
        try:
            sym_size = symbol["line_end"] - symbol["line_start"]
        except TypeError:
            pass
        total_size += sym_size
        print(f'{symbol["name"]:25} {sym_size:3}\t{symbol["path"]}')

    total_symbols = state.query1(db, table="symbol")

    print("render")
    print(f"{project}:")
    print(f"- {total_symbols} symbols, {interesting} interesting")
    print(f"- {total_size} lines of interesting symbols")
    print(f"- {int(total_size/interesting)} average lines per interesting symbol")


# ::::::::::::::::::::::::: COMMANDS


@click.group()
def cli():
    pass


@cli.command()
@click.argument("projects", nargs=-1)
def stats(projects):
    for project in projects:
        stats_project(project)


if __name__ == "__main__":
    cli()
