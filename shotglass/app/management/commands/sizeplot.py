import re

import matplotlib.pyplot as plt
from django.core.management.base import BaseCommand
from django.db.models import Sum

from app import models


def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]    


def get_stats(tag):
    symbols = models.SourceLine.objects.filter(project=tag)
    length = symbols.aggregate(Sum('length')).values()[0]
    return dict(length=length)


class Command(BaseCommand):
    help = __doc__

    # def add_arguments(self, parser):
    #     render_styles = [name.split('_')[-1] for name in globals()
    #         if name.startswith('render_')]

    #     parser.add_argument('--match', choices=('manpage', 'source'))
    #     parser.add_argument('--num_tags', type=int)
    #     parser.add_argument('--style', choices=render_styles, 
    #         default='image')
    #     parser.add_argument('project_dirs', nargs='+')

    def handle(self, *args, **options):
        tags = models.SourceLine.objects.filter(
            project__startswith='ansible-').values_list('project', flat=True).distinct()
        tags = sorted(tags, key=natural_sort_key)
        print tags

        tag_length = {}
        tag_lengths = []
        for tag in tags:
            stats = get_stats(tag)
            tag_length[tag] = stats['length']
            tag_lengths.append(stats['length'])
            print tag, stats['length']

        plt.plot(tag_lengths)
        plt.title('Ansible')
        plt.xlabel('Version')
        plt.ylabel('function length')
        # plt.show()
        plt.savefig('z.png')
        # render_func = globals()['render_{}'.format(options['style'])]
        # matchfunc = {
        # # manpage -- in "man" subdir ending in .8 or .in
        # 'manpage': Matcher(r'man/.*[0-9n]$').match,
        # 'source': Matcher(r'\.[ch]$').match,
        # }.get(options['match']) or all_matcher

        # for project_dir in options['project_dirs']:
        #     repo = Repo(os.path.expanduser(project_dir))
        #     render_func(repo, matchfunc, options)