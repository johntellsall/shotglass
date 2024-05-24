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
    # breakpoint()
    assert cursor.xy == [0, 1]