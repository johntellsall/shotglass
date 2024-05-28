# for all tests insert "conn" connection to sqlite database

import sqlite3
import pytest
from render import Cursor

# FIXME: scope?
@pytest.fixture(scope='module')
def conn():
    with sqlite3.connect('shotglass.db') as conn:
        yield conn

SQL_LIST_TAGS = '''
select path,name,line,end from tag
where end != 'UNKNOWN-end'
limit 3
'''
# def test_sizes(conn):
#     # select first three items from tag table
#     assert 0, list(conn.execute(SQL_LIST_TAGS))

def test_cursor1():
    "move in same row"
    cursor = Cursor(3)
    assert cursor.xy == [0, 0]
    cursor.skip(2)
    assert cursor.xy == [2, 0]

def test_cursor2():
    "jump to next row"
    cursor = Cursor(3)
    cursor.skip(3)
    assert cursor.xy == [0, 1]

def test_cursor_slice1():
    "move in same row"
    slices = Cursor(3).skip(2)
    assert slices == [([0, 0], [2, 0])]

# def test_cursor_slice3():
#     "jump to next row: slice is same
#     slices = Cursor(3).skip(3)
#     assert slices == [([0, 0], [2, 0])]
   

# def test_cursor_slice2():
#     "move to next row"
#     # a 5-wide tag will consume one full row (width=3) and 2 of 2nd row
#     slices = Cursor(3).skip(5)
#     # 5-wide tag:
#     # - start at upper left (0,0)
#     # - move to upper right (2,0)
#     # - start at 2nd row left again (0,1)
#     # - move two steps to the right (2,1)
#     assert slices[0] == ([0, 0], [2, 0]) # first row: full
#     assert ([0, 1], [2, 1])
