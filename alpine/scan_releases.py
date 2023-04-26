# scan_releases.py
# Per Alpine package, scrape Git tags (= package releases)
# INPUT:
# - "alpine" table with package names and source URLs
# OUTPUT
# - "package_tags" table
#
import contextlib
import re
import sqlite3
import subprocess
import sys


def list_tags(repos):
    """
    List tags for remote Git repository
    Note: uses network (github.com)
    """
    cmd = f"git ls-remote --tags {repos}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    tag_pat = re.compile(r"refs/tags/(.+)")
    matches = tag_pat.findall(result.stdout)
    return matches


def query1(conn, sql=None, count=None):
    if count:
        sql = f"select count(*) from {count}"
    cursor = conn.execute(sql)
    return cursor.fetchone()[0]


def queryall(conn, sql):
    return conn.execute(sql).fetchall()


def save_tags(dbpath, tags):
    "save the tags to database"
    sql_insert = "insert into package_tags values (?, ?)"
    with contextlib.closing(sqlite3.connect(dbpath)) as conn:
        for package, tags in tags.items():
            for tag in tags:
                assert type(tag) is str, "Only strings allowed" # FIXME:
                conn.execute(sql_insert, (package, tag))
        conn.commit()


def main(dbpath):
    # TODO: note non-GitHub sources
    query_packages = """
        select package, source from alpine where
        source like '%github.com/%'
    """

    repos_pat = re.compile("(https://github.com/.+?/.+?/)")

    # grab package names from Alpine distro
    # - also list currently-scraped packages
    with contextlib.closing(sqlite3.connect(dbpath)) as conn:
        distro_packages = conn.execute(query_packages).fetchall()
        if not distro_packages:
            sys.exit("db.alpine: table has no packages")
        cursor = conn.execute("select distinct(package) from package_tags")
        prev_packages = set((row[0] for row in cursor.fetchall()))

    # per package, scrape the list of release tags
    package_tags = {}
    for package, source in distro_packages:
        if package in prev_packages:
            print(f"package={package}: done, skipping")
            continue

        # parse repos URL from package metadata XX
        try:
            repos = repos_pat.search(source).group(1)
        except AttributeError:
            print(f"package={package}: source={source}, repos not found")
            info = {package: {"error": "repos not found",
                            source: source }}
            save_tags(dbpath, info)
            continue

        # get release tags from remote repos (via API)
        tags = list_tags(repos)
        print(f"{package}: {len(tags)}")
        if not tags:
            print(f"package={package}: tags not found")
            info = {package: {"error": "tags not found"}}
            save_tags(dbpath, info)
            continue
        package_tags[package] = tags

        # save package's release tags to database
        save_tags(dbpath, package_tags)
        package_tags = {}


if __name__ == "__main__":
    main(sys.argv[1])