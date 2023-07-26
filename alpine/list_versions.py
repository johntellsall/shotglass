# list_versions.py
# List major versions of Alpine packages

import contextlib
import re
import sqlite3
import sys
from collections import defaultdict

from dbsetup import query1


def parse_semver(raw_tag):
    """Parse a semver tag value and return a tuple of (major, minor, patch)."""
    tag = raw_tag.lstrip("v")
    try:
        major, minor, patch = tag.split(".", 2)
    except ValueError:
        patch = 0
        major, minor = tag.split(".", 1)
    return int(major), int(minor), int(patch)


def main(dbpath):
    tag_pat = re.compile(r"([0-9]+.+)\^")
    with contextlib.closing(sqlite3.connect(dbpath)) as conn:

        show_package_count(conn)

        package_tags = make_package_tags(tag_pat, conn)

    def is_major(tag):
        return tag[1:] == (0, 0)

    for package, tags in package_tags.items():
        print(f"{package}: {len(tags)} tags/releases")
        print(f"  {tags[-1]} - latest")
        for tag in reversed(tags):  # most recent first
            if is_major(tag):
                major_min = tag[:2]
                print(f"  {major_min} - major")


def make_package_tags(tag_pat, conn):
    package_tags = defaultdict(list)

    cursor = conn.execute(
            """
            select package, tag from package_tags
            where
            -- package='tmux'            and
            tag like '%{}'
            """
        )
    for package, raw_tag in cursor.fetchall():
        try:
            tag_value = tag_pat.search(raw_tag).group(1)
        except AttributeError:
            print(f"package={package}: {raw_tag=}, tag not recognized")
            continue
        try:
            tag = parse_semver(tag_value)
        except ValueError as err:
            print(f"package={package}: {tag_value=} {err=}")
            continue
        package_tags[package].append(tag)
    return package_tags


def show_package_count(conn):
    num_packages = query1(conn, table="package_tags")
    if num_packages < 1:
        sys.exit("No packages found in database -- run scan_releases.py")
    print(f"{num_packages[0]} packages")


if __name__ == "__main__":
    main(sys.argv[1])
