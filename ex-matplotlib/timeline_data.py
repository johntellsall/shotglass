import contextlib
import sqlite3
from datetime import datetime


def get_rawdata():
    names = [
        "v2.2.4",
        "v3.0.3",
        "v3.0.2",
        "v3.0.1",
        "v3.0.0",
        "v2.2.3",
        "v2.2.2",
        "v2.2.1",
        "v2.2.0",
        "v2.1.2",
        "v2.1.1",
        "v2.1.0",
        "v2.0.2",
        "v2.0.1",
        "v2.0.0",
        "v1.5.3",
        "v1.5.2",
        "v1.5.1",
        "v1.5.0",
        "v1.4.3",
        "v1.4.2",
        "v1.4.1",
        "v1.4.0",
    ]

    dates = [
        "2019-02-26",
        "2019-02-26",
        "2018-11-10",
        "2018-11-10",
        "2018-09-18",
        "2018-08-10",
        "2018-03-17",
        "2018-03-16",
        "2018-03-06",
        "2018-01-18",
        "2017-12-10",
        "2017-10-07",
        "2017-05-10",
        "2017-05-02",
        "2017-01-17",
        "2016-09-09",
        "2016-07-03",
        "2016-01-10",
        "2015-10-29",
        "2015-02-16",
        "2014-10-26",
        "2014-10-18",
        "2014-08-26",
    ]

    # Convert date strings (e.g. 2014-10-18) to datetime
    dates = [datetime.strptime(d, "%Y-%m-%d") for d in dates]
    return {"names": names, "dates": dates}


def make_db():
    raw = get_rawdata()
    db_name = "timeline.db"
    with contextlib.closing(sqlite3.connect(db_name)) as con:
        con.execute("drop table if exists timeline")
        con.execute("create table timeline (name text, date text)")
        data_namesdates = list(zip(raw["names"], raw["dates"]))
        con.executemany("insert into timeline values (?, ?)", data_namesdates)
        con.commit()

    print(f"{db_name}: written")

    with contextlib.closing(sqlite3.connect(db_name)) as con:
        cursor = con.execute("select * from timeline limit 1")
        sel_data = cursor.fetchall()
    print(f"{db_name}: read: {sel_data}")


def main():
    make_db()


if __name__ == "__main__":
    main()
