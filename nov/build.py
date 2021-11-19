"""
USAGE

shotglass.py <command> <project path>
"""

import logging
import re
import subprocess
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

import git


CTAGS_ARGS = "ctags --fields=+zK --excmd=number -o -".split()
# Example: "asbool settings.py 6; kind:function"
CTAGS_PAT = re.compile(
    r"(?P<name> \S+) .*? " + r"(?P<line_num> \d+) ;.+ " + r"kind:(?P<kind> \S+)",
    re.VERBOSE,
)
logging.basicConfig(format="%(asctime)-15s %(message)s", level=logging.INFO)


def show_details(db):
    print("DETAILS:")
    for row in db.execute("select * from files order by 1 limit 3"):
        print(row)


def run_ctags(path):
    cmd = CTAGS_ARGS + [path]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.stdout


def parse_ctags(blob):
    return CTAGS_PAT.finditer(blob)


def list_paths(repo):
    return repo.git.ls_files().split("\n")


# TODO make more general
def is_source_path(path):
    return Path(path).suffix in (".py", ".c")


# TODO make more general
def is_interesting(path):
    return not re.search(r"(docs|migrations|tests)/", path)


def is_interesting_source(path):
    return is_source_path(path) and is_interesting(path)


def format_summary(tags):
    return {"num_tags": len(tags)}


def make_file_info(entry, project_dir):
    return {"path": entry.path, "num_bytes": entry.size}


def make_tags_info(fullpath):
    """
    find info about all tags/symbols in a single source file
    """
    ctags_text = run_ctags(fullpath)
    for match in parse_ctags(ctags_text):
        yield match.groupdict()


def print_project(project_dir, source_paths):
    p_name = project_dir.name
    num_source = len(source_paths)
    print(f"PROJECT:{p_name} {num_source} source files")


def get_project(repo):
    try:
        tree = repo.heads.master.commit.tree
    except AttributeError as err:
        attrs = [attr for attr in dir(repo.heads) if not attr.startswith("_")]
        sys.exit(f"tags?? {attrs}\n{err}")
    paths = list_paths(repo)
    assert len(paths) > 0, "No source"
    # paths = filter(is_interesting_source, paths)
    paths = filter(is_source_path, paths)
    paths = list(paths)
    assert len(paths) > 0, "No interesting source"
    return tree, paths
    paths = filter(is_source_path, paths)
    paths = filter(is_interesting, paths)
    paths = list(paths)
    paths = list(paths)


def get_usage():
    cmd_list = [name for name in globals() if name.startswith("cmd_")]
    usage = [__doc__, f"Commands: {cmd_list}"]
    return "\n".join(usage)


def setup_db(db):
    db.execute("drop table if exists files")
    db.execute(
        """
        create table files (
            id integer primary key, -- TODO rowid?
            path text,
            byte_count int
            );
        """
    )
    db.execute("drop table if exists symbols")
    db.execute(
        """
        create table symbols (
            file_id int,
            name text,
            foreign key (file_id) references files(id));
        """
    )


def get_db():
    con = sqlite3.connect("main.db")
    cur = con.cursor()
    return con, cur


def select1(db, sql):
    db.execute(sql)
    return db.fetchone()[0]


def selectall(db, sql):
    db.execute(sql)
    return db.fetchall()


def format_tstamp(ts):
    return datetime.fromtimestamp(ts).strftime("%c")


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


def cmd_index(project_path):
    project_dir = Path(project_path)
    print(project_dir)

    repo = git.Repo(project_dir)
    tree, source_paths = get_project(repo)
    if not source_paths:
        sys.exit("No source paths")
    con, cur = get_db()

    con.execute("PRAGMA synchronous=OFF")
    con.execute("PRAGMA foreign_keys=ON")
    setup_db(cur)

    issues = []
    values = []
    for path in source_paths:
        try:
            item = make_file_info(tree[path], project_dir)
            values.append((item["path"], item["num_bytes"]))
        except KeyError as err:
            issues.append((path, err))
            continue

    cur.executemany(
        """
    insert into files (path, byte_count) values (?, ?)
    """,
        values,
    )
    con.commit()

    num_files = select1(cur, "select count(*) from files")
    print(f"NUM FILES: {num_files}")

    values = []
    if False:
        path = source_paths[0]
        fullpath = project_dir / path
        item = make_tags_info(fullpath)
        # file_id int, name
        values.append((path, "beer"))
    else:
        for path in [source_paths[10]]:
            fullpath = project_dir / path
            for tag in make_tags_info(fullpath):
                values.append((path, tag["name"]))
    cur.executemany(
        """
    insert into symbols (file_id, name) values (
        (select id from files where path=?),
        ?)
    """,
        values,
    )
    con.commit()

    show_details(con)
    con.close()
    if issues:
        print(f"NOTE: {len(issues)} issues found")


def cmd_info(project_path):
    _, db = get_db()

    num_files = select1(db, "select count(*) from files")
    print(f"NUM FILES: {num_files}")
    file_info = selectall(db, "select * from files limit 3")
    print(f"FILES: {file_info}")

    num_symbols = select1(db, "select count(*) from symbols")
    print(f"NUM SYMBOLS: {num_symbols}")
    sym_info = selectall(db, "select * from symbols limit 3")
    print(f"SYMBOLS: {sym_info}")


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

    if False:
        tags = filter(is_interesting_release, repo.tags)
    else:
        tags = repo.tags

    # TODO sort semver
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
        info = make_file_info(tree[path], project_dir)
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
