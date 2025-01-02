from pathlib import Path
from pprint import pprint
import sys
from sqlmodel import select, delete, func, Field, Session, SQLModel, create_engine
from model import SGAlpinePackage
from parse import parse


DEBUG = False # True


def show_info(paths):
    for topdir in paths:
        print(topdir)
        path = Path(topdir) / 'APKBUILD'
        info = parse(open(path))
        pprint(info)
        print()

def show_summary(paths):
    fields = ['pkgname', 'pkgver', 'pkgrel', 'len_install', 'len_parse_funcs', 'len_subpackages']
    print(fields)
    for topdir in paths:
        path = Path(topdir) / 'APKBUILD'
        info = parse(open(path))
        #'pkgdesc'
        info['len_install'] = len(info.get('install', []))
        info['len_parse_funcs'] = len(info.get('_parse_functions', []))
        info['len_subpackages'] = len(info.get('subpackages', []))
        # print(list(zip(fields, [info.get(f, 'N/A') for f in fields])))
        print([info.get(f, 'N/A') for f in fields])


def get_engine():
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    engine = create_engine(sqlite_url, echo=DEBUG)
    return engine


def cmd_import(paths):
    engine = get_engine()

    # WARNING: Remove all existing SGAlpinePackage entries
    with Session(engine) as session:
        statement = delete(SGAlpinePackage)
        result = session.exec(statement)
        session.commit()
        # print(result.rowcount) -- num of deleted rows

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        statement = select(SGAlpinePackage)
        results = session.exec(statement)
        for package in results:
            print(package.__fields__.keys())

    with Session(engine) as session:
        for num,topdir in enumerate(paths):
            print(topdir)
            path = Path(topdir) / 'APKBUILD'
            info = parse(open(path))
            info = SGAlpinePackage.annotate(info)
            package = SGAlpinePackage(**info)
            session.add(package)
            # commit the first item to find errors more quickly
            if num == 0:
                session.commit()
                # SGAlpinePackage.model_fields()
                # query it and show fields
                # statement = select(SGAlpinePackage)
                # results = session.exec(statement)
                # for package in results:
                #     print(package.__fields__.keys())
        session.commit()

    with Session(engine) as session:
        count = session.scalar(select(func.count()).select_from(SGAlpinePackage))
        print(count)


def cmd_report(paths):
    engine = get_engine()
    with Session(engine) as session:
        query = select(SGAlpinePackage)
        query = query.where(SGAlpinePackage.pkgname.startswith('d'))
        rows = []
        results = session.exec(query)
        for package in results:
            rank = sum([package.sg_len_install, package.sg_len_parse_funcs, package.sg_len_subpackages])
            row = dict(package)
            row['_rank'] = rank
            rows.append(row)

        rows.sort(key=lambda row: row['_rank'], reverse=True)
        for row in rows:
            print(row['_rank'], row['pkgname'])


if __name__ == '__main__':
    cmdfunc = globals().get(f'cmd_{sys.argv[1]}')
    if not cmdfunc:
        sys.exit(f"Unknown command: {sys.argv[1]}")
    cmdfunc(sys.argv[2:])
    # show_summary(sys.argv[1:])
    # insert(sys.argv[1:])
    # report([])

