# commands.py

# FIXME: from distutils.version import LooseVersion

import click

import goodsource
import run
import state


# TODO: remove?
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
        all_items = list(run.git_ls_tree(path, release=tag))
        click.secho(f"= {len(all_items)} total files", fg="yellow")

        items = list(goodsource.filter_good_paths(all_items))
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
