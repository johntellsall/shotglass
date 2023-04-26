# FIXME: needs work!
# FIXME: handle HTTP Error 403: rate limit exceeded

import contextlib
import json
import pprint
import re
import sqlite3
import sys

import github_api as api


def demo():
    data = api.get_github_repos("matplotlib/matplotlib")
    pprint.pprint(data)

# 
# CREATE TABLE package_github (
#     package TEXT, api_repos TEXT);
# sql: update package_github 
# TODO: package unique key, Sqlite enforced
def main(dbpath):
    query_already = 'select package from package_github'
    query_github = 'select package, source from alpine where source like "%github.com%"'
    sql_insert = "insert into package_github (package, api_repos) values (?, ?)"
    
    with contextlib.closing(sqlite3.connect(dbpath)) as conn:
        already = [row[0] for row in conn.execute(query_already)]

        for package, source in conn.execute(query_github).fetchall():
            if package in already:
                continue
            source_url = source.replace('$pkgname', package)
            gh_repos = get_github_repos(source_url)
            if not gh_repos:
                print(f"package={package}: repos not found")
                continue
            print(f"{package}: {gh_repos['topics']}")
            with conn:
                conn.execute(sql_insert, (package, json.dumps(gh_repos)))

    with contextlib.closing(sqlite3.connect(dbpath)) as conn:
        count = list(conn.execute('select count(*) from package_github'))
    print(f"package_github: {count=}")

if __name__ == "__main__":
    main(sys.argv[1])
