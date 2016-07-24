"""
evolve.py -- show code changes over time
"""

import os
import re

from django.core.management.base import BaseCommand
from git import Repo
# import matplotlib.pyplot as plt


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
# TODO: git blame --porcelain v3.0.0..v4.0.0 ip-fou.8

range_1 = 'v3.0.0..v3.1.0'
range_all = 'v3.0.0..v4.0.0'


    
# TODO: skip "total" at end
def parse_diff_changes(diff_text):
    re_path_num = re.compile(r'^\s(\S+).+?(\d+)', re.MULTILINE)
    return re_path_num.finditer(diff_text)

def format_path_changes(all_paths, path_changes):
    def format_diff_value(value):
        return '?.-+*ABCD'[len(value)]

    change_dict = dict(match.groups() for match in path_changes)
    def format_chars():
        for path in all_paths:
            if path not in change_dict:
                yield ' '
            else:
                yield format_diff_value(change_dict[path])
    return ''.join(format_chars())


def render_text(repo):
    re_manpage = re.compile('man/')
    git = repo.git
    diff_text = git.diff(range_all, stat=True)

    man_paths = [match.group(1) for match in parse_diff_changes(diff_text)
        if re_manpage.match(match.group(1))]
    man_paths.sort()

    print len(man_paths), 'manpages'
    man_index = dict((path, index)
        for index,path in enumerate(man_paths))

    tags = get_tags(repo)
    old = tags.pop(0)
    for new in tags:
        diff_index = old.commit.diff(new)
        print '{:7}: {:3}'.format(new.name, len(diff_index)),
        man_diff_paths = (set(diff.a_path for diff in diff_index)
            & set(man_index))
        diff_text = git.diff(
            '{}..{}'.format(old.name, new.name), 
            *man_diff_paths,
            stat=True)
        diff_path_changes = parse_diff_changes(diff_text)
        print format_path_changes(man_paths, diff_path_changes)
        old = new


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('--style', choices=('text', 'image'), 
            default='image')
        parser.add_argument('project_dirs', nargs='+')

    def handle(self, *args, **options):
        render_func = globals()['render_{}'.format(options['style'])]
        for project_dir in options['project_dirs']:
            repo = Repo(os.path.expanduser(project_dir))
            render_func(repo)
