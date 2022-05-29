#!/usr/bin/env python3
#
"""
Shotglass: info about codebases over time
"""

import logging
import pprint
from pathlib import Path, PurePath

import click

import commands
import goodsource
import run
import state
from state import query1

logging.basicConfig(format="%(asctime)-15s %(message)s", level=logging.INFO)


# :::::::::::::::::::: APP-CENTRIC FUNCTIONS


def db_add_project(con, project_path):
    """
    add single project record into database
    """
    insert_project = "insert into project (name) values (:name)"
    name = PurePath(project_path).name
    con.execute(insert_project, [name])


def db_add_releases(con, project_obj):
    """
    for project, insert interesting (Git) tags/releases into db
    """
    tags = project_obj.get_tags()
    project_path = project_obj.path
    if not tags:
        click.secho(f"{project_path}: no good tags, skipping project", fg="red")
        return

    project_id = db_get_project_id(con, project_path)
    insert_release = f"""
    insert into release (label, project_id)
    values (:label, {project_id}
    )"""
    items = [{"label": tag} for tag in tags]
    con.executemany(insert_release, items)


def db_get_project_id(con, path):
    "helper: fetch project's int ID"
    name = PurePath(path).name
    # TODO: query1 with args
    sql = f"select id from project where name='{name}'"
    return query1(con, sql=sql)


# TODO: add via *hash* not path
def db_add_files(con, path, project_id, release):
    """
    for project and release/tag, add interesting files into db
    """
    all_items = list(goodsource.git_ls_tree(path, release=release))
    items = list(goodsource.filter_goodsource(all_items))

    insert_file = (
        "insert into file (project_id, release, path, hash, size_bytes)"
        f" values ({project_id}, '{release}', :path, :hash, :size_bytes)"
    )
    con.executemany(insert_file, items)


# CTAGS
# {'_type': 'tag', 'name': 'Flask', 'path': '.temp.py', 'access': 'public',
# 'inherits': 'object', 'language': 'Python', 'line': 173, 'kind': 'class',
# 'roles': 'def', 'end': 655}


class IterFixedFields:
    """
    ensure dict-like items have all required fields
    - ex: "end" is not always provided by Ctags
    """

    FIELDS = ("name", "path", "start", "end", "kind")

    def __init__(self, items):
        self.items = items
        self.proto = dict.fromkeys(self.FIELDS)

    def __iter__(self):
        return self

    def __next__(self):
        if not self.items:
            raise StopIteration
        item = self.proto.copy()
        item.update(self.items.pop(0))
        return item


# TODO: how do we assoc release with symbol? Needed?
def db_add_symbols(con, project_path, filehash, path):
    """
    Parse symbols from file, add to database
    """
    assert path.endswith(".py")  # TODO:

    # copy file from Git to filesystem (uncompress if needed)
    run.run_blob(f"git -C {project_path} show {filehash} > .temp.py")

    # parse symbols from source file
    items = list(run.run_ctags(".temp.py"))

    # insert symbols into database
    insert_sym = f"""
    insert into symbol (name, path, line_start, line_end, kind) values (
        :name, '{path}', :line, :end, :kind)
    """
    con.executemany(insert_sym, IterFixedFields(items))


def do_add_symbols(con, project_path, limit):
    """
    list files from database (one project only)
    - parse each file for symbols
    - add symbols to database
    """
    # Per file: extract symbols
    # TODO: restrict to interesting releases+files
    project_id = db_get_project_id(con, project_path)
    project_name = Path(project_path).name

    click.secho(f"{project_name}: adding file info", fg="cyan")
    sql = f"select path, hash, release from file where project_id={project_id}"
    if limit:
        sql += " LIMIT 5"
    batch = 5
    for num, (path, filehash, _release) in enumerate(con.execute(sql)):
        if not num or (num + 1) % batch == 0:
            click.secho(f"- {num+1:03d} {path=} {filehash=}")
            batch *= 2
        # TODO: more work here
        db_add_symbols(con, project_path, filehash=filehash, path=path)
    con.commit()


def do_add_files(con, project_path):
    """
    for each project's releases, add those files into database
    """

    # Per project-release: add release files -> database
    project_id = db_get_project_id(con, project_path)
    project_name = Path(project_path).name

    click.secho(f"{project_name}: adding files", bg="magenta", fg="black")

    release_sql = f"select label from release where project_id={project_id}"
    releases = [label for (label,) in con.execute(release_sql)]
    goodsource.sort_versions(releases)

    for label in releases:
        click.echo(f"{project_id=} release {label}")
        db_add_files(con, project_id=project_id, path=project_path, release=label)
    con.commit()

    # Per project-release: show count of files
    click.secho(f"{project_name}: files per release", fg="yellow")

    for label in releases:
        sql = (
            "select count(*) from file where "
            f"project_id={project_id} and release = ?"
        )
        result = list(con.execute(sql, [label]))
        click.secho(f"rel {label}: num files: {result[0][0]}")


# :::::::::::::::::::: COMMANDS


@click.group()
def cli():
    pass


@cli.command()
def list_git():
    commands.cmd_list_git()


@cli.command()
def summary():
    commands.cmd_summary()


@cli.command()
@click.argument("project_path")
def add_project(project_path):
    """
    list project Releases, and stats for each release
    """

    con = state.get_db(temporary=False)

    db_add_project(con, project_path)
    con.commit()

    proj_config = goodsource.AllSourceConfig(project_path)

    # Git releases -> database; show count
    db_add_releases(con, proj_config)

    con.commit()

    # per release -> add files to db
    do_add_files(con, project_path)
    con.commit()

    # TODO: do_add_symbols(con, limit=limit, project_path=project_path)

    con.close()


@cli.command()
@click.argument("path")
def ls_tags(path):
    """
    list tags in Git repos
    """
    click.echo(f"List Tags {path}")
    tags = goodsource.git_tag_list(path)
    pprint.pprint(tags)


@cli.command()
def reset_db():
    """
    delete database
    """
    try:
        Path("main.db").unlink()
    except FileNotFoundError:
        pass


@cli.command()
@click.argument("path")
def ctags(path):
    """
    show symbols of single source file (from Ctags)
    """
    click.echo(f"Ctags {path}")
    symbols = list(run.run_ctags(path))
    pprint.pprint(symbols)


if __name__ == "__main__":
    cli()
