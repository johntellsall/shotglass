# shotlib.py


import json
import logging
import re
import subprocess
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

import git


def get_db(temporary=False):
    path = ":memory:" if temporary else "main.db"
    con = sqlite3.connect(path)
    cur = con.cursor()
    return con, cur


def select1(db, sql):
    db.execute(sql)
    return db.fetchone()[0]


def selectall(db, sql):
    db.execute(sql)
    return db.fetchall()


def show_details(db):
    print("DETAILS:")
    print("-- files")
    for row in db.execute("select * from files order by 1 limit 3"):
        print(row)
    print("-- symbols")
    for row in db.execute("select * from symbols order by 1 limit 3"):
        print(row)
