# FIXME: needs work
# FIXME: handle HTTP Error 403: rate limit exceeded

import contextlib
import json
import sqlite3
import sys

import github_api as api

# 
# CREATE TABLE package_github (
#     package TEXT, api_repos TEXT);
# sql: update package_github 
# TODO: package unique key, Sqlite enforced
def main(dbpath):
    if not api.is_authorized():
        sys.exit("Unauthorized: set GITHUB_TOKEN and restart")

    query_already = 'select package from package_github'
    query_github = 'select package, source from alpine where source like "%github.com%"'
    sql_insert = "insert into package_github (package, api_repos) values (?, ?)"
    
    with contextlib.closing(sqlite3.connect(dbpath)) as conn:
        already = set(row[0] for row in conn.execute(query_already))

        for package, source in conn.execute(query_github).fetchall():
            if package in already:
                continue
            source_url = source.replace('$pkgname', package)
            repos = api.parse_github_url(source_url)
            info = api.get_github_repos(repos)
            # FIXME: insert missing repos info into database
            if not info:
                print(f"package={package}: repos not found")
                continue
            if 'message' in info:
                print(f"package={package}: {info['message']}")
                continue
            print(f"{package}:")
            print(f"\ttopics = {info['topics']}")
            print(f"\tdescription = {info['description']}")
            # FIXME: replace, don't insert
            with conn:
                conn.execute(sql_insert, (package, json.dumps(info)))

    with contextlib.closing(sqlite3.connect(dbpath)) as conn:
        count = list(conn.execute('select count(*) from package_github'))
    print(f"package_github: {count=}")

if __name__ == "__main__":
    main(sys.argv[1])
