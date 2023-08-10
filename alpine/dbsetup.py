"""
dbsetup.py -- setup Sqlite database tables
"""
import contextlib
import sqlite3
import sys

CREATE_TABLES_SQL = [
    """
CREATE TABLE alpine (
  package TEXT PRIMARY KEY,
  num_files INT,
  build_num_lines INT,
  source TEXT
);
""",
    """
create table package_files_lines (
    package TEXT PRIMARY KEY, path TEXT, num_lines INT
)
""",
    """
create table package_tags (
    package TEXT PRIMARY KEY, tag TEXT
);""",
    """
create table github_releases_blob (
    package TEXT PRIMARY KEY, releases_json TEXT
);""",
  """
create table github_releases (
    package TEXT, -- not unique
    release_name TEXT,
    release_created_at TEXT -- datetime in ISO 8601
);"""
]


def queryall(conn, sql: str):
    return conn.execute(sql).fetchall()


def query1(conn, sql=None, table=None):
    assert sql or table
    if sql is None:
        sql = f"select count(*) from {table}"
    return conn.execute(sql).fetchone()[0]


def dbopen(path, readonly=True):
    if readonly:
        return sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    return sqlite3.connect(path)


def main(dbpath):
    with contextlib.closing(dbopen(dbpath, readonly=False)) as conn:
        for num, create_table in enumerate(CREATE_TABLES_SQL):
            print(num, create_table)
            with conn:
                conn.execute(create_table)


if __name__ == "__main__":
    main(sys.argv[1])
