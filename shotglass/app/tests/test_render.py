from app import render


class AttrDict(dict):
    __getattr__ = dict.__getitem__

SYMBOLS = [
    AttrDict(symbol='logger', path='main.py', size='M', length=1),
    AttrDict(symbol='func1', path='main.py', size='L', length=2),
    AttrDict(symbol='func2', path='aux.py', size='S', length=3),
]


def get_pos_arg(results):
    return [(pos,arg) for pos,_symbol,arg in results]


def test_skeleton():
    symbols = list(SYMBOLS)

    result = render.make_skeleton(symbols, 'size', depth=None)
    assert get_pos_arg(result) == [(0, 'M'), (2, 'L'), (5, 'S')]

    result = render.make_skeleton(symbols, 'length', depth=None)
    assert get_pos_arg(result) == [(0, 1), (2, 2), (5, 3)]


def test_skeleton_json():
    symbols = [
        AttrDict(symbol='log', path='main.py', tags_json='"cat"', length=1),
        AttrDict(symbol='func1', path='main.py', tags_json='"cat"', length=2),
        AttrDict(symbol='func2', path='aux.py', tags_json='"dog"', length=3),
    ]
    result = render.make_skeleton(symbols, 'tags_json', depth=1)
    assert get_pos_arg(result) == [(0, 'c'), (2, 'c'), (5, 'd')]

    result = render.make_skeleton(symbols, 'tags_json', depth=2)
    assert get_pos_arg(result) == [(0, 'ca'), (2, 'ca'), (5, 'do')]
