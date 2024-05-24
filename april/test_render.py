# for all tests insert "conn" connection to sqlite database

import sqlite3
import pytest


# FIXME: scope?
@pytest.fixture(scope='module')
def conn():
    with sqlite3.connect('shotglass.db') as conn:
        yield conn

SQL_LIST_TAGS = '''
select name,line,end from tag
where end != 'UNKNOWN-end'
limit 3
'''
def test_sizes(conn):
    # select first three items from tag table
    assert 0, list(conn.execute(SQL_LIST_TAGS))
    assert 0, conn.size()