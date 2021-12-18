# render.py
#

from shotlib import (
    get_db,
    select1,
    selectall,
)


import os

os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame as pg  # noqa: E402


def iter_color():
    hue = 0
    while True:
        color = pg.Color("white")
        color.hsva = (hue, 100, 100, 100)
        yield color
        hue += 15
        hue %= 360


def cmd_render(verbose=True):
    WIDTH, HEIGHT = [1000, 500]

    pg.display.init()
    screen = pg.display.set_mode(size=[WIDTH, HEIGHT])
    _, db = get_db()
    breakpoint()
    total = select1(db, "select sum(byte_count) from files")
    print(f"TOTAL: {total} bytes")

    def num_to_xy(num):
        y = int(num / WIDTH)
        x = num % WIDTH
        return x, y

    num = 0
    rows = db.execute("select path, byte_count from files order by 1")
    coords = []
    for row in rows:
        xy = num_to_xy(num)
        coords.append(xy)
        num += row[1]

    white = pg.Color("white")
    colors = iter_color()
    for i in range(len(coords) - 1):
        color = next(colors)
        xy1, xy2 = coords[i], coords[i + 1]
        width = xy2[0] - xy1[0]
        height = xy2[1] - xy1[1]
        if verbose:
            print(f"{i}\t{xy1}\t{xy2}\tw={width}\th={height}\tc={color}")
        rect = pg.Rect(xy1[0], xy1[1], width, height)
        rect.normalize()
        pg.draw.rect(screen, color, rect)
        if False:
            print(f"\t{rect}")
            rect.width = rect.height = 20
            pg.draw.rect(screen, white, rect)

    pg.image.save(screen, "main.png")
