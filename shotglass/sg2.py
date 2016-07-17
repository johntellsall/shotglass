import os

from git import Repo

repo = Repo(os.path.expanduser('~/src/iproute2'))
tags = [tag.name.lstrip('v') for tag in repo.tags
    if tag.name.startswith('v3.') or tag.name == 'v4.0.0']
tags.sort(key=lambda st: map(int, st.split('.')))
print tags
