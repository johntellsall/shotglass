from app import render


class AttrDict(dict):
    __getattr__ = dict.__getitem__

SYMBOLS = [
    AttrDict(symbol='proc', path='main.py', size='M', length=12),
    AttrDict(symbol='run', path='main.py', size='L', length=23),
    AttrDict(symbol='aux', path='aux.py', size='S', length=34),
]


def get_pos_arg(results):
    return [(pos,arg) for pos,_,arg in results]


def test_skeleton():
    symbols = list(SYMBOLS)

    result = render.make_skeleton(symbols, 'size', depth=None)
    assert get_pos_arg(result) == [(0, 'M'), (13, 'L'), (37, 'S')]

    result = render.make_skeleton(symbols, 'length', depth=None)
    assert get_pos_arg(result) ==  [(0, 12), (13, 23), (37, 34)]


def test_skeleton_json():
    symbols = [
        AttrDict(symbol='proc', path='main.py', tags_json='"cat"', length=12),
        AttrDict(symbol='run', path='main.py', tags_json='"cat"', length=23),
        AttrDict(symbol='aux', path='aux.py', tags_json='"dog"', length=34),
    ]
    result = render.make_skeleton(symbols, 'tags_json', depth=1)
    assert get_pos_arg(result) == [(0, 'c'), (13, 'c'), (37, 'd')]

    result = render.make_skeleton(symbols, 'tags_json', depth=2)
    assert get_pos_arg(result) == [(0, 'ca'), (13, 'ca'), (37, 'do')]
