# shotlib.py

import re
import sqlite3
import sys
from pathlib import Path


def format_lines(objs):
    return "\n".join(map(str, objs))


# TODO make more general
def is_source_path(path):
    return Path(path).suffix in (".py", ".c")


# TODO make more general
def is_interesting(path):
    return not re.search(r"(docs|examples|migrations|tests)/", path)


def is_interesting_source(path):
    return is_source_path(path) and is_interesting(path)


def get_db(temporary=False):
    path = ":memory:" if temporary else "main.db"
    con = sqlite3.connect(path)  # pylint: disable=no-member
    cur = con.cursor()
    return con, cur


def get_db2(temporary=False):
    path = ":memory:" if temporary else "main.db"
    return sqlite3.connect(path)  # pylint: disable=no-member


def get_main_tree(git_repo):
    heads = git_repo.heads
    if hasattr(heads, "master"):
        return heads.master.commit.tree
    try:
        return git_repo.heads.main.commit.tree
    except AttributeError as err:
        print(f"get_main_tree:heads?? {git_repo.heads}")
        if not (len(git_repo.heads) == 1):
            sys.exit(f"heads?? {git_repo.heads}\n{err}")
        return git_repo.heads[0].commit.tree


def get_project(repo):
    tree = get_main_tree(repo)
    paths = list_paths(repo)
    assert len(paths) > 0, "No source"
    paths = filter(is_interesting_source, paths)
    # paths = filter(is_source_path, paths)
    paths = list(paths)
    assert len(paths) > 0, "No interesting source"
    return tree, paths
    # pylint: disable=unreachable
    paths = filter(is_source_path, paths)
    paths = filter(is_interesting, paths)
    paths = list(paths)
    paths = list(paths)


def list_paths(repo):
    return repo.git.ls_files().split("\n")


def make_file_info(entry):
    "return dict of information for single source file"
    return {"path": entry.path, "num_bytes": entry.size}


def select1(db, sql):
    curs = db.execute(sql)
    return curs.fetchone()[0]


def selectall(db, sql):
    db.execute(sql)
    return db.fetchall()


def show_all_details(db):
    print("DETAILS:")

    print("-- files")
    for row in db.execute("select * from files order by 1 limit 3"):
        print(row)

    print("-- symbols")
    for row in db.execute(
        """
    select * -- s.name, s.start_line
    from symbols s
    order by 1 limit 3
    """
    ):
        print(row)

    if False:
        print("-- symbols2")
        for row in db.execute(
            """
        select f.id, f.path, s.name, s.start_line
        from files as f, symbols as s
        join files on f.id = s.file_id
        order by 1 limit 10
        """
        ):
            print(row)

    print("-- releases")
    for row in db.execute(
        """
    select *
    from releases
    order by 1 limit 3
    """
    ):
        print(row)


def show_project_details(db, project):
    print(f"DETAILS for {project}:")

    proj_id = select1(db, f"select id from projects where name='{project}'")
    print(f"NAME: {project} NUM: {proj_id}")

    num_files = select1(db, f"select count(*) from files where project_id={proj_id}")
    print(f"NUM FILES: {num_files}")
    file_info = selectall(db, f"select * from files where project_id={proj_id} limit 3")
    print(f"FILES:\n{format_lines(file_info)}")
