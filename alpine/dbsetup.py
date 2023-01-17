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
create table package_tags (
    package TEXT, tag TEXT
);""",
    """
create table package_github (
    package TEXT, api_repos TEXT
);
""",
]


def queryall(conn, sql):
    return conn.execute(sql).fetchall()


def main(dbpath):
    with contextlib.closing(sqlite3.connect(dbpath)) as conn:
        for num, create_table in enumerate(CREATE_TABLES_SQL):
            print(num, create_table)
            with conn:
                conn.execute(create_table)


if __name__ == "__main__":
    main(sys.argv[1])
