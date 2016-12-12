# USAGE: pytest app/tests/test_spider.py 

import pytest
from django.core.management import call_command, CommandError
from django.utils.six import StringIO


def test_err_noargs():
    with pytest.raises(CommandError):
        call_command('spider')

# def test_err_noargs(self):
#     out = StringIO()
#     self.asscall_command('spider', stdout=out)
#     self.assertIn('Expected output', out.getvalue())
