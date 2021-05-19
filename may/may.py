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


def show_db_info(db):
    for row in db.execute("SELECT * FROM files ORDER BY 1"):
        print(row)


def run_ctags(path):
    cmd = CTAGS_ARGS + [path]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.stdout


def parse_ctags(blob):
    tag_iter = CTAGS_PAT.finditer(blob)
    return tag_iter


def list_paths(repo):
    return repo.git.ls_files().split("\n")


# TODO make more general
def is_source_path(path):
    return path.endswith(".py")


# TODO make more general
def is_interesting(path):
    return not re.search(r"(docs|tests)/", path)


def is_interesting_source(path):
    return is_source_path(path) and is_interesting(path)


def format_summary(tags):
    return {"num_tags": len(tags)}


def parse_entry(entry, project_dir):
    file_info = {"path": entry.path, "num_bytes": entry.size}
    fullpath = project_dir / entry.path
    ctags_text = run_ctags(fullpath)
    tags = list(parse_ctags(ctags_text))
    file_info.update(format_summary(tags))
    return dict(file_info=file_info, tags=tags)


def print_project(project_dir, source_paths):
    p_name = project_dir.name
    num_source = len(source_paths)
    print(f"PROJECT:{p_name} {num_source} source files")


def get_project(repo):
    tree = repo.heads.master.commit.tree
    paths = filter(is_source_path, list_paths(repo))
    paths = filter(is_interesting, paths)
    paths = list(paths)
    return tree, paths


def setup_db(db):
    db.execute("DROP TABLE files")
    db.execute(
        """
    CREATE TABLE files (path text, byte_count int)
    """
    )


def index_project(project_path):
    project_dir = Path(project_path)
    print(project_dir)

    repo = git.Repo(project_dir)
    tree, source_paths = get_project(repo)
    con = sqlite3.connect("may.db")
    cur = con.cursor()

    setup_db(cur)

    issues = []
    for path in source_paths:
        try:
            info = parse_entry(tree[path], project_dir)
        except KeyError as err:
            issues.append((path, err))
            continue
        # print(info)
        finfo = info["file_info"]
        cur.execute(
            "INSERT INTO files VALUES (?, ?)", (finfo["path"], finfo["num_bytes"])
        )

    con.commit()

    show_db_info(con)
    con.close()
    if issues:
        print(f"NOTE: {len(issues)} issues found")


def show_project(project_path):
    project_dir = Path(project_path)
    print(project_dir)
    repo = git.Repo(project_dir)
    tree, source_paths = get_project(repo)
    print_project(project_dir, source_paths)
    for path in source_paths:
        info = parse_entry(tree[path], project_dir)
        file_info = info["file_info"]
        print("{path} {num_bytes} {num_tags}".format(**file_info))
    print("DONE")


def format_tstamp(ts):
    return datetime.fromtimestamp(ts).strftime("%c")


# TODO rename "show_releases"
def show_tags(project_path):
    project_dir = Path(project_path)
    print(project_dir)
    repo = git.Repo(project_dir)

    def is_interesting_release(tag):
        return re.match(r"^[0-9.]+$", tag.name) is not None

    # tags = list(filter(is_interesting_release, repo.tags))
    tags = repo.tags
    # TODO sort semver
    for tagref in list(tags)[:10]:
        cool = is_interesting_release(tagref)
        if not cool:
            print("-", end=" ")
        summary = tagref.commit.summary
        tag_tree = tagref.commit.tree
        com_date = tagref.commit.committed_date
        com_datestr = format_tstamp(com_date)
        print(len(list(tag_tree.traverse())))
        com_count = sum(1 for _ in tag_tree.traverse())
        com_size = sum(c.size for c in tag_tree.traverse())
        file_list = [x.path for x in tag_tree.traverse()]
        source_list = [path for path in file_list if is_interesting_source(path)]
        print(f"{tagref.name} files={len(file_list)} source={len(source_list)}")
        print(f"\t{com_datestr}")
        print(f"\t{com_count} {com_size} {summary}")
    print()


def main():
    if 0:
        show_project(sys.argv[1])
    elif 0:
        show_tags(sys.argv[1])
    else:
        index_project(sys.argv[1])


if __name__ == "__main__":
    main()
