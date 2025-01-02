import os
from sqlmodel import select, delete, func, Field, Session, SQLModel, create_engine

DEBUG = os.environ.has_key('DEBUG')

def get_engine():
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    engine = create_engine(sqlite_url, echo=DEBUG)
    return engine
