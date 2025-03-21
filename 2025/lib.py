import os
from pathlib import Path
import re
import subprocess
import sys
from sqlmodel import Session, create_engine, text

DEBUG = 'DEBUG' in os.environ


def equery(arg, engine=None):
    if engine is None:
        engine = get_engine()

    if 'SELECT' in arg or 'select' in arg:
        query = arg
    else:
        # get SQL from file
        query = Path(arg).read_text()
        # strip header
        # FIXME: support lowercase
        select_index = query.index("SELECT ")
        if select_index >= 0:
            query = query[select_index:]
        else:
            raise ValueError("No SELECT in query file")

    query = text(query)

    with Session(engine) as session:
        return session.exec(query).all()


def equery1(*args, **kwargs):
    res = equery(*args, **kwargs)
    return res[0][0]


def format_html_row(row):
    middle = ''.join(f"<td>{value}</td>" for value in row)
    return f"<tr>{middle}</tr>"


def format_html_table(table_data):
    html = ['<table>']
    html += [format_html_row(row) for row in table_data]
    html += ['</table>']
    return '\n'.join(html)


def get_engine():
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    engine = create_engine(sqlite_url, echo=DEBUG)
    return engine


def git_checkout(branch):
    # FIXME: "git sparse-checkout init"
    # NOTE: "git reset --hard HEAD"?
    checkout_cmd = ["git", "-C", "aports", "checkout", "--quiet", f"remotes/origin/{branch}"]
    _result = subprocess.run(checkout_cmd, capture_output=True, text=True, check=True)
    # NOTE: abort if warning on stderr?
    # if result.returncode != 0: # FIXME: more here
    #     print(f"Failed to checkout branch {branch}: {result.stderr}", file=sys.stderr)
    #     raise ValueError(f"Failed to checkout branch {branch}")


def git_list_branches():
    cmd = ["git", "-C", "aports", "branch", "-a"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    releases = re.compile(r'remotes/origin/(\d+\.\d+-stable)').findall(result.stdout)
    # FIXME:
    if 1:
        releases = [rel for rel in releases if rel.startswith('3.')]
        return releases
    return releases

