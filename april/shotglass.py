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
@click.option('--out', type=click.Path())
def render(out):
    render_cmd.render(image_name=out)

if __name__ == "__main__":
    cli()
