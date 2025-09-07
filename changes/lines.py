import click
import os

from PIL import Image, ImageDraw, ImageFont

from symbols import parse_path


def render(draw, symfile):
    def symlength(sym):
        if not sym.get('end'):
            return 0
        return sym['end'] - sym['line']
    sym = [s for s in symfile.symbols if symlength(s) > 2]
    breakpoint()


@click.command()
@click.argument('paths', nargs=-1, type=click.Path(exists=True))
def main(paths):
    width, height = 800, 600
    file_image = Image.new("RGB", (width, height), color="gray")
    draw = ImageDraw.Draw(file_image)

    for path in paths:
        symfile = parse_path(path)
        
        render(draw, symfile)

if __name__ == '__main__':
    main()