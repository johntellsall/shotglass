from dataclasses import dataclass
from pathlib import Path
import re
import sys
from textwrap import fill

import rpack
from PIL import Image, ImageDraw, ImageFont


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


def make_rects(paths, max_width=None):
    sizes = {}
    
    for path in paths:
        name = Path(path).name
        with Image.open(path) as img:
            width, height = img.size
        sizes[name] = (width, height)

    rects = roughpack(sizes, max_width=max_width)
    rects = {rect.name: rect for rect in rects}
    return rects


def simplify(name):
    """
    strip version number and image suffix
    """
    pat = re.compile('[^-.]+')
    if m := pat.match(name):
        return m.group()
    return name


def main(paths):
    rects = make_rects(paths)
    bbox = rects.pop('BOUNDING-BOX')
    aspect = bbox.width / bbox.height
    print(f'Aspect ratio: {aspect:.2f}')

    overview_img = Image.new('RGB', (bbox.width, bbox.height), 'gray')
    draw = ImageDraw.Draw(overview_img)
    font = ImageFont.truetype("../fonts/ariblk.ttf", 24)

    for name, rect in rects.items():
        rstyle = dict(outline='green', fill='white')
        draw.rectangle([rect.x, rect.y, rect.x + rect.width, rect.y + rect.height], **rstyle)
        label = simplify(name)
        lstyle = dict(fill='black', font=font)
        draw.text((rect.x, rect.y), label, **lstyle)
    overview_img.save('overview.png')
  
    

if __name__=='__main__':
    main(sys.argv[1:])