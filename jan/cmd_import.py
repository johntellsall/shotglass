import subprocess
import sys
import sqlite3
from pathlib import Path


def get_git_release_blob(path, release="2.0.0"):
    """
    get Git info about all files in given release
    """
    cmd = f"git -C {path} ls-tree  -r --long '{release}'"
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
    return proc.stdout


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


def main(path):
    project_name = Path(path).name
    con = sqlite3.connect("jan.db")

    setup(con)
    for release in ["1.0", "2.0.0"]:
        print(f"{project_name} - release {release}")
        import_release(con, path, release, project_name)

    print(list(con.execute("select count(*) from file_hash")))
    print(list(con.execute("select * from file_hash limit 1")))


if __name__ == "__main__":
    main(sys.argv[1])
