import collections
import os

from django.core.management.base import BaseCommand
from django.db.models import Avg, Max, Sum

from app.models import SourceFile


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


# XX V1
# pylint: disable=unused-variable
def show_summary(projects):
    HEADER = '{:30} {:>7} {:>9} {:>5} {:>4} {:>10}'.format(
        'project', 'functions', 'symbols', 'maxlen', 'avglen', 'total')
    FORMAT = ('{project:30} {num_functions:9,} {num_symbols:9,}'
        ' {max_length:6,}'
        ' {avg_length:6,} {total_length:10,}')

    print HEADER
    for project in projects:
        # pylint: disable=no-member
        symbols = SourceLine.objects.filter(project=project)
        num_symbols = symbols.count()
        num_functions = symbols.filter(kind__in=('F', 'M')).count()
        # TODO: optimize
        if not num_symbols:
            max_length = avg_length = total_length = 0
        else:
            max_length = symbols.aggregate(Max('length')).values()[0]
            avg_length = int(symbols.aggregate(Avg('length')).values()[0])
            total_length = symbols.aggregate(Sum('length')).values()[0]
        print FORMAT.format(**locals())


class Command(BaseCommand):
    help = 'beer'

    def add_arguments(self, parser):
        parser.add_argument('projects', nargs='*')
        if 0: # XX V1
            parser.add_argument('--index', action="store_true")
        else:
            parser.add_argument('--dirindex', 
                action="store_true",
                help="show source lines per directory")
            parser.add_argument('--index', default=True)

    def handle(self, *args, **options):
        all_projects = SourceFile.projects()
        projects = options['projects']
        if not projects:
            print('PROJECTS: {}'.format(', '.join(all_projects)))
            print('or "all"')
            return
        if projects == ['all']:
            projects = all_projects

        if options['dirindex']:
            show_dir_index(projects)
        elif options['index']:
            show_file_index(projects)
        else:
            show_summary(projects)
