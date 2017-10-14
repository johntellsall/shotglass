import collections
import os
import sys

from django.core.management.base import BaseCommand
from django.db.models import Avg, Max, Sum

from app.models import SourceFile, Symbol


def show_file_index(projects):
    FORMAT = '{name:20} {path:50} {num_lines:>5}'
    print FORMAT.format(name='NAME', path='PATH', num_lines="LINES")
    for project in projects:
        # pylint: disable=no-member
        files = SourceFile.objects.filter(
            project=project).order_by('path')
        for file_ in files:
            print FORMAT.format(**vars(file_))

def show_dir_index(projects):
    """
    for each directory, output total number of source lines
    """
    FORMAT = '{dir_path:50} {num_lines:>5}'

    for project in projects:
        data = SourceFile.objects.filter(
            project=project).values_list('path', 'num_lines')
        count = collections.Counter()
        for path,num_lines in data:
            count[os.path.dirname(path)] = num_lines

        for dir_path,num_lines in sorted(count.iteritems()):
            print FORMAT.format(**locals())

# XX V1
def show_symbol_index(projects):
    FORMAT = '{name:30} {path}:{line_number}'

    def fun_symbol(sym):
        return sym.name[0] != '_'

    for project in projects:
        # pylint: disable=no-member
        symbols = SourceLine.objects.filter(
            project=project).order_by('name')
        for symbol in filter(fun_symbol, symbols):
            print FORMAT.format(**symbol.__dict__)


def show_summary(projects):
    HEADER = '{:30} {:>9} {:>6} {:>6} {:>10} {:>9}'.format(
        'project', 'files', 'avglen', 'maxlen', 'total', 'symbols')
    FORMAT = ('{project:30} {num_files:9,}'
        ' {avg_length:6,}'
        ' {max_length:6,}'
        ' {total_length:10,}'
        ' {num_symbols:9,}')

    print HEADER
    for project in projects:
        proj_qs = SourceFile.objects.filter(project=project)
        num_files = proj_qs.count()
        avg_length = int(proj_qs.aggregate(Avg('num_lines')).values()[0])
        max_length = proj_qs.aggregate(Max('num_lines')).values()[0]
        total_length = proj_qs.aggregate(Sum('num_lines')).values()[0]
        proj_symbols = Symbol.objects.filter(source_file__project=project)
        num_symbols = proj_symbols.count()
        print FORMAT.format(**locals())


class Command(BaseCommand):
    help = 'beer'

    def add_arguments(self, parser):
        parser.add_argument('projects', nargs='*')
        parser.add_argument('--style', default='summary')

        # if 0: # XX V1
        #     parser.add_argument('--index', action="store_true")
        # else:
        #     parser.add_argument('--dirindex', 
        #         action="store_true",
        #         help="show source lines per directory")
        #     parser.add_argument('--index', default=True)

    def handle(self, *args, **options):
        all_projects = SourceFile.projects()
        projects = options['projects']
        if not projects:
            print('PROJECTS: {}'.format(', '.join(all_projects)))
            print('or "all"')
            return
        if projects == ['all']:
            projects = all_projects

        try:
            style_fname = 'show_{}'.format(options['style'])
            infofunc = globals()[style_fname]
        except KeyError:
            sys.exit("{}: unknown style".format(options['style']))
        infofunc(projects)
        # if options['dirindex']:
        #     show_dir_index(projects)
        # elif options['index']:
        #     show_file_index(projects)
        # else:
        #     show_summary(projects)
