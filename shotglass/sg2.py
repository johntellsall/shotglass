import os
import re

from git import Repo


def get_tags(repo):
    tags = [tag.name.lstrip('v') for tag in repo.tags
        if tag.name.startswith('v3.') or tag.name == 'v4.0.0']
    tags.sort(key=lambda st: map(int, st.lstrip('v').split('.')))
    tags = [repo.tags['v'+version] for version in tags]
    return tags

def show_version_diffs(tags):
    tags = list(tags)
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
test_repo = Repo(os.path.expanduser('~/src/iproute2'))


# TODO: skip "total" at end
def zoot(mygit, myrange):
    re_path_num = re.compile(r'^\s(\S+).+?(\d+)', re.MULTILINE)
    diff_text = mygit.diff(myrange, stat=True)
    return re_path_num.finditer(diff_text)

re_manpage = re.compile('man/.+[0-9]$')
git = test_repo.git
man_paths = [match.group(1) for match in zoot(git, range_all)
    if re_manpage.match(match.group(1))]
man_paths.sort()

print len(man_paths), 'manpages'
man_index = dict((path, index)
    for index,path in enumerate(man_paths))

if 1:
    tags = get_tags(test_repo)
    old = tags.pop(0)
    for new in tags:
        diff_index = old.commit.diff(new)
        print '{:7} - {:7}: {} commits'.format(
            old.name, new.name, len(diff_index))
        for diff in diff_index:
            # if diff.a_path.endswith('8'):
            #     import ipdb ; ipdb.set_trace()
            if diff.a_path in man_index:
                print os.path.split(diff.a_path)[-1],
            else:
                print '.',
        print
        #import ipdb ; ipdb.set_trace()
        old = new

