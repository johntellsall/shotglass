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
    var_pat = re.compile(r"^(?P<name> \S+) .* kind:(?P<kind> \S+)", re.VERBOSE)
    return var_pat.finditer(blob)


def list_paths(repo):
    return repo.git.ls_files().split("\n")
    # return [path for path in paths if path.endswith(".py")]


# TODO make more general
def is_source_path(path):
    return path.endswith(".py")


# def is_interesting(path):
#     if path.startswith("docs/"):
#         return False
#     if "/scripts/" in path:
#         return False
#     # elif re.search(r"/(scripts|tests)/", path):
#     #     return False
#     return True


# def list_source_items(repo):
#     tree = repo.heads.master.commit.tree
#     return [item for item in tree if item.path.endswith(".py")]


def main():
    project_dir = Path(sys.argv[1])
    print(project_dir)
    repo = git.Repo(project_dir)
    tree = repo.heads.master.commit.tree
    source_paths = filter(is_source_path, list_paths(repo))
    # source_paths = filter(is_interesting, source_paths)
    for path in list(source_paths)[:100]:
        entry = tree[path]
        print(f"{entry.path} {entry.size}")
        fullpath = project_dir / entry.path
        ctags_text = run_ctags(fullpath)
        for tag in parse_ctags(ctags_text):
            print(f"\t{tag.groupdict()}")
    print("DONE")


if __name__ == "__main__":
    main()
