# test_scan_github_releases.py
# NOTE: this is very tiny test, add more when needed

import sqlite3
import os

import pytest

import scan_github_releases as scan


@pytest.mark.skipif(not os.environ.get('GITHUB_TOKEN'), reason="GITHUB_TOKEN not set")
def test_main():
    "ensure main at least tries to open the database"
    dbpath = ":memory:"
    pytest.raises(sqlite3.OperationalError, scan.main, dbpath)
