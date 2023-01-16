
import contextlib
import sqlite3
import sys


def queryall(conn, sql):
    return conn.execute(sql).fetchall()


def main(dbpath):
    with contextlib.closing(sqlite3.connect(dbpath)) as conn:
        conn.execute(
            """
            create table if not exists package_tags (
            package TEXT, tag TEXT
            )"""
        )
        conn.commit()
        print("tables created: package_tags")
        print(queryall(conn, "select count(*) from package_tags"))

if __name__ == "__main__":
    main(sys.argv[1])
