import re
import subprocess
import sqlite3
import sys
from pathlib import Path

import git


def setup(db):
    db.execute(
        """
    CREATE TABLE files (path text, line_count int)
    """
    )


def show_info(db):
    for row in db.execute("SELECT * FROM files ORDER BY 1"):
        print(row)


def db_demo():
    con = sqlite3.connect("may.db")
    cur = con.cursor()

    cur.execute("insert into files values (?, ?)", ("C", 49))

    con.commit()

    show_info(con)
    con.close()


def run_ctags(path):
    cmd = "ctags --fields=+zK -o -".split()
    proc = subprocess.run(cmd + [path], capture_output=True, text=True)
    return proc.stdout


def parse_ctags(blob):
    # "tests_require	..//setup.py	...	kind:variable"
    tag_exp = r"^(?P<name> \S+) .*? kind:(?P<kind> \S+)"
    tag_pat = re.compile(tag_exp, re.VERBOSE)
    tag_iter = tag_pat.finditer(blob)
    breakpoint()
    tag_iter = tag_iter


def list_paths(repo):
    return repo.git.ls_files().split("\n")
    # return [path for path in paths if path.endswith(".py")]


# TODO make more general
def is_source_path(path):
    return path.endswith(".py")


# TODO make more general
def is_interesting(path):
    return not re.search(r"(docs|tests)/", path)


# def show_detail():
#     for tag in parse_ctags(ctags_text):
#         print(f"\t{tag.groupdict()}")


def format_summary(tags):
    breakpoint()
    return f"{len(tags)} tags"


def main_scan_project():
    project_dir = Path(sys.argv[1])
    print(project_dir)
    repo = git.Repo(project_dir)
    tree = repo.heads.master.commit.tree
    source_paths = filter(is_source_path, list_paths(repo))
    source_paths = filter(is_interesting, source_paths)
    for path in ["pyramid/view.py"]:  # list(source_paths)[:100]:
        entry = tree[path]
        print(f"{entry.path} {entry.size}")
        fullpath = project_dir / entry.path
        ctags_text = run_ctags(fullpath)
        tags = list(parse_ctags(ctags_text))
        if not tags:
            print("?")
        else:
            print([tag["name"] for tag in tags])
            print("woot")
        # print(format_summary(tags))
    print("DONE")


def main():
    project_dir = sys.argv[1]
    repo = git.Repo(project_dir)
    tree = repo.heads.master.commit.tree

    source_path = sys.argv[2]
    for path in [source_path]:
        entry = tree[path]
        print(f"{entry.path} {entry.size}")
        fullpath = Path(project_dir) / entry.path
        ctags_text = run_ctags(fullpath)
        tags = list(parse_ctags(ctags_text))
        if not tags:
            print("?")
        else:
            print([tag["name"] for tag in tags])
            print("woot")
        # print(format_summary(tags))
    print("DONE")


if __name__ == "__main__":
    main()
