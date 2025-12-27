import main
from state import queryall

def test_raw_add_project():
    con = main.raw_add_project(
        "../SOURCE/flask", is_testing=True, only_interesting=True
    )
    release_rows = queryall(con, sql='select * from release')
    releases = [dict(row) for row in release_rows]
    assert len(releases) >= 1
    assert releases[0]["label"] == "upstream/3.1.2"
    # file_rows = queryall(con, sql='select * from file where path = "src/flask/app.py"')
    # item = dict(file_rows[0])
    # print('FILE:', item)
    # symbol_rows = queryall(con, sql='select * from symbol where path = "src/flask/app.py"')
    # item = dict(symbol_rows[0])
    # print('SYMBOL:', item)
