import os
from sqlmodel import create_engine

DEBUG = 'DEBUG' in os.environ



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

