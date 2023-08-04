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
import subprocess
import sys
import time

import github_api as api
from dbsetup import query1, queryall


# def list_tags(repos):
#     """
#     List tags for remote Git repository
#     Note: uses network (github.com)
#     """
#     cmd = f"git ls-remote --tags {repos}"
#     result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
#     tag_pat = re.compile(r"refs/tags/(.+)")
#     matches = tag_pat.findall(result.stdout)
#     return matches


# def save_tags(dbpath, tags):
#     """
#     save the tags to database - one row per package-tag pair
#     INPUT:
#     - tags: dict of package names and list of tags
#     EXAMPLE:
#         {'abi-compliance-checker': ['1.98.7', '1.98.7^{}', '1.98.8'}}
#     OUTPUT:
#     - "package_tags" table, one row per package-tag pair:
#         abi-compliance-checker|1.98.7
#         abi-compliance-checker|1.98.7^{}
#         abi-compliance-checker|1.98.8
#     """
#     if type(tags) is not dict:
#         raise TypeError("Only dict allowed")
#     sql_insert = "insert into package_tags (package, tag) values (?, ?)"
#     with contextlib.closing(sqlite3.connect(dbpath)) as conn:
#         for package, tags in tags.items():
#             for tag in tags:
#                 assert type(tag) is str, "Only strings allowed" # FIXME:
#                 conn.execute(sql_insert, (package, tag))
#         conn.commit()


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
    """

    repos_list = ['jqlang/jq']
    # repos_pat = re.compile(r"(https://github.com/.+?/.+?/)")
    
    # releases_list = queryall(dbpath, "select * from github_releases_blob")
    # # grab package names from Alpine distro
    # # - also list currently-scraped packages
    # with contextlib.closing(sqlite3.connect(dbpath)) as conn:
    #     distro_packages = conn.execute(query_packages).fetchall()
    #     if not distro_packages:
    #         sys.exit("db.alpine: table has no packages")
    #     cursor = conn.execute("select distinct(package) from package_tags")
    #     prev_packages = set((row[0] for row in cursor.fetchall()))

    # per package, scrape the list of release tags
    # package_tags = {}
    # limit = None # 50
    # if limit:
    #     distro_packages = distro_packages[:limit]
    for repos in repos_list:
        releases = api.get_github_releases(repos)
        assert 0, releases
    #     if package in prev_packages:
    #         print(f"package={package}: done, skipping")
    #         continue

    #     time.sleep(1)  # avoid rate limits FIXME:

        # parse repos URL from package metadata XX
        # source_url = source_url.replace('$pkgname', package)  # package name
        # source_url = source_url.replace('$_pkgname', package)  # TODO: "base name"?
    #     try:
    #         repos = repos_pat.search(source_url).group(1)
    #     except AttributeError:
    #         print(f"package={package}: source={source_url}, repos={repos} not found")
    #         # NOTE: will be re-scanned next time FIXME:
    #         # info = {package: {"error": "repos not found",
    #         #    source_url: source_url }}
    #         # XX save_tags(dbpath, info)
    #         continue

    #     # get release tags from remote repos (via Git)
    #     tags = list_tags(repos)
    #     print(f"{package}: {len(tags)}")
    #     if not tags:
    #         print(f"package={package}: repos={repos}, tags not found")
    #         # info = {package: {"error": "tags not found"}}
    #         # XX FIXME: save_tags(dbpath, info)
    #         continue
    #     package_tags[package] = tags

    #     # save package's release tags to database
    #     save_tags(dbpath, package_tags)

    #     # get release info from GitHub API, save blob to database
    #     owner_repos = api.parse_github_url(source_url)
    #     releases_list = api.get_github_releases(owner_repos)
    #     # FIXME: handle errors e.g. {'message': 'Bad credentials'}
    #     save_releases(dbpath, package, releases_list)

    #     package_tags = {}


if __name__ == "__main__":
    main(sys.argv[1])
