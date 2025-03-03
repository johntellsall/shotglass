# proj_stat.py -- stats about codebase

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Project:
    name: str
    dirs: set
    source_files: set

    def __init__(self, name):
        self.name = name
        self.dirs = set()
        self.source_files = set()
    
def proj_stats(topdir):
    top = Path(topdir)
    proj = Project("beer")

    for path in top.rglob('*'):
        if path.is_dir():
            proj.dirs.add(path)

    print(f'PROJECT: {proj.name}')
    print(f'  Directories: {len(proj.dirs)}')
    print(f'  Source files: {len(proj.source_files)}')

def main(paths):
    for path in paths:
        proj_stats(path)

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
