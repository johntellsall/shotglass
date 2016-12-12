# USAGE: pytest app/tests/test_spider.py 

import os
import sys

import pytest
from django.core.management import call_command, CommandError
from django.utils.six import StringIO


TEST_PATH = os.path.realpath(__file__)

# TODO: write images to temp path
# TODO: verify images

def test_err_noargs():
    with pytest.raises(CommandError):
        call_command('spider')


def test_blocks():
    out = StringIO()
    call_command('spider', TEST_PATH, style='blocks', stdout=out)
    assert out.getvalue() == ''


def test_source():
    out = StringIO()
    call_command('spider', TEST_PATH, style='source', stdout=out)
    assert out.getvalue() == ''
