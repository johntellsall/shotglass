#!/usr/bin/env python

'''
make_index -- compile data from tree of source files
'''

# pylint: disable=bad-builtin

import logging
import os
import re
import subprocess

import django.db
from django.core.management.base import BaseCommand
from radon.complexity import cc_visit

from app.models import SourceLine, ProgPmccabe


INDEX_SUFFIXES = ('.c', '.py')

if 0:
    # XX: never flushes logs!
    logger = logging.getLogger(__name__)
else:
    class HackLogger(object):
        def logme(self, myformat, *args):
            print '*', myformat % args
        debug = info = warning = logme
    logger = HackLogger()


def calc_radon(path):
    code = open(path).read()
    funcs_data = cc_visit(code)
    # TODO: lines = max(func.endline for func in funcs_data)
    return dict((func.lineno, func) for func in funcs_data)


def calc_path_tags(path):
    tags = path.split('/')[:-1]
    return tags


def format_project_name(project_dir):
    pdir = os.path.basename(project_dir.rstrip('/'))
    return pdir


def walk_type(topdir, name_func):
    for root, _, names in os.walk(topdir):
        paths = [os.path.join(root, name) for name in names
            if name_func(name)]
        for path in paths:
            yield path


# def index_ctags(project, ctags_path):
#     """
#     use Exuberant Ctags to find symbols
#     """
#     tagFile = ctags.CTags(ctags_path)
#     entry = ctags.TagEntry()

#     if not tagFile.find(entry, '', ctags.TAG_PARTIALMATCH):
#         sys.exit('no tags?')

#     while True:
#         if entry['kind']:
#             path = entry['file']
#             tags = {'path': calc_path_tags(path)}
#             try:
#                 SourceLine(name=entry['name'],
#                            project=project,
#                            path=path,
#                            length=0, # XX should be None
#                            line_number=entry['lineNumber'],
#                            kind=entry['kind'],
#                            tags_json=json.dumps(tags)).save()
#             except django.db.utils.ProgrammingError:
#                 logger.error('%s: uhoh', entry['name'])
#         status = tagFile.findNext(entry)
#         if not status:
#             break


def index_py_radon(project, paths):
    # X: Radon only supports Python
    # pylint: disable=no-member
    for path in paths:
        radon = calc_radon(path)
        print path, len(radon)
        # for lineno,radon_obj in radon.iteritems():
            # try:
            #     symbol = SourceLine.objects.get(
            #         path=path, project=project, line_number=lineno)
            #     tags = json.loads(symbol.tags_json)
            #     # X: expose the other fields?
            #     tags['radon_cc'] = radon_obj.complexity
            #     symbol.tags_json = json.dumps(tags)
            #     symbol.save()
            # except SourceLine.DoesNotExist:
            #     # XX Radon counts @-lines as start
            #     print '?', path, lineno, radon_obj.name


# # X: doesn't calc last symbol of each file correctly
# def index_symbol_length(project):
#     logger.debug('%s: calculating symbol lengths', project)
#     # pylint: disable=no-member
#     source = SourceLine.objects.filter(project=project
#         ).order_by('path', 'line_number')
#     prev_path = None
#     prev_symbol = None
#     for symbol in source:
#         if symbol.path != prev_path:
#             prev_symbol = None
#             prev_path = symbol.path
#         if prev_symbol:
#             prev_symbol.length = symbol.line_number - prev_symbol.line_number
#             if prev_symbol.kind in ('variable', 'class'):
#                 prev_symbol.length = 1
#             prev_symbol.save()
#         prev_symbol = symbol


def index_c_mccabe(project, paths):
    pmccabe_pat = re.compile(
        r'^(?P<data> [0-9\t]+)'
        r'(?P<path> .+?)'
        r'\( (?P<definition_line> \d+) \): \s+ '
        r'(?P<function> .+)',
        re.VERBOSE)

    paths = list(paths)
    logger.debug('%s: calculating C complexity, %d files',
        project, len(paths))
    if not paths:
        return

    output = subprocess.check_output(
        ['pmccabe'] + paths).split('\n')

    for match in filter(None, (map(pmccabe_pat.match, output))):
        data = [int(field) for field in match.group('data').split()]
        num_lines = data[4]
        definition_line = int(match.group('definition_line'))
        sourceline = SourceLine.objects.create(
            project=project,
            path=match.group('path'),
            name=match.group('function'),
            line_number=definition_line,
            length=num_lines)
        ProgPmccabe.objects.create(
            sourceline=sourceline,
            first_line=data[3],
            modified_mccabe=data[0],
            mccabe=data[1],
            num_statements=data[2],
            # overlap w/ SourceLine
            num_lines=num_lines,
            definition_line=definition_line)
        

    # def find_source_paths(self, top):
    #     # XX
    #     bad_dir_pat = re.compile(
    #         r'(contrib|debian|conf/locale|\.pc|pl|tests)')
    #     for root, _, names in os.walk(top):
    #         if bad_dir_pat.search(root):
    #             continue
    #         names = (name for name in names if name.endswith(INDEX_SUFFIXES))
    #         for path in (os.path.join(root, name) for name in names):
    #             yield path

    # def find_source(self, project_dir, project):
    #     """
    #     find source code in tree, write to list file
    #     """
    #     paths = self.find_source_paths(top=project_dir)
    #     list_path = '{}.lst'.format(project)
    #     with open(list_path, 'w') as listf:
    #         listf.write('\n'.join(paths))
    #     return list_path

    # def find_tags(self, project, list_path):
    #     """
    #     from selected source, find symbols
    #     """
    #     # Python: classes, functions, members, variables
    #     cmd = 'ctags --fields=afmikKlnsStz -L {} -o {}'
    #     tags_path = '{}.tags'.format(project)
    #     subprocess.check_call(
    #         cmd.format(list_path, tags_path), shell=True)
    #     return tags_path

def make_index(project, project_dir):
    is_c = re.compile(r'\.c$').search
    is_python = re.compile(r'\.py$').search
    
    if django.db.connection.vendor == 'sqlite':
        django.db.connection.cursor().execute('PRAGMA synchronous=OFF')

    # XX: delete project's index
    # pylint: disable=no-member
    SourceLine.objects.filter(project=project).delete()
    
    c_paths = list(walk_type(project_dir, is_c))
    logger.info('%s: %d C files', project, len(c_paths))
    index_c_mccabe(project, c_paths)
    # shows as "0" because of the PRAGMA SYNC above

    py_paths = list(walk_type(project_dir, is_python))
    logger.info('%s: %d Python files', project, len(py_paths))
    index_py_radon(project, py_paths)

    # index_ctags(project, tags_path)
    # index_symbol_length(project)
    # index_radon(project)


class Command(BaseCommand):
    help = 'beer'

    def add_arguments(self, parser):
        parser.add_argument('project_dirs', metavar='FILE', nargs='+')
        parser.add_argument('--project')
        parser.add_argument('--tags')
        parser.add_argument('--list_path')

    def handle(self, *args, **options):
        for project_dir in map(os.path.expanduser, options['project_dirs']):
            if not os.path.isdir(project_dir):
                logger.warning(
                    '%s: project must be directory, skipping', project_dir)
                continue
            # X: doesn't support multiple dirs
            project_name = (options.get('project')
                or format_project_name(project_dir))

            logger.info('%s: start', project_name)
            make_index(project_name, project_dir)

            project_source = SourceLine.objects.filter(project=project_name)
            if 01: # X: 0 because of PRAGMA SYNC
                logger.info('%s: %s symbols', project_name,
                        '{:,}'.format(project_source.count()))

            logger.debug('%s: done', project_name)
