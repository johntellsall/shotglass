import pytest
from django.test import TestCase

from app import grid, render
from app.models import SourceLine


class AttrDict(dict):
    __getattr__ = dict.__getitem__


# http://stackoverflow.com/a/11924754/143880
def is_subset(d1, obj):
    d2 = vars(obj)
    return set(d1.items()).issubset(set(d2.items()))


@pytest.mark.skip("OLD")
@pytest.mark.django_db
def test_make_skeleton():
    symbols = [
        SourceLine(path="a.py", length=3),
        SourceLine(path="a.py", length=3),
        SourceLine(path="b.py", length=3),
    ]
    for sym in symbols:
        sym.line_number = -1
    SourceLine.objects.bulk_create(symbols)

    skeleton = list(render.make_skeleton(SourceLine.objects.all()))

    result = [(sk.position, sk.x, sk.y) for sk in skeleton]

    # X BUG: should be two-pixel "smudge" after a.py ends
    assert result == [(0, 0, 0), (3, 0, 1), (6, 1, 3)]
