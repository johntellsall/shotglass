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
def parse_diff_changes(diff_text):
    re_path_num = re.compile(r'^\s(\S+).+?(\d+)', re.MULTILINE)
    return re_path_num.finditer(diff_text)

def format_path_changes(all_paths, path_changes):
    def format_diff_value(value):
        return '?.-+*'[len(value)]

    change_dict = dict(match.groups() for match in path_changes)
    def format_chars():
        for path in all_paths:
            if path not in change_dict:
                yield ' '
            else:
                yield format_diff_value(change_dict[path])
    return ''.join(format_chars())


re_manpage = re.compile('man/.+[0-9]$')
git = test_repo.git
diff_text = git.diff(range_all, stat=True)

man_paths = [match.group(1) for match in parse_diff_changes(diff_text)
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
        print '{:7}: '.format(new.name),
        man_diff_paths = (set(diff.a_path for diff in diff_index)
            & set(man_index))
        diff_text = git.diff(
            '{}..{}'.format(old.name, new.name), 
            *man_diff_paths,
            stat=True)
        diff_path_changes = parse_diff_changes(diff_text)
        print format_path_changes(man_paths, diff_path_changes)
        # print [m.groups() for m in diff_path_changes]
        #import ipdb ; ipdb.set_trace()
        old = new

