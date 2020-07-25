import glob
import pathlib

from git import Git, Repo


SOURCE = pathlib.Path('~/jsrc/shotglass/SOURCE').expanduser()

# interesting words:
# doc, example, test, tool

def line_count(path):
    return sum(1 for _ in open(path))

def ls_files(gitobj, pat):
    return gitobj.ls_files(pat).split('\n')

def count_project(project):
    gitproj = Git(project)
    return {
    'python': len(ls_files(gitproj, '*.py')),
    'c': len(ls_files(gitproj, '*.c')),
    'total': len(ls_files(gitproj, '*'))
    }

# def index_project(project):
#     name = project.name
#     source = 

def main():
    projects = SOURCE.glob('dnsmasq')
    projects = SOURCE.glob('[a-z]*')
    for project in sorted(projects):
        count = count_project(project)
        # assert 0, count
        print(f'{project.name:20} {count["total"]:5} ')
        # print(f'{project.name:20} {count.total:5} {py_count:4} {c_count:4}')
    # import ipdb; ipdb.set_trace()

if __name__=='__main__':
    main()
