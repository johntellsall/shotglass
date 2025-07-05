from pathlib import Path
from symbols import parse_path

import click
import squarify
from PIL import Image, ImageDraw, ImageFont
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

def do_resize(img, rect, scale):
    """
    Resize the rendered image to fit inside the rectangle, maintaining aspect ratio
    """
    img_w, img_h = img.size
    width, height = rect
    rect_w, rect_h = int(width), int(height)
    scale_factor = min(rect_w / img_w, rect_h / img_h, scale)
    new_size = (max(1, int(img_w * scale_factor)), max(1, int(img_h * scale_factor)))
    resized_img = img.resize(new_size, Image.NEAREST)
    return resized_img


def label_files(symfiles, draw, rects):
    font_lg = ImageFont.load_default(size=24)
    font_sm = ImageFont.load_default(size=16)

    # label the larger files
    for i, symfile in enumerate(symfiles):
        if symfile.num_lines < 100:
            continue
        rect = rects[i]
        path = Path(symfile.path)
        label = path.name
        font = font_lg
        label_width = draw.textlength(label, font=font)
        if label_width > rect['dx'] - 10:
            print(f'{label} is too wide for rectangle {rect}')
            font = font_sm
            label_width = draw.textlength(label, font=font)
            if label_width > rect['dx'] - 10:
                print(f'{label} small too wide, skipping')
                continue
        draw.text((rect['x'] + 5, rect['y'] + 5), label, fill="black", font=font)


@click.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True))
def main(files):
    """Print contents of each file passed as argument."""
    width, height = 800, 600
    scale = 3

    files = [file for file in files if is_interesting(file)]
    symfiles = [parse_path(file_) for file_ in files]
    symfiles = [s for s in symfiles if s.num_lines >= 10]
    symfiles.sort(key=lambda s: s.num_lines, reverse=True)

    sizes = [s.num_lines for s in symfiles]
    sizes = squarify.normalize_sizes(sizes, width, height)
    rects = squarify.padded_squarify(sizes, 0, 0, width, height)
    
    image = Image.new("RGB", (width, height), color="gray")
    draw = ImageDraw.Draw(image)

    for i, symfile in enumerate(symfiles):
        img = render(symfile)
        if img is None:
            print(f"Skipping {symfile.path} due to insufficient lines.")
            continue
        
        # Draw a rectangle on the image
        rect = rects[i]
        shape = [rect['x'], rect['y'], rect['x'] + rect['dx'], rect['y'] + rect['dy']]
        draw.rectangle(shape, outline="black", fill="lightblue")

        img = do_resize(img, (rect['dx'], rect['dy']), scale)
        image.paste(img, (int(rect['x']), int(rect['y'])))

    label_files(symfiles, draw, rects)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=True) as tmp:
        image.save(tmp.name)
        show(tmp.name)


if __name__ == '__main__':
    main()