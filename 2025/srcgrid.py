from dataclasses import dataclass
from math import sqrt
from operator import is_
from pathlib import Path
from pprint import pprint
import sys
import rpack
import subprocess
from PIL import Image, ImageDraw, ImageFont

# # Create a bunch of rectangles (width, height)
# >>> sizes = [(58, 206), (231, 176), (35, 113), (46, 109)]

# # Pack
# >>> positions = rpack.pack(sizes)

# # The result will be a list of (x, y) positions:
# >>> positions
# [(0, 0), (58, 0), (289, 0), (289, 113)]

# FIXME: handle other types of source code
def git_list_files(prefix):
    result = subprocess.run(['git', '-C', prefix, 'ls-files', '*.c', '*.py'], capture_output=True, text=True)
    return result.stdout.splitlines()

def count_lines(prefix, path):
    fullpath = Path(prefix) / path
    return sum(1 for line in fullpath.open())

def count_project(projdir):
    """
    Scan files in project directory, count lines in each source file.
    Return: dict with filename as key and line count as value
    - filename will have project prefix removed
    Example: 'src/pattern.c': 386
    """
    SUFFIXES = ['.c', '.py']
    is_git = (Path(projdir) / '.git').is_dir()
    if is_git:
        paths = list(git_list_files(projdir))
    else:
        paths = []
        for suffix in SUFFIXES:
            paths.extend(Path(projdir).rglob(f'*{suffix}'))
        paths = [str(path.relative_to(projdir)) for path in paths]
    count_dict = {path: count_lines(projdir, path) for path in paths}
    return count_dict


@dataclass
class Rect:
    x: int
    y: int
    width: int
    height: int
    name: str


def roughpack(data):
    """
    Given a list of filenames and line counts, pack them into a rectangle
    Returns a list of Rect objects, one for each rendered file
    """
    names = list(data.keys())
    # source file of 100 lines will be rendered as 10x10 square
    sizes_1d = [int(sqrt(count)) for count in data.values()]
    sizes = [(size, size) for size in sizes_1d]
    positions = rpack.pack(sizes)
    # assert positions == [(64, 43), (45, 32), (64, 32), (45, 0), (0, 0)]
    # assert names == ['src/outpacket.c', 'src/pattern.c', 'src/poll.c', 'src/radv.c', 'src/rfc1035.c']

    # calculate bounding box, store as special rect
    bbox = rpack.bbox_size(sizes, positions)
    yield Rect(0, 0, bbox[0], bbox[1], 'BOUNDING-BOX')

    for i in range(len(names)):
        x, y = positions[i]
        width, height = sizes[i]
        yield Rect(x, y, width, height, names[i])


def query_rect_sizes(proj_data):
    # ignore source under 100 lines
    def is_interesting(name, lines):
        return lines > 100 and not name.startswith('contrib/')
    proj_data = {k: v for k, v in proj_data.items() if is_interesting(k, v)}
    packed_rects = list(roughpack(proj_data))
    return packed_rects


def simplify(path):
    path = path.replace('src/', '')
    path = path.replace('.c', '') # FIXME:
    return path


def calc_stats(data):
    total_lines = sum(data.values())
    total_files = len(data)
    return {'total_lines': total_lines, 'total_files': total_files}


def render(projdir):
    assert Path(projdir).is_dir()
    proj_data = count_project(projdir)
    assert len(proj_data) > 0

    rects = query_rect_sizes(proj_data)
    boxdict = {rect.name: rect for rect in rects}

    bbox = boxdict.pop('BOUNDING-BOX')
    scale = 1
    size = (bbox.width * scale, bbox.height * scale)
    image = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("../fonts/ariblk.ttf", 12)

    for rect in rects:
        if rect.name == 'BOUNDING-BOX':
            continue
        draw.rectangle([rect.x, rect.y, rect.x + rect.width, rect.y + rect.height], outline='black')
        label = simplify(rect.name)
        (_, _, bbottom, bright) = font.getbbox(text=label)
        if bright > rect.width or bbottom > rect.height:
            print(f'- {label} does not fit in {rect.width}x{rect.height}')
            continue
        draw.text((rect.x, rect.y), label, fill='black', font=font)

    image.save('output.png')
    print(projdir)
    pprint(calc_stats(proj_data))
    print(f'size: {size}')
    

if __name__ == '__main__':
    render(sys.argv[1])
