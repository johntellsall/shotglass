# render.py
#

from shotlib import (
    get_db2,
    # select1,
    # get_project_id,
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


# TODO: do proper SQL quote
def get_project_id(db, name):
    assert db and name
    breakpoint()
    proj_id = select1(db, f"select id from projects where name = '{name}'")
    if not proj_id:
        raise KeyError(f"{name}: project not found")
    assert proj_id
    return proj_id


def select1(db, sql):
    curs = db.execute(sql)
    row = curs.fetchone()
    return row[0] if row else None
    # if row:
    #     return row[0]
    # raise ValueError("no value returned")


def cmd_render(project, verbose=True):
    WIDTH, HEIGHT = [1000, 500]

    pg.display.init()
    screen = pg.display.set_mode(size=[WIDTH, HEIGHT])
    db = get_db2()
    proj_id = get_project_id(db, project)
    assert 0, proj_id
    total = select1(db, "select sum(byte_count) from files")
    print(f"TOTAL: {total} bytes")
    return

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
