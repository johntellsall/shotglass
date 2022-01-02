import datetime
from pathlib import Path

import release


def test_release():
    rel = release.Release("mysql-3.23.22-beta", "1234-05-06")
    print(vars(rel))
    assert vars(rel) == {
        "raw_label": "mysql-3.23.22-beta",
        "raw_date": "1234-05-06",
        "majormin": "3.23",
        "pre": "mysql-",
        "post": ".22-beta",
        "date": datetime.datetime(1234, 5, 6, 0, 0),
    }


def test_get_git_date():
    name = "src/flask/signals.py"
    git_date = release.get_git_date(Path("../SOURCE/flask"), name)
    assert git_date.year > 1970
