# for all tests insert "conn" connection to sqlite database

import sqlite3

import pytest

import render


# FIXME: scope?
@pytest.fixture(scope="module")
def conn():
    with sqlite3.connect("shotglass.db") as conn:
        yield conn


SQL_LIST_TAGS = """
select path,name,line,end from tag
where end != 'UNKNOWN-end'
limit 3
"""
# def test_sizes(conn):
#     # select first three items from tag table
#     assert 0, list(conn.execute(SQL_LIST_TAGS))

def test_tweak_red():
    color = (255, 0, 0)
    (r,g,b) = render.tweak_color(color)
    assert r > g and r > b
    assert (r,g,b) == (120, 58, 58)

def test_tweak_green():
    color = (0, 255, 0)
    (r,g,b) = render.tweak_color(color)
    assert g > r and g > b
    assert (r,g,b) == (58, 120, 58)
