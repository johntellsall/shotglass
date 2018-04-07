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


def do_version(tree):
    def interestingp(i, _):
        return is_interesting(i.path)

    for item in tree.traverse(predicate=interestingp):
        yield (item.path, {'item': item, 'count': count_lines(item)})


def do_project(project):
    repo = git.Repo(project)
    versions_names = ['0.8', '0.10', '0.12']

    versions = dict((name, repo.tags[name]) for name in versions_names)
    detail = {}
    for ver_label, version in versions.items():
        detail[ver_label] = dict(do_version(version.commit.tree))

    latest = detail[versions_names[-1]]
    for path in sorted(latest):
        path_ver_count = {}
        for ver_label, ver_detail in detail.items():
            if path in ver_detail:
                path_ver_count[(path, ver_label)] = ver_detail[path]['count']
        # later_item = later[path]
        # earlier_count = ''
        # if path in earlier:
        #     earlier_count = earlier[path]['count']
        print(f'{path:30}')


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('projects', nargs=1)

    def handle(self, *args, **options):
        for proj in options['projects']:
            do_project(proj)
