import os

import git
import pytest

try:
    import sg2
except ImportError:
    sg2 = 0


@pytest.mark.skipif(not sg2, reason="requires sg2")
def test_zoot():
    test_git = git.Repo(os.path.expanduser("~/src/iproute2")).git

    diff_text = test_git.diff(sg2.range_1, stat=True)
    diff_iter = sg2.parse_diff_changes(diff_text)
    all_matches = [x.groups() for x in diff_iter]
    assert all_matches[0] == (u"Makefile", u"2")
    assert all_matches[10] == ("man/man8/tc-stab.8", "163")
