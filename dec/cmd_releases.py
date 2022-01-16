# cmd_releases.py
# deprecated?

# import re
from datetime import datetime
from pathlib import Path

import git

from shotlib import (
    is_interesting_source,
)


def format_tstamp(ts):
    return datetime.fromtimestamp(ts).strftime("%c")


def print_release(tagref):
    summary = tagref.commit.summary
    tag_tree = tagref.commit.tree
    com_date = tagref.commit.committed_date
    com_datestr = format_tstamp(com_date)
    total_files = len(list(tag_tree.traverse()))
    com_count = sum(1 for _ in tag_tree.traverse())
    com_size = sum(c.size for c in tag_tree.traverse())
    file_list = [x.path for x in tag_tree.traverse()]
    source_list = [path for path in file_list if is_interesting_source(path)]
    print(f"{tagref.name} files={len(file_list)} source={len(source_list)}")
    print(f"\t{com_datestr}")
    print(f"\t{com_count} commits, {com_size} size")
    print(f"\t{summary}")
    print(f"\t{total_files} total files")


def cmd_releases(project_path):
    project_dir = Path(project_path)
    print(project_dir)
    repo = git.Repo(project_dir)

    # def is_interesting_release(tag):
    #     return re.match(r"^[0-9.]+$", tag.name) is not None

    tags = repo.tags

    # TODO: sort semver
    for tagref in list(repo.tags):
        # cool = is_interesting_release(tagref)
        # if not cool:
        #     print("-", end=" ")
        print_release(tagref)

    print()
