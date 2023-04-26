import contextlib
import sqlite3
import sys


def query1(conn, sql=None, count=None):
    if count:
        sql = f"select count(*) from {count}"
    cursor = conn.execute(sql)
    return cursor.fetchone()[0]


def summarize_tags(dbpath):
    # validate package-tags count
    print("SUMMARY")
    with contextlib.closing(sqlite3.connect(dbpath)) as conn:
        package_tags_count = query1(conn, count="package_tags")
        package_count = query1(
            conn,
            sql="""
            select count(distinct(package)) from package_tags
            """,
        )

        distro_count = query1(conn, count="alpine")
        d_github_count = query1(
            conn,
            sql="""
            select count(*) from alpine where
            source like '%github.com/%'
            """,
        )

        print("alpine distro:")
        print(f" - {distro_count} packages")
        print(f" - {d_github_count} in GitHub")
        print("package_tags:")
        print(f" - {package_tags_count} rows")
        print(f" - {package_count} packages")


def main(dbpath):
    summarize_tags(dbpath)


if __name__ == "__main__":
    main(sys.argv[1])
