import re
import subprocess
import sqlite3
import sys
from pathlib import Path

import git

CTAGS_ARGS = "ctags --fields=+zK --excmd=number -o -".split()
CTAGS_PAT = re.compile(r"(?P<name> \S+) .*? kind:(?P<kind> \S+)", re.VERBOSE)


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


# def show_detail():
#     for tag in parse_ctags(ctags_text):
#         print(f"\t{tag.groupdict()}")


def format_summary(tags):
    return {"num_tags": len(tags)}


def main():
    project_dir = Path(sys.argv[1])
    print(project_dir)
    repo = git.Repo(project_dir)
    tree = repo.heads.master.commit.tree
    source_paths = filter(is_source_path, list_paths(repo))
    source_paths = filter(is_interesting, source_paths)
    source_paths = list(source_paths)
    p_name = project_dir.name
    num_source = len(source_paths)
    print(f"PROJECT:{p_name} {num_source} source files")
    for path in source_paths:
        entry = tree[path]
        info = {"path": entry.path, "num_bytes": entry.size}
        fullpath = project_dir / entry.path
        ctags_text = run_ctags(fullpath)
        tags = list(parse_ctags(ctags_text))
        info.update(format_summary(tags))
        print("{path} {num_bytes} {num_tags}".format(**info))
    print("DONE")


if __name__ == "__main__":
    main()
