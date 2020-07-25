import glob
import pathlib

from git import Git, Repo


SOURCE = pathlib.Path('~/jsrc/shotglass/SOURCE').expanduser()

def ls_files(gitobj, pat):
    return gitobj.ls_files(pat).split('\n')

for project in SOURCE.glob('flask'):
    print(project.name)
    gitproj = Git(project)
    py_count = len(ls_files(gitproj, '*.py'))
    c_count = len(ls_files(gitproj, '*.c'))
    total_count = len(ls_files(gitproj, '*'))

    print(f'{project.name} {total_count} {py_count} {c_count}')
    # import ipdb; ipdb.set_trace()
