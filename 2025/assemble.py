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


def main(paths):
    projects = {}
    
    for path in paths:
        name = Path(path).name
        with Image.open(path) as img:
            width, height = img.size
        info = dict(size=(width, height), name=name)
        projects[name] = info

    sizes = [p['size'] for p in projects.values()]
    positions = rpack.pack(sizes)
    assert 0, positions

if __name__=='__main__':
    main(sys.argv[1:])