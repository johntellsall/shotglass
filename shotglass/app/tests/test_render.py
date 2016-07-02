import cProfile
import pstats
 
from django.test import TestCase
import pytest

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
    assert list(render.jm_add_color(diagram)) == [
        (0, 'x', 1, '#864747'), (1, 'y', 2, '#5dd3d7')]


@pytest.mark.django_db
def test_render():
    models.SourceLine.objects.bulk_create([
        models.SourceLine(
        name='apple', path='a.py', line_number=1, kind='', length=1),
        models.SourceLine(
        name='bat', path='a.py', line_number=3, kind='', length=2),
        models.SourceLine(
        name='camel', path='b.py', line_number=2, kind='', length=1)])

    def abc_color(sym):
        return sym.name[0]

    symbols = models.SourceLine.objects.all()
    diagram = render.Diagram()
    diagram.render(
        symbols, argname=None, depth=None, 
        color_func=abc_color)
    
    bits = [(ds.position, ds.color) for ds in diagram]
    assert bits == [(0, 'a'), (1, 'b'), (3, 'c')]


def test_skeleton():
    symbols = list(SYMBOLS)

    result = list(render.make_skeleton(symbols, 'size', depth=None))
    assert get_pos(result) == [0, 1, 3]
    assert get_arg(result) == ['M', 'L', 'S']

    result = render.make_skeleton(symbols, 'length', depth=None)
    assert get_arg(result) == [1, 2, 3]


class TestDraw(TestCase):
    fixtures = ['diagram-min'] # minimal

    def setUp(self):
        stub = models.SourceLine.objects.create(
            kind='k', length=3, line_number=2, name='name', path='path')
        models.DiagramSymbol.objects.update(sourceline=stub)

    def test_simple(self):
        grid = render.SimpleDraw().draw(None)
        self.assertDictContainsSubset(
            {'last': (0, 2), 'height': 8, 'width': 8},
            actual=vars(grid))


# PERFORMANCE TEST:
# py.test -s app/tests/test_render.py::TestDraw
#
# TODO: disable this except when explicitly called
@pytest.mark.skip(reason="performance test only")
class ProfileDraw(TestCase):
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

