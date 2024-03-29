# state.py
"database setup and functions"

import sqlite3

SETUP_SQL = [
    "PRAGMA foreign_keys = ON",
    """create table if not exists project (
        id integer primary key, name
        )""",
    """create table if not exists release (
        label, project_id,
        foreign key (project_id) references project (id)
        )""",
    """create table if not exists file (
        id integer primary key, release, path, hash, size_bytes,
        project_id,
        foreign key (project_id) references project (id)
        )""",
    """create table if not exists symbol (
        name, path, line_start, line_end, kind,
        file_id int,
        project_id int,
        foreign key (file_id) references file (id),
        foreign key (project_id) references project (id)
        )""",
]


def get_db(temporary=False, setup=True):
    path = ":memory:" if temporary else "main.db"
    con = sqlite3.connect(path)  # pylint: disable=no-member
    # allow field access by name in addition to index
    con.row_factory = sqlite3.Row
    if setup:
        do_setup(con)
    return con


def query1(con, sql=None, table=None):
    assert sql or table
    if table:
        sql = f"select count(*) from {table}"
    res = list(con.execute(sql))
    return res[0][0]


def do_setup(con):
    for sql in SETUP_SQL:
        con.execute(sql)
