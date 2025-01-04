import os
from sqlmodel import create_engine

DEBUG = 'DEBUG' in os.environ

def get_engine():
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    engine = create_engine(sqlite_url, echo=DEBUG)
    return engine
