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
    num_symbols = symbols.count()
    num_files = symbols.values_list('path', flat=True).distinct().count()
    return dict(length=length, num_files=num_files, num_symbols=num_symbols)


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
        if 0:
            tags = tags[:10]
        print tags

        tag_stats = {}
        for tag in tags:
            tag_stats[tag] = get_stats(tag)

        for index, tag in enumerate(tags):
            m = re.search(r'v(1.0|2.0.0.0-1)$', tag)
            if not m:
                continue
            version = m.group(1)
            plt.annotate(
                'v{}'.format(version[0]), xy=(index, 20), xytext=(index, 1.5))
                    # arrowprops=dict(facecolor='black', shrink=0.05),
                    # )

        STYLES = dict(length='r-', num_symbols='b-', num_files='g-')

        plt.style.use('fivethirtyeight') # see plt.style.available
        stat_keys = tag_stats.values()[0]
        for stat_key in stat_keys:
            try:
                values = [tag_stats[tag][stat_key]
                    for tag in tags]
            except KeyError as err:
                print '?', err
                continue
            print values
            plot_style = STYLES.get(stat_key, 'ro')
            plt.plot(values, plot_style)
            # plt.plot(tag_lengths)
        plt.title('Ansible')
        plt.xlabel('Version')
        # plt.ylabel('function length')
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