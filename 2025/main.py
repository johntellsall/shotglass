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

# def insert(args):
#     for topdir in args:
#         path = Path(topdir) / 'APKBUILD'
#         info = parse(open(path))
#         print(info)

if __name__ == '__main__':
    show_summary(sys.argv[1:])
