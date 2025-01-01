from pathlib import Path
from pprint import pprint
import sys
from parse import parse

def show_info(args):
    for topdir in args:
        print(topdir)
        path = Path(topdir) / 'APKBUILD'
        info = parse(open(path))
        pprint(info)
        print()

def show_summary(args):
    fields = ['pkgname', 'pkgver', 'pkgrel', 'len_install', 'len_parse_funcs', 'len_subpackages']
    print(fields)
    for topdir in args:
        path = Path(topdir) / 'APKBUILD'
        info = parse(open(path))
        #'pkgdesc'
        info['len_install'] = len(info.get('install', []))
        info['len_parse_funcs'] = len(info.get('_parse_functions', []))
        info['len_subpackages'] = len(info.get('subpackages', []))
        # print(list(zip(fields, [info.get(f, 'N/A') for f in fields])))
        print([info.get(f, 'N/A') for f in fields])

from model import SGAlpinePackage
from sqlmodel import Field, Session, SQLModel, create_engine

def insert(args):
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    engine = create_engine(sqlite_url, echo=True)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        for topdir in args:
            path = Path(topdir) / 'APKBUILD'
            info = parse(open(path))
            info = SGAlpinePackage.annotate(info)
            package = SGAlpinePackage(**info)
            session.add(package)
            session.commit()

    with Session(engine) as session:
        result = session.exec("SELECT COUNT(*) FROM sgalpinepackage")
        row_count = result.one()[0]
        print(f"Total rows in sgalpinepackage: {row_count}")

    # for topdir in args:
    #     path = Path(topdir) / 'APKBUILD'
    #     info = parse(open(path))
    #     info = SGAlpinePackage.annotate(info)
    #     package = SGAlpinePackage(**info)

if __name__ == '__main__':
    # show_summary(sys.argv[1:])
    insert(sys.argv[1:])
