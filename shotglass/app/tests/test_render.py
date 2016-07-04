import pytest
from django.test import TestCase

from app import grid, render
from app.models import SourceLine


class AttrDict(dict):
    __getattr__ = dict.__getitem__

SYMBOLS = [
    AttrDict(symbol='logger', path='main.py', size='M', length=1),
    AttrDict(symbol='func1', path='main.py', size='L', length=2),
    AttrDict(symbol='func2', path='aux.py', size='S', length=3),
]


def get_arg(result):
    return [args[2] for args in result]
def get_pos(result):
    return [args[0] for args in result]

# http://stackoverflow.com/a/11924754/143880
def is_subset(d1, obj):
    d2 = vars(obj)
    return set(d1.items()).issubset(set(d2.items()))


def test_skeleton():
    symbols = list(SYMBOLS)

    result = list(render.make_skeleton(symbols, 'size', depth=None))
    assert get_pos(result) == [0, 1, 3]
    assert get_arg(result) == ['M', 'L', 'S']

    result = render.make_skeleton(symbols, 'length', depth=None)
    assert get_arg(result) == [1, 2, 3]


@pytest.mark.django_db
def test_dsymbols():
    SourceLine.objects.bulk_create([
        SourceLine(
        name='apple', path='a.py', line_number=1, kind='', length=1),
        SourceLine(
        name='bat', path='a.py', line_number=3, kind='', length=2),
        SourceLine(
        name='camel', path='b.py', line_number=2, kind='', length=1)])

    dsymbols = list(render.make_dsymbols(
        SourceLine.objects.all(), None, None))
    
    assert is_subset({'x': 0, 'y': 0, 'position': 0}, 
        dsymbols[0])
    assert is_subset({'x': 1, 'y': 0, 'position': 1},
        dsymbols[1])
    assert is_subset({'x': 0, 'y': 1, 'position': 3},
        dsymbols[2])
    assert len(dsymbols) == 3
