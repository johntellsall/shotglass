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
    def get_tree(label):
        return repo.tags[label].commit.tree

    def in_latest(item, _):
        return item.path in paths

    repo = git.Repo(project)
    versions_labels = ['0.6', '0.8', '0.10', '0.12']

    latest_label = versions_labels[-1]
    paths = set(interesting_paths(get_tree(latest_label)))

    grid = {}  # key=(version, path); value=item
    for label in versions_labels:
        tree = get_tree(label)
        for item in tree.traverse(predicate=in_latest):
            grid[(label, item.path)] = item

    headers = (f'{label:>4}' for label in versions_labels)
    print(f'{"":30} {" ".join(headers)}')

    for path in sorted(paths):
        counts = []
        for ver_label in versions_labels:
            item = grid.get((ver_label, path))
            if item:
                counts.append(f'{count_lines(item):4}')
            else:
                counts.append(f'{"":4}')
        print(f'{path:30} {" ".join(counts)}')


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('--versions')
        parser.add_argument('projects', nargs=1)

    def handle(self, *args, **options):
        for proj in options['projects']:
            do_project(proj)
