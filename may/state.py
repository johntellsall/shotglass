# state.py

import sqlite3


SETUP_SQL = [
    "create table release (label)",
    "create table file (release, path, hash, size_bytes)",
]


def get_db(temporary=True):
    path = ":memory:" if temporary else "main.db"
    con = sqlite3.connect(path)  # pylint: disable=no-member
    return con


def query1(con, sql=None, table=None):
    assert sql or table
    if table:
        sql = f"select count(*) from {table}"
    res = list(con.execute(sql))
    return res[0][0]


def setup(con):
    for sql in SETUP_SQL:
        con.execute(sql)
