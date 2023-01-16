
import contextlib
import sqlite3
import sys


CREATE_TABLES_SQL = [
    """
-- create table to set int fields
CREATE TABLE IF NOT EXISTS "alpine"(
  "package" TEXT,
  "num_files" INT,
  "build_num_lines" INT,
  "source" TEXT
);
""",
    """
create table if not exists package_tags (
    package TEXT, tag TEXT
)"""
]


def queryall(conn, sql):
    return conn.execute(sql).fetchall()


def main(dbpath):
    with contextlib.closing(sqlite3.connect(dbpath)) as conn:
        for create_table in CREATE_TABLES_SQL:
            conn.execute(create_table)
            conn.commit()


if __name__ == "__main__":
    main(sys.argv[1])
