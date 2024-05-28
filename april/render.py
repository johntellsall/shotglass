# render.py

import sqlite3
from math import sqrt
from itertools import islice

# FIXME: define xy as list of two numbers
class Cursor:
    def __init__(self, width):
        self.xy = [0, 0]
        self.width = int(width)

    def skip(self, num):
        self.xy[0] += int(num)
        while self.xy[0] >= self.width:
            self.xy[0] -= self.width
            self.xy[1] += 1
       

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
        rows = conn.execute(sql)
        if 1:
            rows = islice(rows, 3)
        for row in rows:
            print(cursor.xy, end=' ')
            print('{size}\t{name} {path}'.format(**row))
            cursor.skip(row['size'])
    print(f"{cursor.xy} end")

def get_total_lines(conn):
    res = conn.execute(SQL_TOTAL)
    total = res.fetchone()['total']
    image_size = 1 + int(sqrt(total))
    return total,image_size
    