import datetime

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
