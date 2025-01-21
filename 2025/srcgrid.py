from dataclasses import dataclass
from math import sqrt
from pathlib import Path
import pprint
import rpack
import subprocess
from PIL import Image, ImageDraw

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

def count_project(prefix):
    prefix = '../SOURCE/dnsmasq'
    paths = list(git_list_files(prefix))
    count_dict = {path: count_lines(prefix, path) for path in paths}
    return count_dict

@dataclass
class Rect:
    x: int
    y: int
    width: int
    height: int
    name: str

def roughpack(data):
    names = list(data.keys())
    sizes_1d = [int(sqrt(count)) for count in data.values()]
    sizes = [(size, size) for size in sizes_1d]
    positions = rpack.pack(sizes)
    # assert positions == [(64, 43), (45, 32), (64, 32), (45, 0), (0, 0)]
    # assert names == ['src/outpacket.c', 'src/pattern.c', 'src/poll.c', 'src/radv.c', 'src/rfc1035.c']
    bbox = rpack.bbox_size(sizes, positions)
    yield Rect(0, 0, bbox[0], bbox[1], 'BOUNDING-BOX')

    for i in range(len(names)):
        x, y = positions[i]
        width, height = sizes[i]
        yield Rect(x, y, width, height, names[i])


def query_rect_sizes(projdir):
    proj_data = count_project('../SOURCE/dnsmasq')
    # ignore source under 100 lines
    def is_interesting(name, lines):
        return lines > 100 and not name.startswith('contrib/')
    proj_data = {k: v for k, v in proj_data.items() if is_interesting(k, v)}
    packed_rects = list(roughpack(proj_data))
    return packed_rects


def render(projdir):
    rects = query_rect_sizes(projdir)
    boxdict = {rect.name: rect for rect in rects}

    bbox = boxdict.pop('BOUNDING-BOX')
    image = Image.new('RGB', (bbox.width, bbox.height), 'white')
    draw = ImageDraw.Draw(image)

    for rect in rects:
        draw.rectangle([rect.x, rect.y, rect.x + rect.width, rect.y + rect.height], outline='black')
        draw.text((rect.x, rect.y), rect.name, fill='black')

    image.save('output.png')
    

if __name__ == '__main__':
    render('../SOURCE/dnsmasq')
