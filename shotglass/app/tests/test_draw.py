import pytest
from django.test import TestCase

from app import draw
from app import models


class TestDraw(TestCase):
    fixtures = ["diagram-min"]  # minimal

    def setUp(self):
        stub = models.SourceLine.objects.create(
            kind="k", length=3, line_number=2, name="name", path="path"
        )
        models.Skeleton.objects.update(sourceline=stub)

    def test_simple(self):
        grid = draw.SimpleDraw().draw(None)
        assert grid.last == (0, 2)
        assert grid.height == 8
        assert grid.width == 8


def test_add_color():
    diagram = [(0, "x", 1), (1, "y", 2)]
    assert list(draw.pal_add_color(diagram)) == [
        (0, 'x', 1, '#053061'), 
        (1, 'y', 2, '#2166AC')
        # (0, "x", 1, "#864747"),
        # (1, "y", 2, "#5dd3d7"),
    ]
