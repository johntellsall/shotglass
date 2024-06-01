import click

import build as build_cmd
import render as render_cmd


@click.group()
def cli():
    pass


@cli.command()
@click.argument("paths", nargs=-1)
def build(paths):
    build_cmd.build(paths)


@cli.command()
@click.option("--out", type=click.Path())
@click.option("--show", is_flag=True)
@click.option("--show-iterm", is_flag=True)
@click.option("--show-macos", is_flag=True)
def render(out, show, show_iterm, show_macos):
    render_cmd.render(
        image_name=out, show=show, show_iterm=show_iterm, show_macos=show_macos
    )


if __name__ == "__main__":
    cli()
