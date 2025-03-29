from collections import namedtuple
from distutils.version import StrictVersion
import os
import random
from pathlib import Path
import re
import subprocess
from sqlmodel import Session, create_engine, text

DEBUG = 'DEBUG' in os.environ


def cmp_version(verstring):
    verstring = verstring.split('-')[0]
    return StrictVersion(verstring)

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

def namedtuple_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    cls = namedtuple("Row", fields)
    return cls._make(row)

# TODO: support "?" args
def OLDequery(arg, engine=None):
    if engine is None:
        engine = get_engine()

    if 'SELECT' in arg or 'select' in arg:
        query = arg
    else:
        # get SQL from file
        query = Path(arg).read_text()
        # strip header
        # TODO: strip footer
        select_index = query.upper().index("SELECT ")
        if select_index >= 0:
            query = query[select_index:]
        else:
            raise ValueError("No SELECT in query file")

    query = text(query)

    with Session(engine) as session:
        return session.exec(query).all()


# TODO: support "?" args
def equery(arg, engine=None):
    if engine is None:
        engine = get_engine()

    if 'SELECT' in arg or 'select' in arg:
        query = arg
    else:
        # get SQL from file
        query = Path(arg).read_text()
        # strip header
        # TODO: strip footer
        select_index = query.upper().index("SELECT ")
        if select_index >= 0:
            query = query[select_index:]
        else:
            raise ValueError("No SELECT in query file")

    query = text(query)

    with Session(engine) as session:
        result = session.exec(query).all()
    
    # FIXME: use formal method
    # if asdict:
    #     return [row._asdict() for row in result]
    return result


def equery1(*args, **kwargs):
    res = equery(*args, **kwargs)
    return res[0][0]

def equery_col(*args, **kwargs):
    "return first column of data"
    res = equery(*args, **kwargs)
    return [row[0] for row in res]


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


def savefig(plt, myfile):
    imgpath = Path(myfile).with_suffix('.png')
    plt.savefig(imgpath)

    pagepath = imgpath.with_suffix('.html')
    title = Path(myfile).name
    imagename = imgpath.name
    # NOTE: add cache buster
    imagename = f"{imagename}?{random.random()}"
    with open(pagepath, 'w') as f:
        f.write(PAGE.format(title=title, imagename=imagename))
    return dict(imgpath=imgpath, pagepath=pagepath)

PAGE = '''
<html>
<head>
    <title>{title}</title>
    <meta http-equiv="refresh" content="5" />
</head>
<body>
    <img src="{imagename}">
</body>
</html>
'''
