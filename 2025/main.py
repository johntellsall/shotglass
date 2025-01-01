from pathlib import Path
from pprint import pprint
import sys
from parse import parse

def main(args):
    for topdir in args:
        print(topdir)
        path = Path(topdir) / 'APKBUILD'

        info = parse(open(path))
        pprint(info)
        print()

if __name__ == '__main__':
    main(sys.argv[1:])
