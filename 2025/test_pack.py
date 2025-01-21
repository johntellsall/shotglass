from math import sqrt
import rpack


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
