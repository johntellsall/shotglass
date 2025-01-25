import os
from pathlib import Path
from sqlmodel import Session, create_engine, text

DEBUG = 'DEBUG' in os.environ



def equery(arg, engine=None):
    if engine is None:
        engine = get_engine()

    if 'SELECT' in arg:
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

