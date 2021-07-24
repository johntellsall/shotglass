import itertools
import operator
import numpy as np

import matplotlib.pyplot as plt
from django.core.management.base import BaseCommand

from app import models


class Command(BaseCommand):
    help = "beer"

    def add_arguments(self, parser):
        parser.add_argument("projects", nargs="+")

    def handle(self, *args, **options):
        fs = 10  # fontsize

        versions = (
            models.SourceLine.objects.filter(project__startswith="django-")
            .order_by("project")
            .values_list("project", "progradon__complexity")
        )
        for vers, complexity_iter in itertools.groupby(
            versions, key=operator.itemgetter(1)
        ):
            print(vers, ":")
            print("-", ", ".join(str(x) for x in complexity_iter))
        data = models.SourceLine.objects.filter(project="django-1.0.1").values_list(
            "progradon__complexity", flat=True
        )
        plt.boxplot(data)  # , labels=labels)

        plt.show()

        # xs, ys, areas = zip(*data)
        # ys = areas
        # colors = np.random.rand(len(xs))
        # plt.scatter(xs, ys, c=colors) # s=areas)
        # plt.xlabel('file index')
        # plt.ylabel('version index')
        plt.savefig("z.png")
        # plt.savefig('z.svg')
