# shotglass.py -- count source lines, render simply

import glob
from pathlib import Path
import sys
from itertools import accumulate, filterfalse, islice

SOURCE_EXTENSIONS = ('.py', '.c', '.cpp')

# FIXME: make configurable
def is_source(path):
    return path.endswith(SOURCE_EXTENSIONS)

# FIXME: make configurable
def is_test(path):
    return '/test' in path

# FIXME: make configurable
def find_source(root_dir):
    if not Path(root_dir).is_dir():
        raise ValueError(f'{root_dir} is not a directory')
    file_paths = glob.iglob(root_dir + '/**', recursive=True)
    sources = filter(is_source, file_paths)
    no_tests = filterfalse(is_test, sources)
    return no_tests

def scan(source_dirs):
    for source_dir in source_dirs:
        print(f'{source_dir=}')
        sources = find_source(source_dir)
        source_count = len(list(sources))
        print(f'\t{source_count=}')

def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python shotglass.py <filename>")

    source_dirs = sys.argv[1:]
    scan(source_dirs)

if __name__ == "__main__":
    main()