# scan_lines.py
# FIXME: needs work
# Count number of lines for all files in a Git repos
# INPUT:
# - "alpine" table with package names and source URLs
# OUTPUT database, "package_files_lines" table
#
import contextlib
import re
import sqlite3
import subprocess
import sys
from pathlib import Path


def list_files_lines(repos):
    """
    List files for local checked-out Git repository
    Includes number of lines per file, and total.
    """
    # FIXME: handle paths with spaces
    # EX: cmd = "git ls-files -z | xargs -0 wc -l"
    cmd = "git ls-files | xargs wc -l"
    try:
        result = subprocess.run(
            cmd, capture_output=True, check=True, cwd=repos, shell=True, text=True
        )
    except subprocess.CalledProcessError as exc:
        print("??", repos, exc)
        return []
    count_path_pat = re.compile(r"^\s+(\d+) (.+)", re.MULTILINE)
    matches = count_path_pat.findall(result.stdout)
    return matches


def query1(conn, sql=None, count=None):
    if count:
        sql = f"select count(*) from {count}"
    cursor = conn.execute(sql)
    return cursor.fetchone()[0]


def queryall(conn, sql):
    return conn.execute(sql).fetchall()


def main(args):
    dbpath, repos_list = args[0], args[1:]

    # TODO: uses "repos" as package name
    sql_insert = "insert into package_files_lines values (?, ?, ?)"
    with contextlib.closing(sqlite3.connect(dbpath)) as conn:
        for repos in repos_list:
            print(f"repos={repos}")
            if not Path(repos).is_dir():
                print(f"?? repos={repos} must be a repos directory")
                continue

            files_lines = list_files_lines(repos)
            if not files_lines:
                continue
            repos_name = Path(repos).name
            for count, path in files_lines:
                conn.execute(sql_insert, (repos_name, path, count))
            # check that "wc -l" last line is "total"
            assert path == "total"
            conn.commit()
            num_files = len(files_lines)
            print(f"name={repos_name} {num_files=} total_lines={count}")

    num_packages_sql = """
    select count(*) from package_files_lines
    where path='total'
    """
    num_lines_sql = """
    select sum(num_lines) from package_files_lines
    where path='total'
    """
    with contextlib.closing(sqlite3.connect(dbpath)) as conn:
        num_packages = query1(conn, num_packages_sql)
        print(f"{num_packages=}")
        num_lines = query1(conn, num_lines_sql)
        print(f"{int(num_lines/1000):,} KLOC")

    # repos_pat = re.compile("(https://github.com/.+?/.+?/)")

    # # grab package names from Alpine distro
    # # - also list currently-scraped packages
    # with contextlib.closing(sqlite3.connect(dbpath)) as conn:
    #     distro_packages = conn.execute(query_packages).fetchall()
    #     if not distro_packages:
    #         sys.exit("db.alpline: table has no packages")
    #     cursor = conn.execute("select distinct(package) from package_tags")
    #     prev_packages = set((row[0] for row in cursor.fetchall()))

    # # per package, scrape the list of tags
    # package_tags = {}
    # for package, source in distro_packages:
    #     if package in prev_packages:
    #         print(f"package={package}: done, skipping")
    #         continue
    #     try:
    #         repos = repos_pat.search(source).group(1)
    #     except AttributeError:
    #         print(f"package={package}: source={source}, repos not found")
    #         continue
    #     tags = list_tags(repos)
    #     print(f"{package}: {len(tags)}")
    #     if not tags:
    #         # TODO: handle this case; store in db
    #         print(f"package={package}: tags not found")
    #         continue
    #     package_tags[package] = tags

    # # save the tags to database
    # sql_insert = "insert into package_tags values (?, ?)"
    # with contextlib.closing(sqlite3.connect(dbpath)) as conn:
    #     for package, tags in package_tags.items():
    #         for tag in tags:
    #             conn.execute(sql_insert, (package, tag))
    #         conn.commit()


if __name__ == "__main__":
    main(sys.argv[1:])
