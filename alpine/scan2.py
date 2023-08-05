# scan2.py 
# scan/plot multiple releases for many packages
# FIXME: this is a placeholder

import contextlib
import json
import sys
from dbsetup import dbopen, queryall
import datetime

# parse datetime from this format "2015-01-01T21:15:10Z"
# TODO: simplify?
def parse_datetime(dt_str):
    return datetime.datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ")

def main(dbpath):
    query = "select package, releases_json from github_releases_blob"
    query += " where package='jq'"
    # query += " limit 10"

    with contextlib.closing(dbopen(dbpath)) as conn:
        package_releases = queryall(conn, query)

    for package, releases_json in package_releases:
        print(package)
        releases = json.loads(releases_json)
        if not releases:
            print('- (no releases)')
            continue
        for release in releases[:5]:
            print(f'- {release["name"]}')
            print(f'- {release["created_at"]}')
            created_at = parse_datetime(release["created_at"])
            print(f'- {created_at}')


if __name__ == "__main__":
    main(sys.argv[1])
