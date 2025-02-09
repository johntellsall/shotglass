from dataclasses import dataclass
from pathlib import Path
import sys

import rpack
from PIL import Image


# def render(projdir):
#     assert Path(projdir).is_dir()
#     proj_data = count_project(projdir)
#     assert len(proj_data) > 0

#     rects = query_rect_sizes(proj_data)
#     boxdict = {rect.name: rect for rect in rects}

#     bbox = boxdict.pop('BOUNDING-BOX')
#     scale = 1
#     size = (bbox.width * scale, bbox.height * scale)
#     image = Image.new('RGB', size, 'white')
#     draw = ImageDraw.Draw(image)
#     font = ImageFont.truetype("../fonts/ariblk.ttf", 12)

#     for rect in rects:
#         if rect.name == 'BOUNDING-BOX':
#             continue
#         draw.rectangle([rect.x, rect.y, rect.x + rect.width, rect.y + rect.height], outline='black')
#         label = simplify(rect.name)
#         (_, _, bbottom, bright) = font.getbbox(text=label)
#         if bright > rect.width or bbottom > rect.height:
#             print(f'- {label} does not fit in {rect.width}x{rect.height}')
#             continue
#         draw.text((rect.x, rect.y), label, fill='black', font=font)

#     return image


@dataclass
class Rect:
    x: int
    y: int
    width: int
    height: int
    name: str


def roughpack(data, max_width=None):
    """
    Given a list of filenames and rectangle sizes, pack them into a new large rectangle
    Returns a list of Rect objects, one for each rendered file
    - also includes a special Rect object for the bounding box
    - "position" is the lower-left corner of the rectangle
    """
    names = list(data.keys())
    sizes = list(data.values())
    positions = rpack.pack(sizes, max_width=max_width)

    # calculate bounding box, store as special rect
    bbox = rpack.bbox_size(sizes, positions)
    yield Rect(0, 0, bbox[0], bbox[1], 'BOUNDING-BOX')

    for i in range(len(names)):
        x, y = positions[i]
        width, height = sizes[i]
        yield Rect(x, y, width, height, names[i])


def make_rects(paths):
    sizes = {}
    
    for path in paths:
        name = Path(path).name
        with Image.open(path) as img:
            width, height = img.size
        sizes[name] = (width, height)

    rects = roughpack(sizes, max_width=600)
    rects = {rect.name: rect for rect in rects}
    return rects


def main(paths):
    rects = make_rects(paths)
    bbox = rects['BOUNDING-BOX']
    aspect = bbox.width / bbox.height
    print(f'Aspect ratio: {aspect:.2f}')
    assert 0, rects

if __name__=='__main__':
    main(sys.argv[1:])