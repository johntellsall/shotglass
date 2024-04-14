# shotglass.py -- count source lines, render simply

import glob
import sys
from itertools import filterfalse, islice

SOURCE_EXTENSIONS = ('.py', '.c', '.cpp')

# FIXME: make configurable
def is_source(path):
    return path.endswith(SOURCE_EXTENSIONS)

# FIXME: make configurable
def is_test(path):
    return '/test' in path

# FIXME: make configurable
def find_source(root_dir):
    file_paths = glob.iglob(root_dir + '/**', recursive=True)
    sources = filter(is_source, file_paths)
    no_tests = filterfalse(is_test, sources)
    return no_tests

def scan(source_dir):
    sources = find_source(source_dir)
    # sources = islice(find_source(source_dir), 3)
    source_count = len(list(sources))
    print(f'{source_dir=}')
    print(f'{source_count=}')

def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python shotglass.py <filename>")

    source_dir = sys.argv[1]
    scan(source_dir)

if __name__ == "__main__":
    main()