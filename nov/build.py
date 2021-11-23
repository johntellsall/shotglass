"""
USAGE

shotglass.py <command> <project path>
"""

import logging
import re
import sys
from datetime import datetime
from pathlib import Path

import git

from cmd_index import cmd_index  # pylint: disable=unused-import
from shotlib import (
    get_db,
    get_project,
    make_file_info,
    select1,
    selectall,
    is_interesting_source,
)

# Universal Ctags
CTAGS_ARGS = "ctags --output-format=json --fields=*-P -o -".split()

logging.basicConfig(format="%(asctime)-15s %(message)s", level=logging.INFO)


def format_summary(tags):
    return {"num_tags": len(tags)}


def print_project(project_dir, source_paths):
    p_name = project_dir.name
    num_source = len(source_paths)
    print(f"PROJECT:{p_name} {num_source} source files")


def get_usage():
    cmd_list = [name for name in globals() if name.startswith("cmd_")]
    usage = [__doc__, f"Commands: {cmd_list}"]
    return "\n".join(usage)


def format_tstamp(ts):
    return datetime.fromtimestamp(ts).strftime("%c")


def format_lines(objs):
    return "\n".join(map(str, objs))


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


def cmd_info(project_path):  # pylint: disable=unused-argument
    _, db = get_db()

    num_files = select1(db, "select count(*) from files")
    print(f"NUM FILES: {num_files}")
    file_info = selectall(db, "select * from files limit 3")
    print(f"FILES: {format_lines(file_info)}")

    num_symbols = select1(db, "select count(*) from symbols")
    print(f"NUM SYMBOLS: {num_symbols}")
    sym_info = selectall(db, "select * from symbols limit 3")
    print(f"SYMBOLS: {format_lines(sym_info)}")

    size = selectall(
        db,
        """
    select *, end_line-start_line as size from symbols
    where size = (
        select max(end_line-start_line) as size from symbols
    )
    """,
    )
    print(f"LARGEST: {size}")


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

    def is_interesting_release(tag):
        return re.match(r"^[0-9.]+$", tag.name) is not None

    # pylint: disable=using-constant-test
    if False:
        tags = filter(is_interesting_release, repo.tags)
    else:
        tags = repo.tags

    # TODO: sort semver
    for tagref in list(tags):
        cool = is_interesting_release(tagref)
        if not cool:
            print("-", end=" ")
        print_release(tagref)

    print()


def cmd_show(project_path):
    project_dir = Path(project_path)
    print(project_dir)
    repo = git.Repo(project_dir)
    tree, source_paths = get_project(repo)
    print_project(project_dir, source_paths)
    print(f"{'PATH':50}\tBYTES\tTAGS")
    for path in source_paths:
        info = make_file_info(tree[path])
        info = info["file_info"]
        print(f"{path:50}\t{info['num_bytes']}\t{info['num_tags']}")
    print("DONE")


def cmd_nov(project_path):
    def is_release(tag):
        return tag.name.startswith("v")

    repo = git.Repo(project_path)
    release_tags = filter(is_release, repo.tags)
    names = [t.name for t in release_tags]
    assert "v4.5.1" in names
    assert len(names) > 10
    print("okay")


def main():
    try:
        cmd = sys.argv[1]
        project = sys.argv[2]
        cmd_func = globals()[f"cmd_{cmd}"]
    except (KeyError, IndexError):
        sys.exit(get_usage())

    cmd_func(project)


if __name__ == "__main__":
    main()
