# render.py

import sqlite3
from math import sqrt
from itertools import islice
from PIL import Image, ImageColor, ImageDraw

# TODO: define xy as list of two numbers? Position?
class Cursor:
    def __init__(self, width):
        self.xy = [0, 0]
        self.width = int(width)

    def skip(self, num):
        """emit slices of consumed area
        Note: slice endpoints are *exclusive*
        Ex: 3-wide row, consume 2:
        - start at 0,0
        - move to 2,0 -- two spots consumed
        -> slice is ([0,0], [2,0]) -- end is exclusive
        -> draw [0,0] and [1,0] (two spots) don't draw [2,0]
        FIXME: slices are lists of tuples
        """
        slices = []
        old = tuple(self.xy)
        self.xy[0] += int(num)
        while self.xy[0] >= self.width:
            oldy = self.xy[1]
            # consume whole rest of row
            slices.append([old, (self.width - 1, oldy)])
            # move to left col of next row
            self.xy[0] -= self.width
            self.xy[1] += 1
            old = (0, self.xy[1])
        if old != self.xy:
            slices.append([old, tuple(self.xy)])
        return slices
       

def dbopen():
    conn = sqlite3.connect('shotglass.db')
    conn.row_factory = sqlite3.Row
    return conn

# TODO: strip small tags?

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
def render():
    sql = SQL_LIST_TAGS
    sql += ' and size >= 9' # limit to larger tags

    with dbopen() as conn:
        total, image_size = get_total_lines(conn)
        print(f'{total} LOC, {image_size=}')
        cursor = Cursor(image_size)
        tags = conn.execute(sql)

    if 0:
        tags = islice(tags, 3)
    image = Image.new('RGB', (image_size, image_size), color='gray')
    draw = ImageDraw.Draw(image)
    colors = list(get_colors(8))
    for tag in tags:
        size = tag['size']
        print(cursor.xy, end=' ')
        print('{size}\t{name} {path}'.format(**tag))
        slices = cursor.skip(size)
        for num,slice in enumerate(slices):
            color = colors[num % len(colors)]
            draw.line(slice, fill=color, width=1)

    print(f"{cursor.xy} end")
    image.show()
    image.save('out.png')

def get_total_lines(conn):
    res = conn.execute(SQL_TOTAL)
    total = res.fetchone()['total']
    image_size = 1 + int(sqrt(total))
    return total,image_size

def get_colors(count):
    for i in range(count):
        hue = i*360/count
        color = ImageColor.getrgb(f'hsl({hue}, 50%, 50%)')
        yield color