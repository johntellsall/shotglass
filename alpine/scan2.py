# scan2.py
# scan/plot multiple releases for many packages
# FIXME: add docs
# FIXME: rename to be consistent
# DATABASE:
# - github_releases_blob
# - github_releases


import contextlib
import datetime
import json
import sys

from dbsetup import dbopen, query1, queryall


# parse datetime from this format "2015-01-01T21:15:10Z"
# TODO: simplify?
def parse_datetime(dt_str):
    return datetime.datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ")


def setup(dbpath):
    "setup database"
    setup_list = [
        """delete from github_releases""",  # FIXME: <===
    ]
    with contextlib.closing(dbopen(dbpath, readonly=False)) as conn:
        for sql in setup_list:
            conn.execute(sql)
        conn.commit()


def add_releases(conn, releases):
    "add releases to database"
    sql_insert = "insert into github_releases values (?, ?, ?)"
    for release in releases:
        conn.execute(sql_insert, release)


def main(dbpath):
    setup(dbpath)

    query = "select package, releases_json from github_releases_blob"
    # query += " where package='jq'"
    # query += " limit 30"

    # grab cached GitHub Releases
    # - this is a list of GH Release details, including name and created_at
    with contextlib.closing(dbopen(dbpath)) as conn:
        package_releases = queryall(conn, query)

    # import all Releases parsed from a Package's JSON blob
    for package, releases_json in package_releases:
        print(package)
        orig_releases = json.loads(releases_json)
        if not orig_releases:
            print("- (no releases)")
            continue

        def format_release(release):
            created_at = parse_datetime(release["created_at"])
            return (package, release["name"], created_at)
        
        with contextlib.closing(dbopen(dbpath, readonly=False)) as conn:
            add_releases(conn, map(format_release, orig_releases))
            conn.commit()

    # validate import by showing summary
    with contextlib.closing(dbopen(dbpath)) as conn:
        sql = "select count(distinct(package)) from github_releases"
        num_packages = query1(conn, sql)
        print(f"{num_packages=}")

        num_releases = query1(conn, "select count(*) from github_releases")
        print(f"{num_releases=}")


if __name__ == "__main__":
    main(sys.argv[1])
