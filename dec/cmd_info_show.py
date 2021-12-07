# import logging
# import sys
# from datetime import datetime
from pathlib import Path

import git

from shotlib import (
    get_db,
    get_project,
    make_file_info,
    select1,
    selectall,
)


def format_lines(objs):
    return "\n".join(map(str, objs))


def print_project(project_dir, source_paths):
    p_name = project_dir.name
    num_source = len(source_paths)
    print(f"PROJECT:{p_name} {num_source} source files")


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

    if False:
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


# TODO: fix
def cmd_show(project_path):
    project_dir = Path(project_path)
    print(project_dir)
    repo = git.Repo(project_dir)
    tree, source_paths = get_project(repo)
    print_project(project_dir, source_paths)
    print(f"{'PATH':50}\tBYTES\tTAGS")
    for path in source_paths:
        try:
            info = make_file_info(tree[path])
            print(f"{path:50}\t{info['num_bytes']}")
        except KeyError as err:
            print(f"?? {path}: {err}")
    print("DONE")
