import os

from git import Repo

repo = Repo(os.path.expanduser('~/src/iproute2'))

tags = [tag.name.lstrip('v') for tag in repo.tags
    if tag.name.startswith('v3.') or tag.name == 'v4.0.0']
tags.sort(key=lambda st: map(int, st.lstrip('v').split('.')))
tags = ['v'+version for version in tags]

old = tags.pop(0)
for new in tags:
    print '{:7} - {:7}: {} commits'.format(
        old, new, len(repo.tags[old].commit.diff(new)))
    old = new
