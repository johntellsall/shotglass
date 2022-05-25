# commands.py

from distutils.version import LooseVersion

import click

import goodsource
import state


def cmd_list_git():
    """
    list project Releases, and stats for each release
    TODO: make generic (now Flask only)
    """
    path = "../SOURCE/flask"  # TODO:
    click.echo(f"List Tags {path}")
    tags = goodsource.get_good_tags(path)
    tags.sort(key=LooseVersion)

    hashes = set()
    # for each release
    for tag in tags:
        click.secho(f"release: {tag}", fg="black", bg="yellow")
        all_items = list(goodsource.git_ls_tree(path, release=tag))
        click.secho(f"= {len(all_items)} total files", fg="yellow")

        items = list(goodsource.filter_goodsource(all_items))
        click.secho(f"= {len(items)} source files", fg="yellow")

        changed_items = []
        for item in items:
            filehash = item["hash"]
            if filehash in hashes:
                continue
            hashes.add(filehash)
            changed_items.append(item)

        # show count of files changed in this release
        click.secho(f"+/- {len(changed_items)} changed source", fg="yellow")

        # .. and the files
        for item in changed_items:
            click.secho(f"- {item['path']}")


def cmd_summary():
    con = state.get_db()
    # list Projects
    # per project: count Releases, Files, Symbols
    num_projects = state.query1(con, table="project")
    num_releases = state.query1(con, table="release")
    num_files = state.query1(con, table="file")
    num_symbols = state.query1(con, table="symbol")

    click.echo(f"Projects: {num_projects} Releases: {num_releases}", nl=False)
    click.echo(f" Files: {num_files} Symbols: {num_symbols}")


# def summarize_project(con, project_name):
#     project_id = db_get_project_id(con, project_name)

#     def sql_count(table):
#         return f"select count(*) from {table} where project_id={project_id}"

#     rel_count = state.query1(con, sql_count("release"))
#     sym_count = state.query1(con, sql_count("symbol"))
#     file_count = state.query1(con, sql_count("file"))

#     click.secho(
#         f"{project_name}: Files: {file_count} Symbols: {sym_count}"
#         f" Releases: {rel_count}",
#         fg="yellow",
#     )

#     click.secho(f"{project_name}: symbol examples", fg="yellow")
#     for item in con.execute("select * from symbol limit 3"):
#         click.echo(f"- {dict(item)}")
