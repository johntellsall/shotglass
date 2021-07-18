#!/usr/bin/env python

"""
pack -- 
"""

import json
import logging
import math
import os
import sys

import rectpack
from bokeh.plotting import figure, output_file, show
from django.core.management.base import BaseCommand

from app.models import SourceFile


logging.basicConfig(
    stream=sys.stderr,
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def box_dimensions(lines):
    dim = math.ceil(math.sqrt(lines))
    return [dim, dim]


def render(rectangles):
    p = figure(title="Beer Morphology")
    p.xaxis.axis_label = "Petal Length"
    p.yaxis.axis_label = "Petal Width"

    for (_, x, y, w, h, _) in rectangles:
        p.rect(x, y, width=w, height=h)

    output_file("zoot.html", title="example")

    show(p)


def pack(project):
    "pack each file sized according to count of source lines"
    file_data = SourceFile.objects.filter(project=project).values_list(
        "path", "num_lines"
    )
    total_lines = sum(item[1] for item in file_data)
    bin_lines = 2 * total_lines  # X: heuristic!

    packer = rectpack.newPacker()
    packer.add_bin(*box_dimensions(bin_lines))
    for path, num_lines in file_data:
        packer.add_rect(*box_dimensions(num_lines), rid=path)

    cache_path = "rect.json"
    if not os.path.exists(cache_path):
        logger.info("%s: %d rectangles, packing", project, len(file_data))
        packer.pack()
        logger.info("%s: packing done", project)
        with open(cache_path, "w") as rectf:
            json.dump(packer.rect_list(), rectf)

    rects = json.load(open(cache_path))
    render(rects)


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument("projects", nargs="+")

    def handle(self, *args, **options):
        projects = options["projects"]
        if projects == ["all"]:
            projects = SourceFile.projects()

        for project in projects:
            pack(project)
