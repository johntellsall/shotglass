import os
import re
import sys

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


def interesting_paths(tree):
    def interestingp(i, _):
        return is_interesting(i.path)

    for item in tree.traverse(predicate=interestingp):
        yield item.path


def show_project_grid(project, versions):
    def get_tree(label):
        return repo.tags[label].commit.tree

    def in_latest(item, _):
        return item.path in paths

    repo = git.Repo(project)

    latest_label = versions[-1]
    paths = set(interesting_paths(get_tree(latest_label)))

    grid = {}  # key=(version, path); value=item
    for label in versions:
        tree = get_tree(label)
        for item in tree.traverse(predicate=in_latest):
            grid[(label, item.path)] = item

    headers = (f'{label:>4}' for label in versions)
    print(f'{"":30} {" ".join(headers)}')

    for path in sorted(paths):
        counts = []
        for ver_label in versions:
            item = grid.get((ver_label, path))
            if item:
                counts.append(f'{count_lines(item):4}')
            else:
                counts.append(f'{"":4}')
        print(f'{path:30} {" ".join(counts)}')


def usage_versions(project):
    repo = git.Repo(project)
    tags_names = sorted(tag.name for tag in repo.tags)
    print(f'project {project}: tags/versions {tags_names}')

class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('--versions')
        parser.add_argument('projects', nargs=1)

    def handle(self, *args, **options):
        if not options['versions']:
            usage_versions(options['projects'][0])
            sys.exit(1)
        for proj in options['projects']:
            versions = options['versions'].split(',')
            show_project_grid(proj, versions)
