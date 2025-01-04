import os
from pathlib import Path
from pprint import pprint
import sys
from sqlmodel import select, delete, func, Field, Session, SQLModel, create_engine
from model import SGAlpinePackage
from parse import parse
from lib import get_engine
import render
import extract


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


def cmd_import(paths):
    extract.extract(paths, release=os.environ['RELEASE'])
                    

# def cmd_report(paths):
#     limit = 'LIMIT' in os.environ
#     render.render1(limit)

def cmd_table(paths):
    print(render.format_html_table())

def cmd_extract2(paths):
    print(extract.extract2())


def cmd_popcon(paths):
    print(render.report_popcon())


if __name__ == '__main__':
    cmdfunc = globals().get(f'cmd_{sys.argv[1]}')
    if not cmdfunc:
        sys.exit(f"Unknown command: {sys.argv[1]}")
    cmdfunc(sys.argv[2:])
    # show_summary(sys.argv[1:])
    # insert(sys.argv[1:])
    # report([])

