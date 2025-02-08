import sys


def main(paths):
    for path in paths:
        print(path)

if __name__=='__main__':
    main(sys.argv[1:])