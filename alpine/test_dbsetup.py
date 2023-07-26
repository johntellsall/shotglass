import contextlib
import sqlite3
import dbsetup

def test_query1():
    # create in-memory Sqlite database
    conn = sqlite3.connect(":memory:")
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        assert 0, dbsetup.query1(conn, sql="select 1")