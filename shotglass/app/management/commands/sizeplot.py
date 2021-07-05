"""
sizeplot
"""

import re

import matplotlib.pyplot as plt
from django.core.management.base import BaseCommand
from django.db.models import Sum

from app import models

# X compare with from natsort import natsorted


def natural_sort_key(s, _nsre=re.compile("([0-9]+)")):
    return [
        int(text) if text.isdigit() else text.lower() for text in re.split(_nsre, s)
    ]


def get_stats(tag):
    symbols = models.SourceLine.objects.filter(project=tag)
    length = symbols.aggregate(Sum("length")).values()[0]
    num_symbols = symbols.count()
    num_files = symbols.values_list("path", flat=True).distinct().count()
    return dict(length=length, num_files=num_files, num_symbols=num_symbols)


class Command(BaseCommand):
    help = __doc__
    STYLES = dict(length="r.", num_symbols="b-", num_files="g-")

    def add_arguments(self, parser):
        parser.add_argument("projects", nargs="+")

    def render_project(self, project):
        tags = (
            models.SourceLine.objects.filter(project__startswith=project)
            .values_list("project", flat=True)
            .distinct()
        )
        tags = sorted(tags, key=natural_sort_key)
        # tags = [tag for tag in tags if '_' not in tag]
        if 0:
            tags = tags[:10]

        tag_stats = {}
        for tag in tags:
            tag_stats[tag] = get_stats(tag)
            print "{:<20} {}".format(tag, tag_stats[tag])
        if 0:
            for index, tag in enumerate(tags):
                m = re.search(r"v(1.0|2.0.0.0-1)$", tag)
                if not m:
                    continue
                version = m.group(1)
                plt.annotate(
                    "v{}".format(version[0]), xy=(index, 20), xytext=(index, 1.5)
                )

        plt.style.use("fivethirtyeight")  # see plt.style.available
        stat_keys = tag_stats.values()[0]
        for stat_key in stat_keys:
            try:
                values = [tag_stats[tag][stat_key] for tag in tags]
            except KeyError as err:
                print "?", err
                continue
            plot_style = self.STYLES.get(stat_key, "ro")
            plt.plot(values, plot_style)
        plt.title(project)
        #        plt.xlabel('Version')

        # def format_fn(tick_val, tick_pos):
        #     try:
        #         return tags[int(tick_val)]
        #     except IndexError:
        #         return '?'
        # ax = plt.figure().add_subplot(111)
        # ax.xaxis.set_major_formatter(FuncFormatter(format_fn))
        # ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.savefig("{}.png".format(project))

    def handle(self, *args, **options):
        for project in options["projects"]:
            self.render_project(project)
