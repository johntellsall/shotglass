# cmd_info_show.py
#
from pathlib import Path

import git

from shotlib import (
    format_lines,
    get_db,
    get_project,
    make_file_info,
    select1,
    selectall,
    show_project_details,
)


def print_project(project_dir, source_paths):
    p_name = project_dir.name
    num_source = len(source_paths)
    print(f"PROJECT:{p_name} {num_source} source files")


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


# TODO: add quoting
def cmd_pinfo(project):  # pylint: disable=unused-argument
    con, cur = get_db()

    show_project_details(db=cur, project=project)
    # proj_id = select1(db, f"select id from projects where name='{project}'")
    # print(f"NAME: {project} NUM: {proj_id}")

    # num_files = select1(db, f"select count(*) from files where project_id={proj_id}")
    # print(f"NUM FILES: {num_files}")
    # file_info = selectall(db, f"select * from files where project_id={proj_id} limit 3")
    # print(f"FILES:\n{format_lines(file_info)}")

    # num_symbols = select1(
    #     db, f"select count(*) from symbols where project_id={proj_id}"
    # )
    # print(f"NUM SYMBOLS: {num_symbols}")
    # sym_info = selectall(
    #     db, f"select * from symbols where project_id={proj_id} limit 3"
    # )
    # print(f"SYMBOLS:\n{format_lines(sym_info)}")

    # num_releases = select1(db, "select count(*) from releases, projects  where name='{project}'")
    # print(f"NUM RELEASES: {num_releases}")
    # release_info = selectall(
    #     db, "select * from releases where name='{project}' limit 3"
    # )
    # print(f"RELEASES:\n{format_lines(release_info)}")


def cmd_info(project_path):  # pylint: disable=unused-argument
    _, db = get_db()

    proj_info = selectall(db, "select * from projects")
    print(f"PROJECTS:\n{format_lines(proj_info)}")

    num_files = select1(db, "select count(*) from files")
    print(f"NUM FILES: {num_files}")
    file_info = selectall(db, "select * from files limit 3")
    print(f"FILES:\n{format_lines(file_info)}")

    num_symbols = select1(db, "select count(*) from symbols")
    print(f"NUM SYMBOLS: {num_symbols}")
    sym_info = selectall(db, "select * from symbols limit 3")
    print(f"SYMBOLS:\n{format_lines(sym_info)}")

    num_releases = select1(db, "select count(*) from releases")
    print(f"NUM RELEASES: {num_releases}")
    release_info = selectall(db, "select * from releases limit 3")
    print(f"RELEASES:\n{format_lines(release_info)}")

    if False:  # pylint: disable=using-constant-test
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
