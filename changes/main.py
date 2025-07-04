from symbols import parse_path

import click
from PIL import Image
import math
import subprocess
import tempfile


def render(symfile):
    if symfile.num_lines < 10:
        return None
    size = math.ceil(symfile.num_lines ** 0.5)
    img = Image.new("RGB", (size, size), color="white")
    return img


def show(imgpath):
    subprocess.run(["imgcat-iterm2", "--legacy", imgpath])

def is_interesting(sourcepath):
    return sourcepath.endswith(('.py', '.c'))

@click.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True))
def main(files):
    """Print contents of each file passed as argument."""

    files = [file for file in files if is_interesting(file)]
    for file_path in files:
        symbols = parse_path(file_path)
        img = render(symbols)
        if img is None:
            continue
        with tempfile.NamedTemporaryFile(suffix=".png", delete=True) as tmp:
            img.save(tmp.name)
            print(f'{symbols.path}: {symbols.num_lines} lines, {len(symbols.symbols)} symbols, size={img.size}')
            show(tmp.name)

if __name__ == '__main__':
    main()