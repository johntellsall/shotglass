# render.py

import sqlite3

# FIXME: define xy as list of two numbers
class Cursor:
    def __init__(self, width):
        self.xy = [0, 0]
        self.width = width

    def skip(self, num):
        self.xy[0] += num
        while self.xy[0] >= self.width:
            print(self.xy)
            self.xy[0] -= self.width
            self.xy[1] += 1
        print(f'-> {self.xy}')
       


def dbopen():
    return sqlite3.connect('shotglass.db')

# select first three items from tag table
SQL_LIST_TAGS = '''
select path,name,line,end from tag
where end != 'UNKNOWN-end'
limit 3
'''
def render():
    with dbopen() as conn:
        for (tagpath, name, start, end) in conn.execute(SQL_LIST_TAGS):
            print(f"{start}, {end} {name} {tagpath}")