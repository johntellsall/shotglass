import contextlib
import sqlite3
import dbsetup


def test_query1():
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        version = dbsetup.query1(conn, sql="select sqlite_version()")
        assert version.startswith('3.')