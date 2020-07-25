import glob
import pathlib

from git import Git, Repo


SOURCE = pathlib.Path('~/jsrc/shotglass/SOURCE').expanduser()


for project in SOURCE.glob('flask'):
    print(project.name)
    g = Git( project )
    rval = g.ls_files('*.py')
    import ipdb; ipdb.set_trace()
