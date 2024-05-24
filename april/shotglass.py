import click
import build as build_cmd
import render as render_cmd

@click.group()
def cli():
    pass

@cli.command()
@click.argument('paths', nargs=-1)
def build(paths):
    build_cmd.build(paths)

@cli.command()
def render():
    render_cmd.render()

if __name__ == "__main__":
    cli()
