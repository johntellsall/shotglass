import subprocess
import sys
import sqlite3


def get_git_release_blob(path, release="2.0.0"):
    cmd = f"git -C {path} ls-tree  -r --long '{release}'"
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
    # if verbose:
    #     print(f"-- RAW\n{proc.stdout[:300]}\n-- ENDRAW")
    return proc.stdout


def setup(db):
    db.execute("drop table if exists file_hash")  # <== XXXXX

    db.execute("create table file_hash(path, hash, size_bytes)")


def main(path):
    con = sqlite3.connect("jan.db")
    setup(con)

    blob = get_git_release_blob(path)

    def row2item(row):
        pre, path = row.split("\t")
        _mode, _type, hash, size_bytes = pre.split()
        return path, hash, size_bytes

    data = list(map(row2item, blob.rstrip("\n").split("\n")))

    con.executemany(
        "insert into file_hash(path, hash, size_bytes) values (?, ?, ?)", data
    )

    print(list(con.execute("select count(*) from file_hash")))


if __name__ == "__main__":
    main(sys.argv[1])
