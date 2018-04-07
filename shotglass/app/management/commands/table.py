import difflib
import os
import re

import git
from django.core.management.base import BaseCommand


def is_interesting(path):
    if re.search('(docs|examples|scripts|testsuite)/', path):
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
        yield (item, count_lines(item))
        # print(f'{num_lines}\t{item.path}')

def do_project(project):
    import operator
    blob_path = operator.attrgetter('path')
    # def compare_blobs(a,b):
    #     return cmp(a.path, b.path)

    repo = git.Repo(project)
    earlier = dict(do_version(repo.tags['0.8'].commit.tree))
    later = dict(do_version(repo.tags['0.9'].commit.tree))
    for item in sorted(later, key=blob_path):
        count_later = count_lines(item)
        print(f'{item.path:30} {count_later}')
    # diffs = repo.commit('0.8').diff('0.9')
    # diffs = [d for d in diffs if is_interesting(d.b_path)]
    # for diff in diffs:
    #     print('{}'.format(diff.b_path))
    #     a_text = get_text(diff.a_blob)
    #     b_text = get_text(diff.b_blob)
    #     try:
    #         parts = difflib.Differ().compare(a_text, b_text)
    #         print(", ".join(parts))
    #     except Exception as exc:
    #         print('?', exc)
        # import ipdb ; ipdb.set_trace()
        # print('{}\t{}'.format(diff.b_path, 
        #     diff.b_blob.data_stream.read()[:40]))


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('projects', nargs=1)

    def handle(self, *args, **options):
        for proj in options['projects']:
            do_project(proj)