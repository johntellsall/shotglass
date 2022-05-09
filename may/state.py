# state.py

import sqlite3

SETUP_SQL = [
    "PRAGMA foreign_keys = ON",
    "create table release (label)",
    """create table file (
        id integer primary key, release, path, hash, size_bytes
        )""",
    """create table symbol (
        name, path, line_start, line_end, kind,
        file_id int,
        foreign key (file_id) references file (id)
    )""",
]


def get_db(temporary=True):
    path = ":memory:" if temporary else "main.db"
    con = sqlite3.connect(path)  # pylint: disable=no-member
    con.row_factory = sqlite3.Row
    setup(con)
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
