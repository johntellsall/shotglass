#!/usr/bin/env python

"""
sparklines -- show sparkline in terminal on file sizes
"""

# pylint: disable=bad-builtin

import logging
import sys

import sparklines
from django.core.management.base import BaseCommand

from app.models import SourceFile


logging.basicConfig(
    stream=sys.stderr,
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def plot(project):
    WIDTH = 20
    query = SourceFile.objects.filter(project=project).order_by("-num_lines")
    num_lines = query.values_list("num_lines", flat=True)
    largest, num_files = num_lines.first(), num_lines.count()

    print(f"{project}: {num_files} source files, largest = {largest} lines")

    data = [num_lines[i] for i in range(0, num_files, int(num_files / WIDTH))]
    print(sparklines.sparklines(data)[0])

    print("Largest:")
    for info in query[:10]:
        print(info.num_lines, info.path)


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument("projects", nargs="+")

    def handle(self, *args, **options):
        projects = options["projects"]
        if projects == ["all"]:
            projects = SourceFile.projects()

        for project in projects:
            print("PROJECT {}:".format(project.upper()))
            plot(project)
