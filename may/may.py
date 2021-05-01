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


def main():
    project_dir = Path(sys.argv[1])
    repos = git.Repo(project_dir)
    tree = repos.heads.master.commit.tree
    print(project_dir)
    for entry in tree:
        if not entry.path.endswith(".py"):
            continue
        print(entry)
        print(f"{entry.path} {entry.size}")
        fullpath = project_dir / entry.path
        ctags = run_ctags(fullpath)
        print(ctags)
        blam
        # breakpoint()


if __name__ == "__main__":
    main()
