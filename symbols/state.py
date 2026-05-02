# state.py
"database setup and functions"

import sqlite3

SETUP_SQL = [
    "PRAGMA foreign_keys = ON",
    # PROJECT: like "flask"
    # RELEASE: a specific version of a Project
    """create table if not exists project (
        id integer primary key, name
        )""",
    """create table if not exists release (
        id integer primary key,
        label, project_id,
        foreign key (project_id) references project (id)
        )""",
    # FILE: part of a Release
    # - simple stats
    """create table if not exists file (
        id integer primary key, 
        path, hash, num_lines, size_bytes,
        release_id,
        foreign key (release_id) references release (id)
        )""",
    # SYMBOL:
    # - also part of a Release
    # - no file_id; release+path is more convenient
    """create table if not exists symbol (
        name, path, line_start, line_end, kind,
        release_id int,
        foreign key (release_id) references release (id)
        )""",
]


def get_db(temporary=False):
    path = ":memory:" if temporary else "main.db"
    # FIXME:
    if 1:
        params = {} # default: manual commit
    else:
        params = {"isolation_level": None}  # autocommit
    con = sqlite3.connect(path, **params)  # pylint: disable=no-member
    con.row_factory = sqlite3.Row
    setup(con)
    return con


def query1(con, sql=None, table=None, args=None):
    assert sql or table
    if table:
        sql = f"select count(*) from {table}"
    res = list(con.execute(sql, args or []))
    return res[0][0]


def queryall(con, sql):
    return list(con.execute(sql))


def setup(con):
    for sql in SETUP_SQL:
        con.execute(sql)
