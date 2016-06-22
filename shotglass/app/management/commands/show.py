from django.core.management.base import BaseCommand
from django.db.models import Avg, Max, Sum

from app.models import SourceLine


def show_index(projects):
    FORMAT = '{name:30} {path}:{line_number}'

    def fun_symbol(sym):
        return sym.name[0] != '_'

    for project in projects:
        # pylint: disable=no-member
        symbols = SourceLine.objects.filter(
            project=project).order_by('name')
        for symbol in filter(fun_symbol, symbols):
            print FORMAT.format(**symbol.__dict__)


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
        parser.add_argument('--index', action="store_true")

    def handle(self, *args, **options):
        if not options['projects']:
            all_projects = SourceLine.projects()
            print('PROJECTS: {}'.format(', '.join(all_projects)))
            print('or "all"')
            return
        projects = options['projects']
        if projects == ['all']:
            projects = SourceLine.projects()

        if options['index']:
            show_index(projects)
        else:
            show_summary(projects)
