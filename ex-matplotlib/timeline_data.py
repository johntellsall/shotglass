import contextlib
import json
import sqlite3
import urllib.request
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


def get_github_data():

    # Try to fetch a list of Matplotlib releases and their dates
    # from https://api.github.com/repos/matplotlib/matplotlib/releases

    url = "https://api.github.com/repos/matplotlib/matplotlib/releases"
    url += "?per_page=100"
    data = json.loads(urllib.request.urlopen(url).read().decode())

    dates = []
    names = []
    for item in data:
        if "rc" not in item["tag_name"] and "b" not in item["tag_name"]:
            dates.append(item["published_at"].split("T")[0])
            names.append(item["tag_name"])

    # Convert date strings (e.g. 2014-10-18) to datetime
    dates = [datetime.strptime(d, "%Y-%m-%d") for d in dates]
    return {"names": names, "dates": dates}


def summarize(data):
    print(f"Number of releases: {len(data['names'])}")
    releases = data["names"][0], data["names"][-1]
    print(f"Release range: {releases[0]} {releases[-1]}")
    dates = data['dates'][0], data['dates'][-1]
    print(f"Release date range: {dates[0].date()} {dates[-1].date()}")


def make_db(data):
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
    # data = get_rawdata()
    data = get_github_data()
    summarize(data)
    # make_db(raw)


if __name__ == "__main__":
    main()
