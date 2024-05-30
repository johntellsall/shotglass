# render.py

import sqlite3
from math import sqrt
from itertools import islice
from PIL import Image, ImageColor, ImageDraw
from cursor import Cursor

def dbopen():
    conn = sqlite3.connect('shotglass.db')
    conn.row_factory = sqlite3.Row
    return conn

SQL_TOTAL = '''
select sum(end - line) as total
from tag
where end != 'UNKNOWN-end'
'''

SQL_LIST_TAGS = '''
select path,name,line,end,
end - line AS size
from tag
where end != 'UNKNOWN-end'
'''

def get_total_lines(conn, suffix_sql=None):
    sql = SQL_TOTAL
    if suffix_sql:
        sql += ' and {suffix_sql}'
    res = conn.execute(sql)
    total = res.fetchone()['total']
    image_size = 1 + int(sqrt(total))
    return total,image_size

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

def render():
    sql = SQL_LIST_TAGS
    if 0:
        sql += ' and size >= 9' # limit to larger tags

    with dbopen() as conn:
        total, image_size = get_total_lines(conn)
        print(f'{total} LOC, {image_size=}')
        tags = conn.execute(sql)

    if 0:
        tags = islice(tags, 3)

    image = Image.new('RGB', (image_size, image_size), color='gray')
    render_tags(image, tags)

    image.show()
    image.save('out.png')
