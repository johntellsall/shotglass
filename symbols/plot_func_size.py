import logging
import state
from PIL import Image
from PIL import ImageDraw
import math

logging.basicConfig(format="%(asctime)-15s %(message)s", level=logging.INFO)

FUNC_SIZE = """
select s.name,
    (s.line_end - s.line_start + 1) as line_count,
    s.path
from symbol s
where line_count > 1
order by line_count desc, s.name
"""

def make_image():
    img = Image.new('RGB', (500, 500), color='green')
    return img

def main():
    limit = False

    db = state.get_db()
    symbols = state.queryall(db, sql=FUNC_SIZE)
    if limit:
        symbols = symbols[:15]
    symbols = [dict(sym) for sym in symbols]

    style = dict(outline="black")
    label_style = dict(fill="white")

    img = make_image()
    draw = ImageDraw.Draw(img)
    max_r = min(img.size) // 2 - 1
    scale = max_r / 4
    cx, cy = img.width // 2, img.height // 2
    print(f'Drawing {len(symbols)} functions')
    line_count_set = set(sym['line_count'] for sym in symbols)

    for count in line_count_set:
        r = scale * math.log10(count)
        print(f'{count} scaled r={r}')
        draw.circle(xy=(cx, cy), radius=r, **style)

    for count in [10, 50, 100, 200, 1000]:
        r = scale * math.log10(count)
        label = str(count)
        draw.text((cx, cy + r), label, **label_style)
    img.save('pil_example.png')
    print('Image saved as pil_example.png')

if __name__ == "__main__":
    main()