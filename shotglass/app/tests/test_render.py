import cProfile
import pstats
 
from django.test import TestCase
from pytest import mark

from app import grid, models, render


class AttrDict(dict):
    __getattr__ = dict.__getitem__

SYMBOLS = [
    AttrDict(symbol='logger', path='main.py', size='M', length=1),
    AttrDict(symbol='func1', path='main.py', size='L', length=2),
    AttrDict(symbol='func2', path='aux.py', size='S', length=3),
]


def get_arg(result):
    return [arg for pos,_symbol,arg in result]
def get_pos(result):
    return [pos for pos,_symbol,arg in result]


def test_add_color():
    diagram = [(0, 'x', 1), (1, 'y', 2)]
    assert list(render.add_color(diagram)) == [
        (0, 'x', 1, '#864747'), (1, 'y', 2, '#5dd3d7')]


def test_skeleton():
    symbols = list(SYMBOLS)

    result = list(render.make_skeleton(symbols, 'size', depth=None))
    assert get_pos(result) == [0, 1, 3]
    assert get_arg(result) == ['M', 'L', 'S']

    result = render.make_skeleton(symbols, 'length', depth=None)
    assert get_arg(result) == [1, 2, 3]


def test_skeleton_json():
    symbols = [
        AttrDict(symbol='log', path='main.py', tags_json='"cat"', length=1),
        AttrDict(symbol='func1', path='main.py', tags_json='"cat"', length=2),
        AttrDict(symbol='func2', path='aux.py', tags_json='"dog"', length=3),
    ]
    result = render.make_skeleton(symbols, 'tags_json', depth=1)
    assert get_arg(result) == ['c', 'c', 'd']

    result = render.make_skeleton(symbols, 'tags_json', depth=2)
    assert get_arg(result) == ['ca', 'ca', 'do']


# def test_draw():
#     # XX move to fixture
#     diagram = pickle.load(open('/tmp/diagram.pickle'))
#     mygrid = grid.TextGrid(1000, 1000)
#     diagram.draw(mygrid)


# PERFORMANCE TEST:
# py.test -s app/tests/test_render.py::TestDraw
#
# TODO: disable this except when explicitly called
class TestDraw(TestCase):
    fixtures = ['diagram-django']  # slow + useful
    fixtures = ['diagram-min'] # minimal

    def setUp(self):
        stub = models.SourceLine.objects.create(
            kind='k', length=3, line_number=2, name='name', path='path')
        models.DiagramSymbol.objects.update(sourceline=stub)

    def test_rawdraw(self):
        def rawdraw():
            diagram = render.Diagram.FromDB()
            mygrid = grid.Grid(None, None)
            diagram.draw(mygrid)

        prof_name = 'rawdraw-{}.prof'.format(self.fixtures[0])
        cProfile.runctx(
            rawdraw.func_code,  # pylint: disable=no-member
            globals=globals(), locals={},
            filename=prof_name)

        p = pstats.Stats(prof_name)
        p.strip_dirs().sort_stats('cumtime').print_stats(20)

