# render.py

import sqlite3
from math import sqrt
import colorsys
import subprocess

from PIL import Image, ImageColor, ImageDraw
from rectpack import newPacker

from cursor import Cursor


def dbopen():
    conn = sqlite3.connect("shotglass.db")
    conn.row_factory = sqlite3.Row
    return conn


# TODO: ditch order?
SQL_PATH_NUMLINES = """
select path, sum(end - line) as numlines
from tag
where end != 'UNKNOWN-end'
group by path
order by numlines desc
"""

# TODO: order?
SQL_LIST_TAGS = """
select path,name,line,end,
end - line AS size
from tag
where end != 'UNKNOWN-end'
-- and size > 50
-- and path like '%/sessions.py'
order by path, line
"""


def get_path_numlines(conn):
    sql = SQL_PATH_NUMLINES
    return conn.execute(sql)


def calc_image_size(num_lines):
    return 1 + int(sqrt(num_lines))


def get_colors(count):
    for i in range(count):
        hue = i * 360 / count
        color = ImageColor.getrgb(f"hsl({hue}, 50%, 50%)")
        yield color


def tweak_color(color):
    color_float = [c / 255 for c in color]
    hsl_color = colorsys.rgb_to_hls(*color_float)
    hue, _sat, _light = hsl_color
    color2_float = colorsys.hls_to_rgb(hue, 0.35, 0.35)
    color2 = tuple(int(c * 255) for c in color2_float)
    return color2


def draw_image_tags(image, tags, colors=None):
    cursor = Cursor(image.width)
    draw = ImageDraw.Draw(image)
    colors = colors or list(get_colors(8))
    color_num = 0
    # print(f'render_image_tags: {image.size=}')
    for tag in tags:
        size = tag["size"]
        # print(f'- {tag["name"]:20} {cursor.xy=}, {size=}')
        color = colors[color_num % len(colors)]
        color_num += 1
        # print(cursor.xy, end=' ')
        # print('{size}\t{name} {path}'.format(**tag))
        slices = cursor.skip(size)
        for slice in slices:
            draw.line(slice, fill=color, width=1)
    # print(f"- end render_image_tags: {cursor.xy} {image.size=}")


def make_packer(rectangles, image_size):
    bins = [(image_size, image_size)]
    packer = newPacker()
    for r in rectangles:
        packer.add_rect(*r)

    # Add the bins where the rectangles will be placed
    for b in bins:
        packer.add_bin(*b)
    packer.pack()
    return packer


def render_files():
    """show each file as a colored square

    Size proportional to the number of lines in the file. Folders ignored.

    NOTE: actually, number of lines in the defined symbols, e.g. functions and
    classes. Comments not counted.
    """

    with dbopen() as conn:
        path_numlines = list(get_path_numlines(conn))

    total_numlines = sum(info["numlines"] for info in path_numlines)
    image_size = calc_image_size(total_numlines)
    print(f"{total_numlines} LOC, {image_size=}")

    # add one rectangle for each file
    rectangles = []
    for info in path_numlines:
        box_size = calc_image_size(info["numlines"])
        rectangles.append((box_size, box_size, info))

    packer = make_packer(rectangles, image_size)
    assert len(packer) == 1

    image = Image.new("RGB", (image_size, image_size), color="gray")
    draw = ImageDraw.Draw(image)
    colors = list(get_colors(8))
    color_num = 0

    for rect in packer[0].rect_list():
        x, y, w, h, info = rect
        color = colors[color_num % len(colors)]
        color_num += 1
        draw.rectangle((x, y, x + w, y + h), fill=color)
    return image


def render_tags():
    """show each tag/symbol as a colored line within its file's box

    Size proportional to the number of lines in the tag.
    Folders ignored. XX files?
    """

    verbose = False

    # calc overall image size, also size of each file's box
    with dbopen() as conn:
        path_numlines = list(get_path_numlines(conn))

    total_numlines = sum(info["numlines"] for info in path_numlines)
    image_size = calc_image_size(total_numlines)
    print(f"{total_numlines} LOC, {image_size=}")

    # add one rectangle for each file
    rectangles = []
    for info in path_numlines:
        box_size = calc_image_size(info["numlines"])
        rectangles.append((box_size, box_size, info))

    packer = make_packer(rectangles, image_size)
    assert len(packer) == 1

    # get info for all tags, all files
    file_tags = {}
    with dbopen() as conn:
        for info in conn.execute(SQL_LIST_TAGS):
            path = info["path"]
            if path not in file_tags:
                file_tags[path] = []
            file_tags[path].append(info)

    # print(f'{len(file_tags)} files')

    # different color per file -- symbols will be variations of this color
    colors = list(get_colors(8))
    color_num = 0

    # create rectangle for each file
    file_rectangles = {}
    for rect in packer[0].rect_list():
        x, y, w, h, info = rect
        color = colors[color_num % len(colors)]
        color_num += 1
        file_rectangles[info["path"]] = (x, y, w, h, color)

    # FIXME: this is probably a bug / poor assumption
    print(f"files: {len(file_rectangles)} tags: {len(file_tags)}")

    # draw each tag in its file's box
    image = Image.new("RGB", (image_size, image_size), color="gray")
    file_bg = None
    if verbose:
        file_bg = 'pink'
    for path, tags in file_tags.items():
        try:
            x, y, w, h, color = file_rectangles[path]
        except KeyError:
            print(f"no rectangle for {path=}")
            continue

        # render file tags into a new image, paste into main (project) image
        file_image = Image.new("RGB", (w, h), color=file_bg)
        file_colors = [color, tweak_color(color)]
        draw_image_tags(file_image, tags, colors=file_colors)
        image.paste(file_image, (x, y))

    return image


def render(image_name=None, show=False, show_iterm=False, show_macos=False):
    # image = render_files()
    image = render_tags()
    if show:
        image.show()
    name = image_name or "project.png"
    image.save(name)
    print(f"render written to {name}")
    if show_iterm:
        subprocess.run(["imgcat", name])
    if show_macos:
        subprocess.run(["open", name])
