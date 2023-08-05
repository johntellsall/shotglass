# scan2.py 
# scan/plot multiple releases for many packages
# FIXME: this is a placeholder

import contextlib
import json
import sys
from dbsetup import dbopen, queryall


def main(dbpath):
    query = "select distinct(package), releases_json from github_releases_blob limit 3"
    with contextlib.closing(dbopen(dbpath)) as conn:
        package_releases = queryall(conn, query)

    for package, releases_json in package_releases:
        print(package)
        # releases = json.loads(releases_json)
        # for release in releases:
        #     print(release["name"])


if __name__ == "__main__":
    main(sys.argv[1])
