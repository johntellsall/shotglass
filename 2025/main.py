import os
from pathlib import Path
from pprint import pprint
import sys
from parse import parse
import render
import r_grid
import r_scatter
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
    """
    import Alpine packages
    - 'aports' directory)
    - X: set env RELEASE, example RELEASE=3.19-stable python3 -m main import aports
    """
    # TODO: `git log -1` to get the release?
    extract.extract(paths, release=os.environ['RELEASE'])
                    

def cmd_table(paths):
    print(render.format_html_table())

def cmd_extract2(paths):
    extract.extract2(paths)


def cmd_popcon(paths):
    print(render.report_popcon())

def cmd_popcon2(paths):
    print(render.report_popcon2())

def cmd_popcon3(paths):
    print(render.report_popcon3())

def cmd_popcon4(paths):
    print(render.report_popcon4())

def cmd_extract_popcon(paths):
    print(extract.extract_popcon())

def cmd_grid(paths):
    print(r_grid.grid())

def cmd_scatter(paths):
    print(r_scatter.scatter())


if __name__ == '__main__':
    cmdfunc = globals().get(f'cmd_{sys.argv[1]}')
    if not cmdfunc:
        sys.exit(f"Unknown command: {sys.argv[1]}")
    cmdfunc(sys.argv[2:])

