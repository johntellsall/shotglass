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

# TODO change to count index
def count_project(project):
    gitproj = Git(project)
    return {
        'python': len(ls_files(gitproj, '*.py')),
        'c': len(ls_files(gitproj, '*.c')),
        'total': len(ls_files(gitproj, '*'))
    }

def index_project(project):
    gitproj = Git(project)
    return {
        'python': ls_files(gitproj, '*.py'),
        'c': ls_files(gitproj, '*.c'),
        'total': ls_files(gitproj, '*')
    }

def diagram_project(project):
    projname = project.name
    index = index_project(project)
    d_source = [f'{projname} --> {source}'
        for source in index['c']]
    diagram = ['graph TD'] + d_source
    return '\n'.join(diagram)
#     source = 

def main():
    projects = SOURCE.glob('[a-z]*')
    for project in sorted(projects):
        count = count_project(project)
        print(f'{project.name:20} {count["total"]:5} ', end='')
        print(f'{count["python"]:5} {count["c"]:5} ')

# def main():
#     projects = SOURCE.glob('dnsmasq')
#     out = diagram_project(list(projects)[0])
#     open('zoot.mmd', 'w').write(out)
#     print(out)

if __name__=='__main__':
    main()
