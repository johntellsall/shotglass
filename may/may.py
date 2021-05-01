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


def main():
    project_dir = Path(sys.argv[1])
    repos = git.Repo(project_dir)
    tree = repos.heads.master.commit.tree
    print(project_dir)
    source = [item for item in tree if item.path.endswith(".py")]
    for entry in source:
        print(entry)
        print(f"{entry.path} {entry.size}")
        fullpath = project_dir / entry.path
        ctags_text = run_ctags(fullpath)
        for tag in parse_ctags(ctags_text):
            print(tag.groupdict())
    print("DONE")


if __name__ == "__main__":
    main()
