"""
evolve.py -- show code changes over time
"""

import os
import re

from django.core.management.base import BaseCommand
from git import Repo
import matplotlib.pyplot as plt


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
    re_path_num = re.compile(
        r'^\s(\S+) .+? \| \s+ (\d+)', 
        re.MULTILINE | re.VERBOSE)
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


class Matcher(object):
    def __init__(self, pattern):
        self.match = re.compile(pattern).search

class ManpageMatcher(Matcher):
    def __init__(self):
        super(ManpageMatcher, self).__init__('man/')

all_matcher = str


def get_paths(repo):
    diff_text = repo.git.diff(range_all, stat=True)
    all_paths = (match.group(1) for match in parse_diff_changes(diff_text))
    return sorted(all_paths)


def render_image(repo, matchfunc):
    paths = filter(matchfunc, get_paths(repo))
    print paths
    tags = get_tags(repo)

    path_index = dict((path, index)
        for index,path in enumerate(paths))

    symbols = []
    old = tags.pop(0)
    for y,new in enumerate(tags):
        diff_index = old.commit.diff(new)
        print '{:7}: {:3}'.format(new.name, len(diff_index))
        diff_paths = set(paths) & set(path_index)
        if not diff_paths:
            continue
        diff_text = repo.git.diff(
            '{}..{}'.format(old.name, new.name),
            *diff_paths,
            stat=True)
        diff_path_changes = parse_diff_changes(diff_text)
        for path,diff_count in (
            match.groups() for match in diff_path_changes):
            try:
                x = path_index[path]
            except IndexError:
                print '?', path
                continue
            area = 6 * len(diff_count)
            symbols.append((x, y, area))
        old = new

    xs, ys, areas = zip(*symbols)
    plt.scatter(xs, ys, s=areas)
    plt.xlabel('file index')
    plt.ylabel('version index')
    plt.savefig('z.png')
    plt.savefig('z.svg')


def render_text(repo, matchfunc):
    paths = filter(matchfunc, get_paths(repo))

    print len(paths), 'files'
    path_index = dict((path, index)
        for index,path in enumerate(paths))

    tags = get_tags(repo)
    old = tags.pop(0)
    for new in tags:
        diff_index = old.commit.diff(new)
        print '{:7}: {:3}'.format(new.name, len(diff_index)),
        diff_paths = set(paths) & set(path_index)
        diff_text = repo.git.diff(
            '{}..{}'.format(old.name, new.name), 
            *diff_paths,
            stat=True)
        diff_path_changes = parse_diff_changes(diff_text)
        print format_path_changes(paths, diff_path_changes)
        old = new


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('--match', choices=('manpage', 'source'))
        parser.add_argument('--style', choices=('text', 'image'), 
            default='image')
        parser.add_argument('project_dirs', nargs='+')

    def handle(self, *args, **options):
        render_func = globals()['render_{}'.format(options['style'])]
        matchfunc = {
        # manpage -- in "man" subdir ending in .8 or .in
        'manpage': Matcher(r'man/.*[0-9n]$').match,
        'source': Matcher(r'\.[ch]$').match,
        }.get(options['match']) or all_matcher

        for project_dir in options['project_dirs']:
            repo = Repo(os.path.expanduser(project_dir))
            render_func(repo, matchfunc)
