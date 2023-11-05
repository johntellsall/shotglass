#!/usr/bin/env python3
#
"""
Shotglass: info about codebases over time
"""

import logging
import pprint
import re
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
    if not items:
        click.secho(f"{path}: {release=}: no files")
        return

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
    def is_dull(path):
        # __init__.py and __manifest__.py
        return path.endswith("__.py")

    if not path.endswith(".py"):  # TODO:
        click.echo(f"{path=}: unsupported language")
        return

    sql = "select id from file where hash=?"
    file_id = query1(con, sql=sql, args=[filehash])

    # copy file from Git to filesystem (uncompress if needed)
    # FIXME: support other languages
    run.run_blob(f"git -C {project_path} show {filehash} > .temp.py")

    # parse symbols from source file
    items = list(run.run_ctags(".temp.py"))
    if not items and not is_dull(path):
        click.secho(f"- {path=}: no symbols")
        return

    # insert symbols into database
    insert_sym = f"""
    insert into symbol (
        name, path, line_start, line_end, kind, file_id
    ) values (
        :name, '{path}', :line, :end, :kind, {file_id})
    """
    con.executemany(insert_sym, IterFixedFields(items))


def do_add_symbols(con, project_path, limit=False):
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
            batch = min(batch*2, 50)
            
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

    # FIXME: handle this better!
    if releases == ['']:
        logging.warning("%s: no release tags -- using HEAD", project_name)
        releases = ['HEAD']

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

    if 1:
        proj_config = goodsource.GoodSourceConfig(project_path)
        proj_config.set_good_pat('latest')
    else:

        class SqlAlchemyConfig(goodsource.GoodSourceConfig):
            is_good_tag = re.compile(r"^rel[0-9_]+_0$").match
            # TODO:

            def is_good_tag(_self, s):
                return s == "rel_1_4_0"

        proj_config = SqlAlchemyConfig(project_path)

    # Git releases -> database; show count
    db_add_releases(con, proj_config)

    con.commit()

    # per release -> add files to db
    do_add_files(con, project_path)
    con.commit()

    # per file -> add symbols to db
    do_add_symbols(con, project_path=project_path)
    con.commit()

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


@cli.command()
@click.argument("path")
def count_defs(path):
    "print rough count of Python functions in project"
    cmd = f"cd {path} ; git ls-files '*.py' | xargs grep -w def | wc -l"
    count = int(run.run_blob(cmd))
    click.echo(f"{path}: def {count=}")


if __name__ == "__main__":
    cli()
