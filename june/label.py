"""
label.py --
"""

import itertools

import click
from palettable import colorbrewer
from PIL import Image, ImageDraw


BLACK = (0, 0, 0)
CMAP_OBJ = colorbrewer.qualitative.Set3_12
CMAP_COLORS = list(map(tuple, CMAP_OBJ.colors))

COL_WIDTH, COL_HEIGHT = 100, 2000
COL_GAP = 10


def serpentine_iter(width):
    y = 0
    while True:
        for x in range(width):
            yield x, y
        for x in range(width):
            yield width - x - 1, y + 1
        y += 2


def render_funcs(funcs, color_gen):
    width = COL_WIDTH
    height = COL_HEIGHT
    im = Image.new("RGB", (width, height))
    im_pixel = im.load()
    im_draw = ImageDraw.Draw(im)
    image_iter = serpentine_iter(width=width)
    first_ch = None
    new_labels = []
    for func in funcs:
        name = func.name
        new_label = False
        if name[0] != first_ch:
            new_label = True
            first_ch = name[0]
            print(name)
        if new_label:
            new_labels.append([func, next(image_iter)])
        color = color_gen()
        for _ in range(func.length):
            im_pixel[next(image_iter)] = color
    print(new_labels)
    for func, label_pos in new_labels:
        x, y = label_pos
        rect = [x - 1, y - 1, x + 2, y + 2]
        im_draw.rectangle(rect, fill="black")
    return im


def render_paths(funcs, color_gen):
    width = COL_WIDTH
    height = COL_HEIGHT
    im = Image.new("RGB", (width, height))
    im_pixel = im.load()
    im_draw = ImageDraw.Draw(im)
    image_iter = serpentine_iter(width=width)
    prev_path = None
    color = None
    for func in funcs:
        if func.path != prev_path:
            prev_path = func.path
            color = color_gen()
            x, y = next(image_iter)
            rect = [x - 1, y - 1, x + 2, y + 2]
            im_draw.rectangle(rect, fill="black")
        for _ in range(func.length):
            im_pixel[next(image_iter)] = color
    return im


@click.command()
@click.option("--output", default="z.png")
@click.option("--style", default="source")
@click.argument("paths", nargs=-1)
def label(output, style, paths):
    click.secho(f"Label: {paths}", fg="yellow")
    color_iter = itertools.cycle(CMAP_COLORS + list(reversed(CMAP_COLORS)))

    for project in paths:
        p = SourceLine.objects.filter(project=project)
        print(project)
        print("all:", p.count())
        funcs = p.exclude(path__startswith="tests/").exclude(
            path__startswith="examples/"
        )
        print("no tests:", funcs.count())

        if 0:
            funcs = funcs.order_by("name")
            img = render_funcs(funcs, color_iter.__next__)
        else:
            funcs = funcs.order_by("path")
            img = render_paths(funcs, color_iter.__next__)

        img.save("{}.png".format(project))
    # im = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), color="white")
    # render = render_source
    # if style == "blocks":
    #     render = render_blocks

    # render(image=im, paths=paths)
    # im.save(output)
    # print(f"{output}: image written")


if __name__ == "__main__":
    label()
