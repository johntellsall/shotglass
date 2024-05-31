# render.py

import sqlite3
from math import sqrt
from itertools import islice
from PIL import Image, ImageColor, ImageDraw
from cursor import Cursor
from rectpack import newPacker

def dbopen():
    conn = sqlite3.connect('shotglass.db')
    conn.row_factory = sqlite3.Row
    return conn

SQL_PATH_NUMLINES = '''
select path, sum(end - line) as numlines
from tag
where end != 'UNKNOWN-end'
group by path
order by numlines desc
'''
# limit 10

SQL_LIST_TAGS = '''
select path,name,line,end,
end - line AS size
from tag
where end != 'UNKNOWN-end'
'''

def get_path_numlines(conn):
    sql = SQL_PATH_NUMLINES
    return conn.execute(sql)

def calc_image_size(num_lines):
    return 1 + int(sqrt(num_lines))

def get_colors(count):
    for i in range(count):
        hue = i*360/count
        color = ImageColor.getrgb(f'hsl({hue}, 50%, 50%)')
        yield color

def render_tags(image, tags):
    cursor = Cursor(image.width)
    draw = ImageDraw.Draw(image)
    colors = list(get_colors(8))
    color_num = 0
    for tag in tags:
        size = tag['size']
        print(cursor.xy, end=' ')
        print('{size}\t{name} {path}'.format(**tag))
        slices = cursor.skip(size)
        for slice in slices:
            color = colors[color_num % len(colors)]
            color_num += 1
            draw.line(slice, fill=color, width=1)


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

def render_project():
    """show each file as a colored square
    Size proportional to the number of lines in the file.
    NOTE: actually, number of lines in the defined symbols, e.g. functions and classes.
    """

    with dbopen() as conn:
        path_numlines = list(get_path_numlines(conn))

    total_numlines = sum(info['numlines'] for info in path_numlines)
    image_size = calc_image_size(total_numlines)
    print(f'{total_numlines} LOC, {image_size=}')

    # add one rectangle for each file
    rectangles = []
    for info in path_numlines:
        box_size = calc_image_size(info['numlines'])
        rectangles.append((box_size, box_size, info))

    packer = make_packer(rectangles, image_size)
    assert len(packer) == 1

    image = Image.new('RGB', (image_size, image_size), color='gray')
    draw = ImageDraw.Draw(image)
    colors = list(get_colors(8))
    color_num = 0

    for rect in packer[0].rect_list():
        x, y, w, h, info = rect
        color = colors[color_num % len(colors)]
        print(f'{x=}, {y=}, {w=}, {h=} \t {color=} \t {info["path"]}')
        color_num += 1
        draw.rectangle((x, y, x+w, y+h), fill=color)
    # image.show()
    return image
   

def render(image_name=None):
    image = render_project()
    name = 'project.png'
    if image_name:
        name = f'{image_name}.png'
    image.save(name)
    print(f'render written to {name}')
