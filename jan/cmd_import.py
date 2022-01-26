import re
import sqlite3
import subprocess
import sys
from pathlib import Path


def run(cmd):
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
    out_blob = proc.stdout
    out_lines = out_blob.rstrip("\n").split("\n")
    return out_lines


def get_git_release_blob(path, release="2.0.0"):
    """
    get Git info about all files in given release
    """
    cmd = f"git -C {path} ls-tree  -r --long '{release}'"
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
    return proc.stdout


def list_git_tags(path):
    return run(f"git -C {path} tag --list")


def setup(db):
    """
    create database tables
    """
    db.execute("drop table if exists file_hash")  # <== XXXXX

    db.execute(
        """
    create table file_hash(
        project_name, release, path, hash, size_bytes
        )
    """
    )


def import_release(db, path, release, project_name):
    """
    add Git info into database
    """
    blob = get_git_release_blob(path, release)

    def row2item(row):
        pre, path = row.split("\t")
        _mode, _type, hash, size_bytes = pre.split()
        return path, hash, size_bytes

    data = list(map(row2item, blob.rstrip("\n").split("\n")))

    insert_sql = f"""
insert into file_hash(path, hash, size_bytes, release, project_name)
values (?, ?, ?, '{release}', '{project_name}')
    """
    db.executemany(insert_sql, data)


def is_interesting_release(release):
    return bool(re.compile("[0-9.]+$").match(release))


def main(path):
    project_name = Path(path).name
    con = sqlite3.connect("jan.db")

    # skip tags/releases with letters, e.g. "1.2alpha3"
    releases = list(filter(is_interesting_release, list_git_tags(path)))

    setup(con)
    for release in releases:
        print(f"{project_name} - release {release}")
        import_release(con, path, release, project_name)

    print(list(con.execute("select count(*) from file_hash")))
    print(list(con.execute("select * from file_hash limit 1")))


if __name__ == "__main__":
    main(sys.argv[1])
