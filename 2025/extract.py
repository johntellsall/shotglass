import os
from pathlib import Path
from pprint import pprint
import sys
from sqlmodel import select, delete, func, Field, Session, SQLModel, create_engine
from model import SGAlpinePackage
from parse import parse
from lib import get_engine
from sqlalchemy.exc import OperationalError


def extract(paths):
    engine = get_engine()

    # WARNING: Remove all existing SGAlpinePackage entries
    try:
        with Session(engine) as session:
            statement = delete(SGAlpinePackage)
            session.exec(statement)
            session.commit()
    except OperationalError as e:
        print(f"OperationalError: {e}") # FIXME:

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        for num,topdir in enumerate(paths):
            dirname = Path(topdir).name
            if (num % 10 == 1):
                print(dirname, end=' ')
            path = Path(topdir) / 'APKBUILD'
            info = parse(open(path), label=path)
            info = SGAlpinePackage.annotate(info)
            package = SGAlpinePackage(**info)
            session.add(package)
            # commit the first item to find errors more quickly
            if num == 0:
                session.commit()

        session.commit()
        print()

    with Session(engine) as session:
        count = session.scalar(select(func.count()).select_from(SGAlpinePackage))
        print(f"Total packages: {count}")
