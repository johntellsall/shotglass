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
import sqlite3
import sys

import github_api as api
from dbsetup import query1, queryall


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
     
    repos_list = [('jq', 'jqlang/jq')] # FIXME:
   
    for package,repos in repos_list:
        releases = api.get_github_releases(repos)

        # FIXME: handle errors e.g. {'message': 'Bad credentials'}
        save_releases(dbpath, package, releases)
        print(f"{package}: {len(releases)}")

if __name__ == "__main__":
    main(sys.argv[1])
