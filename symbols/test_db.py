import pytest

import main
from state import queryall


@pytest.fixture(scope="module")
def test_con():
    con = main.raw_add_project(
        "../SOURCE/flask", is_testing=True, only_interesting=True
    )
    return con

def test_release(test_con):
    release_rows = queryall(test_con, sql='select * from release')
    releases = [dict(row) for row in release_rows]
    assert len(releases) >= 1
    assert releases[0]["label"] == "upstream/3.1.2"


def test_path(test_con):
    file_rows = queryall(test_con, sql='select * from file')
    files = [dict(row) for row in file_rows]
    assert len(files) >= 1
    myfile = files[0]
    assert myfile['path'] == 'src/flask/__init__.py'
    assert myfile['release'] == 'upstream/3.1.2'
    assert int(myfile['size_bytes']) > 1000


    # file_rows = queryall(con, sql='select * from file where path = "src/flask/app.py"')
    # item = dict(file_rows[0])
    # print('FILE:', item)
    # symbol_rows = queryall(con, sql='select * from symbol where path = "src/flask/app.py"')
    # item = dict(symbol_rows[0])
    # print('SYMBOL:', item)
