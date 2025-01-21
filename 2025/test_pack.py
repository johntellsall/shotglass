from math import sqrt
from pathlib import Path
import rpack
import subprocess

# # Create a bunch of rectangles (width, height)
# >>> sizes = [(58, 206), (231, 176), (35, 113), (46, 109)]

# # Pack
# >>> positions = rpack.pack(sizes)

# # The result will be a list of (x, y) positions:
# >>> positions
# [(0, 0), (58, 0), (289, 0), (289, 113)]
import srcgrid

DATA = {
    'src/outpacket.c': 118,
 'src/pattern.c': 386,
 'src/poll.c': 125,
 'src/radv.c': 1030,
 'src/rfc1035.c': 2098,
}

def test_pack():
    names = list(DATA.keys())
    sizes_1d = [int(sqrt(count)) for count in DATA.values()]
    sizes = [(size, size) for size in sizes_1d]
    positions = rpack.pack(sizes)
    assert positions == [(64, 43), (45, 32), (64, 32), (45, 0), (0, 0)]
    assert names == ['src/outpacket.c', 'src/pattern.c', 'src/poll.c', 'src/radv.c', 'src/rfc1035.c']
    bbox = rpack.bbox_size(sizes, positions)
    assert bbox == (77, 53)
