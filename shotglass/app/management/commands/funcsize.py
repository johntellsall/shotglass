import numpy as np

import matplotlib.pyplot as plt
from django.core.management.base import BaseCommand

from app import models


class Command(BaseCommand):
    help = 'beer'

    def add_arguments(self, parser):
        parser.add_argument('projects', nargs='+')

    def handle(self, *args, **options):
        data = models.SourceLine.objects.values_list(
            'progpmccabe__num_lines', 'progpmccabe__num_statements',
            'progpmccabe__mccabe')
        xs, ys, areas = zip(*data)
        ys = areas
        colors = np.random.rand(len(xs))
        plt.scatter(xs, ys, c=colors) # s=areas)
        # plt.xlabel('file index')
        # plt.ylabel('version index')
        plt.savefig('z.png')
        # plt.savefig('z.svg')
