import difflib
import os
import re

import git
from django.core.management.base import BaseCommand


def is_interesting(path):
    if re.search('(docs|examples|scripts|tests|testsuite)/', path):
        return False
    return os.path.splitext(path)[-1] in ['.py']

# TODO: filter diff types, e.g. hcommit.diff('HEAD~1').iter_change_type('A'):


def get_text(blob):
    if hasattr(blob, 'data_stream'):
        return blob.data_stream.read()
    return ''


def count_lines(blob):
    return sum(1 for line in blob.data_stream.stream.readlines())


# def do_version(tree):
#     def interestingp(i, _):
#         return is_interesting(i.path)

#     for item in tree.traverse(predicate=interestingp):
#         yield (item.path, {'item': item, 'count': count_lines(item)})

def interesting_paths(tree):
    def interestingp(i, _):
        return is_interesting(i.path)

    for item in tree.traverse(predicate=interestingp):
        yield item.path


def do_project(project):
    repo = git.Repo(project)
    versions_labels = ['0.8', '0.10', '0.12']

    def get_tree(label):
        return repo.tags[label].commit.tree

    latest_label = versions_labels[-1]
    paths = set(interesting_paths(get_tree(latest_label)))

    def in_latest(item, _):
        return item.path in paths

    grid = {} # key=(version, path); value=item
    for label in versions_labels:
        tree = get_tree(label)
        for item in tree.traverse(predicate=in_latest):
            grid[(label, item.path)] = item

    # versions = dict((name, repo.tags[name]) for name in versions_labels)
    # detail = {}
    # for ver_label, version in versions.items():
    #     detail[ver_label] = dict(do_version(version.commit.tree))

    # # TODO: don't count lines of paths that aren't in latest
    # latest = detail[versions_labels[-1]]
    # for path in latest:
    #     path_ver_count = {}
    #     for ver_label, ver_detail in detail.items():
    #         if path in ver_detail:
    #             path_ver_count[(path, ver_label)] = ver_detail[path]['count']

    for path in sorted(paths):
        def get_items():
            for ver_label in versions_labels:
                yield grid.get((ver_label, path))
        items = get_items()

        print(f'{path:30}')

        # later_item = later[path]
        # earlier_count = ''
        # if path in earlier:
        #     earlier_count = earlier[path]['count']


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('projects', nargs=1)

    def handle(self, *args, **options):
        for proj in options['projects']:
            do_project(proj)
