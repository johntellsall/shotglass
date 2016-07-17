import os
import re

from git import Repo

repo = Repo(os.path.expanduser('~/src/iproute2'))

tags = [tag.name.lstrip('v') for tag in repo.tags
    if tag.name.startswith('v3.') or tag.name == 'v4.0.0']
tags.sort(key=lambda st: map(int, st.lstrip('v').split('.')))
tags = [repo.tags['v'+version] for version in tags]

old = tags.pop(0)
for new in tags:
    diff_index = old.commit.diff(new)
    print '{:7} - {:7}: {} commits'.format(
        old.name, new.name, len(diff_index))
    old = new

# IDEA: use iter_change_type('A') to get all file paths, even if they've been renamed/deleted
# Or: git.diff('v3.0.0..v4.0.0',name_status=True)
# ALSO
# - git.diff('v3.0.0..v3.1.0',dirstat=True)

range_1 = 'v3.0.0..v3.1.0'
range_all = 'v3.0.0..v4.0.0'

def zoot(mygit):
    re_path_num = re.compile(r'^\s(\S+).+?(\d+)', re.MULTILINE)
    diff_text = mygit.diff(range_1, stat=True)
    return re_path_num.finditer(diff_text)

