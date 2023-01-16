# list_versions.py
# List major versions of Alpine packages

import contextlib
import re
import sqlite3
from collections import defaultdict


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
    package_tags = defaultdict(list)
    with contextlib.closing(sqlite3.connect(dbpath)) as conn:
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
                # print(f"package={package}: {tag_value=} {err=}")
                continue
            package_tags[package].append(tag)

    def is_major(tag):
        return tag[1:] == (0, 0)

    for package, tags in package_tags.items():
        print(f"{package}: {len(tags)} tags/releases")
        print(f"  {tags[-1]} - latest")
        for tag in reversed(tags):  # most recent first
            if is_major(tag):
                major_min = tag[:2]
                print(f"  {major_min} - major")


if __name__ == "__main__":
    main(sys.argv[1])
