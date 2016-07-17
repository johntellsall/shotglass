import os

import git

import sg2


test_git = git.Repo(os.path.expanduser('~/src/iproute2')).git


def test_zoot():
    diff_iter = sg2.zoot(test_git, myrange=sg2.range_1)
    all_matches = [x.groups() for x in diff_iter]
    assert all_matches[0] == (u'Makefile', u'2')
    assert all_matches[10] == ('man/man8/tc-stab.8', '163')
