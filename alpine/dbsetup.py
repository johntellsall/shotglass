import contextlib
import sqlite3
import sys

CREATE_TABLES_SQL = [
    """
-- create table to set int fields
CREATE TABLE "alpine"(
  "package" TEXT,
  "num_files" INT,
  "build_num_lines" INT,
  "source" TEXT
);
""",
"""
create table package_files_lines (
    package TEXT, path TEXT, num_lines INT
)
""",
    """
create table package_tags (
    package TEXT, tag TEXT
);""",
# list of releases from GitHub API
# https://docs.github.com/en/rest/releases/releases?apiVersion=2022-11-28
    """
create table github_releases_blob (
    package TEXT, releases_json TEXT
);""",
# FIXME: 
    """
create table package_releases_new (
    package TEXT, name TEXT, tag_name TEXT, created_at DATETIME
);""",
    """
create table package_github (
    package TEXT, api_repos TEXT
);
""",
]


def queryall(conn, sql: str):
    return conn.execute(sql).fetchall()


def query1(conn, sql=None, table=None):
    assert sql or table
    if sql is None:
        sql = f"select count(*) from {table}"
    return conn.execute(sql).fetchone()[0]


def main(dbpath):
    with contextlib.closing(sqlite3.connect(dbpath)) as conn:
        for num, create_table in enumerate(CREATE_TABLES_SQL):
            print(num, create_table)
            with conn:
                conn.execute(create_table)


if __name__ == "__main__":
    main(sys.argv[1])
