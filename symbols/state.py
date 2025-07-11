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
        id integer primary key, release,
        path, hash, num_lines, size_bytes,
        project_id,
        foreign key (project_id) references project (id)
        )""",
    """create table if not exists symbol (
        name, path, line_start, line_end, kind,
        -- file_id int, -- FIXME: reconcile this
        project_id int,
        -- foreign key (file_id) references file (id),
        foreign key (project_id) references project (id)
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
