# cmd_import.py
# - db: files are hashes
# - direct Git commands
#
import re
import sqlite3
import subprocess
from pathlib import Path

import click


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
    db.execute("drop table if exists symbols")  # <== XXXXX

    db.execute(
        """
        create table file_hash(
            project_name, release, path, hash, size_bytes
        )
        """
    )

    db.execute(
        """
        create table symbols (
            hash text,
            name text,
            start_line int,
            end_line int,
            kind text,
            foreign key (hash) references file_hash(hash)
        )
        """
    )


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: SYMBOLS


def import_symbols(db):
    from cmd_index import make_tags_info

    path = "../SOURCE/flask/src/flask/views.py"
    symbols = make_tags_info(path)
    # assert 0, list(symbols)[0]

    # {'_type': 'tag', 'name': 'MethodView', 'path': '../SOURCE/flask/src/flask/views.py', 'access': 'public', 'inherits': 'View, metaclass=MethodViewType', 'language': 'Python', 'line': 133, 'kind': 'class', 'roles': 'def', 'end': 158}
    def to_symbol(info):
        "convert Ctags symbols to Shotglass"
        return "123", info["name"], info["line"], info.get("end"), info["kind"]

    # values = [["123", "xname", "xstart", "xend", "xkind"]]

    db.executemany(
        """
    insert into symbols (hash, name, start_line, end_line, kind) values (
        ?, -- file hash
        ?, -- symbol name
        ?, -- start_line
        ?, -- end_line
        ? -- kind
        )
    """,
        map(to_symbol, symbols),
    )


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: RELEASES


def import_release(db, path, release, project_name):
    """
    add Git info into database
    Single file, single release (Git tag)
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
    'skip tags/releases with letters, e.g. "1.2alpha3"'
    return bool(re.compile("[0-9.]+$").match(release))


def is_okay_release(release):
    """
    Ignore most micro releases
    Return True if major.minor (1.3) or micro=0 (1.2.0)
    """
    nums = release.split(".")
    return len(nums) == 2 or nums[-1] == "0"


# def cmd_initdb(paths):
#     con = sqlite3.connect("jan.db")
#     con.execute("PRAGMA synchronous=OFF")
#     con.execute("PRAGMA foreign_keys=ON")

#     click.echo("Initialized the database")

#     setup(con)

#     import_symbols(con)

#     # for path in paths:
#     #     project_name = Path(path).name

#     #     releases = list(filter(is_interesting_release, list_git_tags(path)))

#     #     setup(con)
#     #     for release in filter(is_minor, releases):
#     #         click.echo(f"{project_name} - release {release}")
#     #         import_release(con, path, release, project_name)

#     con.commit()
#     con.close()


def show_info(db):
    click.echo("File Hashes")
    click.echo(list(db.execute("select count(*) from file_hash")))
    click.echo(list(db.execute("select * from file_hash limit 4")))
    click.echo("Symbols")
    click.echo(list(db.execute("select count(*) from symbols")))
    click.echo(list(db.execute("select * from symbols limit 4")))


@click.command()
@click.argument("paths", nargs=-1)
def initdb(paths):
    con = sqlite3.connect("jan.db")
    click.echo("Initialized the database")

    setup(con)

    for project_path in paths:
        project_name = Path(project_path).name

        releases = list(filter(is_interesting_release, list_git_tags(project_path)))

        for release in filter(is_okay_release, releases):
            click.echo(f"{project_name} - release {release}")
            import_release(con, project_path, release, project_name)

        import_symbols(con)

    con.commit()
    show_info(con)
    con.close()


if __name__ == "__main__":
    if 0:
        import sys

        cmd_initdb(sys.argv[1])
    else:
        initdb()
