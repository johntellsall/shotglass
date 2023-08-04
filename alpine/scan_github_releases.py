# scan_github_releases.py
# Per Alpine package, scrape GitHub releases
# TODO: use click to parse args
# INPUT:
# - "alpine" table with package names and source URLs
# OUTPUT
# - FIXME: "package_tags" table
#
import contextlib
import json
import re
import sys

import github_api as api
from dbsetup import dbopen, queryall


def query_github_repos(conn):
    """
    get package names and GitHub repos from database
    """
    query_packages = """
        select package, source from alpine where
        source like '%github.com/%'
        limit 40
    """
    return queryall(conn, query_packages)


def query_package_names(conn):
    releases_list = queryall(conn, "select distinct(package) from github_releases_blob")
    return set((row[0] for row in releases_list))


def save_releases(dbpath, package, releases):
    "save the list of releases to database -- whole JSON blob"
    if not isinstance(releases, list):
        raise TypeError("Only list allowed")
    sql_replace = "replace into github_releases_blob values (?, ?)"
    with contextlib.closing(dbopen(dbpath, readonly=False)) as conn:
        releases_json = json.dumps(releases)
        conn.execute(sql_replace, (package, releases_json))
        conn.commit()


def main(dbpath):
    if not api.is_authorized():
        sys.exit("Unauthorized: set GITHUB_TOKEN and restart")

    # TODO: note non-GitHub sources

    with contextlib.closing(dbopen(dbpath)) as conn:
        # get list of desired packages
        packages_list = query_github_repos(conn)

        # get set of already-found release package names
        prev_packages = query_package_names(conn)

    # parse source URLs to get GitHub repos
    repos_list = parse_github_repos(packages_list, prev_packages)

    for package, repos in repos_list:
        releases = api.get_github_releases(repos)
        # no releases? emit warning but save anyway
        if not releases:
            print(f"? {package}: no releases")

        # error? show it and continue
        # TODO: save "no releases" to database?
        if isinstance(releases, dict):
            print(f"! {package}: {releases}")
            continue
        save_releases(dbpath, package, releases)
        print(f"{package}: {len(releases)}")
    print("DONE")


def parse_github_repos(packages_list, prev_packages):
    """
    format list of GitHub repos where Releases not already fetched
    """
    repos_pat = re.compile(r"https://github.com/(.+?/.+?)/")
    repos_list = []
    for package, source in packages_list:
        if repos := repos_pat.search(source):
            if package in prev_packages:
                print(f"skipping {package}: already done")
                continue
            repos_list.append((package, repos.group(1)))
        else:
            print(f"? {source}")
    return repos_list


if __name__ == "__main__":
    main(sys.argv[1])
