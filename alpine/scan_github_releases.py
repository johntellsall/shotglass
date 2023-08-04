# scan_github_releases.py
# Per Alpine package, scrape GitHub releases
# TODO: handle rate limits!
# TODO: use click to parse args
# INPUT:
# - "alpine" table with package names and source URLs
# OUTPUT
# - FIXME: "package_tags" table
#
import contextlib
import json
import re
import sqlite3
import sys

import github_api as api
from dbsetup import queryall


def save_releases(dbpath, package, releases):
    "save the list of releases to database -- whole JSON blob"
    if type(releases) is not list:
        raise TypeError("Only list allowed")
    sql_replace = "replace into github_releases_blob values (?, ?)"
    with contextlib.closing(sqlite3.connect(dbpath)) as conn:
        releases_json = json.dumps(releases)
        conn.execute(sql_replace, (package, releases_json))
        conn.commit()


def main(dbpath):
    if not api.is_authorized():
        sys.exit("Unauthorized: set GITHUB_TOKEN and restart")
     
    # TODO: note non-GitHub sources
    query_packages = """
        select package, source from alpine where
        source like '%github.com/%'
        limit 20
    """
    repos_pat = re.compile(r"https://github.com/(.+?/.+?)/")
    
    with contextlib.closing(sqlite3.connect(dbpath)) as conn:
        # list of desired packages
        packages_list = queryall(conn, query_packages)
    
        # get set of already-found release package names
        releases_list = queryall(conn, "select package from github_releases_blob")
    prev_packages = set((row[0] for row in releases_list))

    # parse source URLs to get GitHub repos
    repos_list = []
    for package, source in packages_list:
        if repos := repos_pat.search(source):
            # if '$' in source:
            #     print(f"skipping {package}: {source} -- $ unsupported")
            #     continue
            if package in prev_packages:
                print(f"skipping {package}: already done")
                continue
            repos_list.append((package, repos.group(1)))
        else:
            print(f"? {source}")

    for package,repos in repos_list:
        releases = api.get_github_releases(repos)
        # no releases? emit warning but save anyway
        if not len(releases):
            print(f"? {package}: no releases")

        # FIXME: handle errors e.g. {'message': 'Bad credentials'}
        save_releases(dbpath, package, releases)
        print(f"{package}: {len(releases)}")

if __name__ == "__main__":
    main(sys.argv[1])
