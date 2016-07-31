"""
age.py -- show age of code
"""
# pylint: disable=W0640

# list files in Git branch
# git ls-tree --name-status --full-tree -r v4.0.0

import datetime
import math
import os
import re

import matplotlib.pyplot as plt
from django.core.management.base import BaseCommand
from git import Repo
from palettable import colorbrewer
from PIL import Image, ImageDraw


BLACK = (0, 0, 0)
CMAP_NAME = 'PiYG_11'
CMAP_OBJ = getattr(colorbrewer.diverging, CMAP_NAME)
CMAP_COLORS = map(tuple, CMAP_OBJ.colors)
MAX_DAYS = 5 * 365
CMAP_SCALE = (len(CMAP_COLORS) - 1) / math.log10(MAX_DAYS)

COL_WIDTH, COL_HEIGHT = 100, 2000
COL_GAP = 10


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

def get_tag_paths(repo, tag):
    ls_tree_text = repo.git.ls_tree(
        tag, full_tree=True, name_status=True, r=True)
    return ls_tree_text.split('\n')

# X probably buggy
def get_latest_datetime(repo, tag):
    latest_opts = {'1': True, 'date': 'short', 'format': '%cd'}
    log_text = repo.git.log(tag, **latest_opts)
    log_date = datetime.datetime.strptime(log_text, '%Y-%m-%d')
    return log_date

def OLD_render_image(repo, matchfunc):
    good_paths = filter(matchfunc, get_paths(repo))
    print good_paths
    tags = get_tags(repo)

    good_index = dict((path, index)
        for index,path in enumerate(good_paths))

# TODO: currently does git-diff, then re-does diff to get each
# "good" path's contribution.  Simplify to just do git-diff once.

    symbols = []
    old = tags.pop(0)
    for y,new in enumerate(tags):
        diff_index = old.commit.diff(new)
        diff_versions = '{}..{}'.format(old.name, new.name)
        old = new
        print '{:7}: {:3}'.format(new.name, len(diff_index))
        diff_paths = set(d.a_path for d in diff_index) & set(good_paths)
        if not diff_paths:
            # version has diffs, but not in the region of interest
            print '- skip:', new
            continue
        diff_text = repo.git.diff(diff_versions, *diff_paths, stat=True)
        diff_path_changes = parse_diff_changes(diff_text)
        for path,diff_count in (
            match.groups() for match in diff_path_changes):
            try:
                x = good_index[path]
            except IndexError:
                print '?', path
                continue
            area = 6 * len(diff_count)
            symbols.append((x, y, area))

    xs, ys, areas = zip(*symbols)
    plt.scatter(xs, ys, s=areas)
    plt.xlabel('file index')
    plt.ylabel('version index')
    plt.savefig('z.png')
    plt.savefig('z.svg')

def serpentine_iter(width):
    y = 0
    while True:
        for x in xrange(width):
            yield x, y
        for x in xrange(width):
            yield width - x - 1, y + 1
        y += 2


def format_age(mycommit, mylatest):
    """
    format commit age as single character
    0-9 days / 10-99 days / 100-999 days
    """
    authored_dt = mycommit.authored_datetime.replace(tzinfo=None)
    delta_days = (mylatest - authored_dt).days
    if delta_days < -1:
        print 'UHOH:', delta_days
        return (255, 0, 0) # bogus = hot red
    if delta_days > MAX_DAYS:
        return (50, 50, 50) # old = dark grey
    delta_days = min(max(0, delta_days), MAX_DAYS)
    if 0:
        delta_num = math.log10(delta_days + 1)
        delta_index = delta_num * CMAP_SCALE
    else:
        delta_index = len(CMAP_COLORS) * delta_days / MAX_DAYS
    try:
        return CMAP_COLORS[int(delta_index)]
    except IndexError:
        print 'UHOH:', delta_index
        return (40, 40, 40)


def iter_source(repo, tag, tag_paths):
    latest = get_latest_datetime(repo, tag)
    print '-', tag, latest
    for tag_path in tag_paths:
        print '.', tag_path
        blame = repo.blame(tag, tag_path)
        for commit, regions in blame:
            yield format_age(commit, latest), len(regions)


def render_image_tag(repo, matchfunc, tag):
    width = COL_WIDTH
    height = COL_HEIGHT
    tag_paths = filter(matchfunc, get_tag_paths(repo, tag))

    im = Image.new('RGB', (width, height))
    im_pixel = im.load()
    image_iter = serpentine_iter(width=width)
    for color, size in iter_source(repo, tag, tag_paths):
        for _ in xrange(size):
            im_pixel[image_iter.next()] = color
    return im


def render_image(repo, matchfunc, options):
    tags_limit = options['num_tags'] or 3
    tags = get_tags(repo)[:tags_limit]
    size = (COL_WIDTH + COL_GAP)*len(tags), COL_HEIGHT
    image = Image.new('RGB', size)
    for index,tag in enumerate(tags):
        print tag, ':'
        subimage = render_image_tag(repo, matchfunc, tag)
        image.paste(subimage, ((COL_WIDTH + COL_GAP)*index, 0))
    image = image.crop(image.getbbox())
    image.save('z.png')

# Quickly find all functions (not Python?):
# git grep --line-number --no-color --show-function --word-regexp 
# -E '\S'  | egrep '=[0-9]+='
# Find all directories with source:
# find . -name '*.py' | xargs dirname | sort -u >source-dirs

def render_index(repo, matchfunc, options):
    func_re = re.compile('(.+?)=(\d+)=(.+)')
    grep_out = repo.git.grep('.', 'tc', line_number=True, no_color=True, show_function=True,  word_regexp=True)
    for match in func_re.finditer(grep_out):
        print match.groups()
    #  . $(cat source-dirs) | egrep =[0-9]+=

def render_text(repo, matchfunc, options):
    def format_age(mycommit, mylatest):
        """
        format commit age as single character
        * recent (0-9 days); + 10-99 days, - 100-999 days
        """
        authored_dt = mycommit.authored_datetime.replace(tzinfo=None)
        delta = mylatest - authored_dt
        delta_num = len(str(delta.days))
        return '?*+-.'[delta_num]

    tag = 'v4.0.0'
    latest = get_latest_datetime(repo, tag)
    for path in filter(matchfunc, get_tag_paths(repo, tag)):
        blame = repo.blame(tag, path)
        def path_age():
            for commit, regions in blame:
                yield format_age(commit, latest) * len(regions)
        print path, ':', ''.join(path_age())

# find . -name '*.c' | xargs dirname | sort -u


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        render_styles = [name.split('_')[-1] for name in globals()
            if name.startswith('render_')]

        parser.add_argument('--match', choices=('manpage', 'source'))
        parser.add_argument('--num_tags', type=int)
        parser.add_argument('--style', choices=render_styles, 
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
            render_func(repo, matchfunc, options)
