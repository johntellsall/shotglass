import contextlib
import sqlite3
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np


def get_data():
    def parse_ymd(datestr):
        return datetime.strptime(datestr, "%Y-%m-%d")

    db_name = "timeline.db"
    with contextlib.closing(sqlite3.connect(db_name)) as con:
        cursor = con.execute("select name,date from timeline")
        data = cursor.fetchall()
    names = [item[0] for item in data]
    dates = [parse_ymd(item[1].split()[0]) for item in data]
    return names, dates


def do_plot(data):
    names, dates = data

    # Choose some nice levels
    levels = np.tile([-5, 5, -3, 3, -1, 1], int(np.ceil(len(dates) / 6)))[: len(dates)]

    # Create figure and plot a stem plot with the date
    fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
    ax.set(title="Matplotlib release dates")

    ax.vlines(dates, 0, levels, color="tab:red")  # The vertical stems.
    ax.plot(
        dates, np.zeros_like(dates), "-o", color="k", markerfacecolor="w"
    )  # Baseline and markers on it.

    # annotate: put release at end of each stem
    for rdate, rlevel, rname in zip(dates, levels, names):
        ax.annotate(
            rname,
            xy=(rdate, rlevel),
            xytext=(-3, np.sign(rlevel) * 3),
            textcoords="offset points",
            horizontalalignment="right",
            verticalalignment="bottom" if rlevel > 0 else "top",
        )

    # format xaxis with 4 month intervals
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

    # remove y axis and spines
    ax.yaxis.set_visible(False)
    ax.spines[["left", "top", "right"]].set_visible(False)

    ax.margins(y=0.1)

    return fig, plt


def main():
    data = get_data()
    fig, plt = do_plot(data)

    # save to file
    name = "timeline"
    img_name = f"{name}.png"
    fig.savefig(img_name, dpi=150)
    print(f"wrote to {img_name}")
    # plt.show()


if __name__ == "__main__":
    main()
