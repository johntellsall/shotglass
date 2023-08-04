# scan_packages.py -- find package description and topics
# Note: GitHub only.
# FIXME: needs work
# FIXME: handle HTTP Error 403: rate limit exceeded
#
# Updates package_github table. Example:
# package="jq", api_repos={
#   "id": 5101141,
#   "node_id": "MDEwOlJlcG9zaXRvcnk1MTAxMTQx",
#   "name": "jq",
#   "full_name": "jqlang/jq",
#   "owner": {...}
#   "description": "Command-line JSON processor",
#   "git_tags_url": "https://api.github.com/repos/jqlang/jq/git/tags{/sha}",
#   "created_at": "2012-07-18T19:57:25Z",
#   "updated_at": "2023-07-26T19:22:13Z",
#   "pushed_at": "2023-07-26T20:40:02Z",
#   "git_url": "git://github.com/jqlang/jq.git",
#   "homepage": "https://jqlang.github.io/jq/",
# }

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

    query_already = "select package from package_github"
    query_github = 'select package, source from alpine where source like "%github.com%"'
    sql_insert = "insert into package_github (package, api_repos) values (?, ?)"

    with contextlib.closing(sqlite3.connect(dbpath)) as conn:
        already = set(row[0] for row in conn.execute(query_already))

        for package, source in conn.execute(query_github).fetchall():
            if package in already:
                continue
            source_url = source.replace("$pkgname", package)
            repos = api.parse_github_url(source_url)
            info = api.get_github_repos(repos)
            # FIXME: insert missing repos info into database
            if not info:
                print(f"package={package}: repos not found")
                continue
            if "message" in info:
                print(f"package={package}: {info['message']}")
                continue
            print(f"{package}:")
            print(f"\ttopics = {info['topics']}")
            print(f"\tdescription = {info['description']}")
            # FIXME: replace, don't insert
            with conn:
                conn.execute(sql_insert, (package, json.dumps(info)))

    with contextlib.closing(sqlite3.connect(dbpath)) as conn:
        count = list(conn.execute("select count(*) from package_github"))
    print(f"package_github: {count=}")


if __name__ == "__main__":
    main(sys.argv[1])
