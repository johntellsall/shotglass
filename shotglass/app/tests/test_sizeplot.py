# TIMING
# python -m cProfile -o profile $(which pytest) app/tests/test_sizeplot.py

from django import test

import pytest

from app.management.commands import sizeplot

if 0:
    # TODO: use Django fixture w/ Pytest
    @pytest.mark.django_db(transaction=False)
    def test1():
        sizeplot.Command().render_project("redis-2.8.4")


class Test1(test.TestCase):
    fixtures = ["redis.yaml"]

    def test1(self):
        sizeplot.Command().render_project("redis-2.8.4")
