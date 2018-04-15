import os
import re
import sys

import git
from django.core.management.base import BaseCommand
from natsort import natsorted


# TODO: filter diff types, e.g. hcommit.diff('HEAD~1').iter_change_type('A'):


def get_text(blob):
    if hasattr(blob, 'data_stream'):
        return blob.data_stream.read()
    return ''


def count_lines(blob):
    return sum(1 for line in blob.data_stream.stream.readlines())

# if re.search('(docs|examples|scripts|tests|testsuite)/', path):

def interesting_paths(tree, ignore_pat, suffixes):
    ignore_re = re.compile(ignore_pat)
    suffix_set = set(f'.{suffix}' for suffix in suffixes)

    def not_ignored(path):
        if ignore_pat and ignore_re.search(path):
            return False
        return True

    def good_suffix(path):
        return os.path.splitext(path)[-1] in suffix_set

    def interestingp(item, _):
        return not_ignored(item.path) and good_suffix(item.path)

    for item in tree.traverse(predicate=interestingp):
        yield item.path


def show_project_grid(project, versions, ignore_pat, suffixes):
    def get_tree(label):
        return repo.tags[label].commit.tree

    def in_latest(item, _):
        return item.path in paths

    # TODO simplify
    def render_cell(item):
        if item is None:
            return f'{"":8}'
        count = count_lines(item)
        return f'{count:8}'

    repo = git.Repo(project)
    latest_label = versions[-1]
    paths = set(interesting_paths(
        get_tree(latest_label), ignore_pat, suffixes))

    grid = {}  # key=(version, path); value=item
    for label in versions:
        tree = get_tree(label)
        for item in tree.traverse(predicate=in_latest):
            grid[(label, item.path)] = item

    headers = (f'{label:>8}' for label in versions)
    print(f'{"":40} {" ".join(headers)}')

    for path in sorted(paths):
        row = [grid.get((ver_label, path))
            for ver_label in versions]
        num_nonzero = sum(1 for count in row if count)
        # TODO move to option
        if num_nonzero < 4:
            # path only in a couple releases: ignore
            continue
        cells = map(render_cell, row)
        print(f'{path:40} {" ".join(cells)}')


def parse_versions(opt_versions):
    if os.path.exists(opt_versions):
        return [line.strip() for line in open(opt_versions)]
    return opt_versions.split(',')


def usage_versions(project):
    repo = git.Repo(project)
    tags_names = natsorted(tag.name for tag in repo.tags)
    print(f'project {project}: tags/versions {tags_names}')


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('--ignore-dirs', default='') # TODO
        parser.add_argument('--ignore', default='')
        parser.add_argument('--suffixes', default='py')
        parser.add_argument('--versions')
        parser.add_argument('projects', nargs=1)

    def handle(self, *args, **options):
        if not options['versions']:
            usage_versions(options['projects'][0])
            sys.exit(1)
        versions = parse_versions(options['versions'])

        for proj in options['projects']:
            suffixes = options['suffixes'].split(',')
            show_project_grid(
                proj, versions,
                ignore_pat=options['ignore'],
                suffixes=suffixes)
