# scan_lines.py
# Count number of lines for all files in a Git repos
# INPUT:
# - "alpine" table with package names and source URLs
# OUTPUT database, "package_files_lines" table
#
import contextlib
from pathlib import Path
import re
import sqlite3
import subprocess
import sys


def list_files_lines(repos):
    """
    XX List tags for remote Git repository
    Note: uses network (github.com)
    """
    # FIXME: handle paths with spaces
    # EX: cmd = "git ls-files -z | xargs -0 wc -l"
    cmd = "git ls-files | xargs wc -l"
    result = subprocess.run(cmd, capture_output=True, check=True, cwd=repos, shell=True, text=True)
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

    sql_insert = "insert into package_files_lines values (?, ?, ?)"
    with contextlib.closing(sqlite3.connect(dbpath)) as conn:
        for repos in repos_list:
            assert Path(repos).is_dir(), f"repos={repos} must be a repos directory"
            print(f"repos={repos}")
            files_lines = list_files_lines(repos)
            print(f"files_lines={len(files_lines)}")

            repos_name = Path(repos).name
            for count, path in files_lines:
                pass # conn.execute(sql_insert, (repos_name, path, count))
            # conn.commit()
            print(f"- total {count}")

    # query_packages = """
    #     select package, source from alpine where
    #     source like '%github.com/%'
    # """

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
