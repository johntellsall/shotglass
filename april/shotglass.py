import click
import build as build_cmd

@click.group()
def cli():
    pass

@cli.command()
@click.argument('paths', nargs=-1)
def build(paths):
    build_cmd.build(paths)

if __name__ == "__main__":
    cli()
