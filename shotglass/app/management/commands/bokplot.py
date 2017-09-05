#!/usr/bin/env python

'''
sparklines -- XX
'''

# pylint: disable=bad-builtin

import logging
import sys

import django.db
from bokeh import plotting as bplot
from django.core.management.base import BaseCommand

from app.models import SourceFile
from app import render


logging.basicConfig(
    stream=sys.stderr,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

def plot2(project):
    query = SourceFile.objects.filter(
        project=project).order_by('path')
    num_lines = query.values_list('num_lines', flat=True)

    bplot.output_file("lines.html")

    # create a new plot with a title and axis labels
    p = bplot.figure(
        title="{} Source".format(project.title()),
        x_axis_label='index', 
        y_axis_label='number of lines')

    y = num_lines
    x = range(y.count())

    # add a line renderer with legend and line thickness
    p.line(x, y, legend="", line_width=2)
    bplot.show(p)

def plot(project):
    WIDTH = 20
    query = SourceFile.objects.filter(project=project).order_by('-num_lines')
    num_lines = query.values_list('num_lines', flat=True)
    largest, num_files = num_lines.first(), num_lines.count()
    print '{project}: {num_files} source files, largest = {largest} lines'.format(
        **locals())

    data = [num_lines[i] for i in range(0, num_files, num_files/WIDTH)]
    print sparklines.sparklines(data)[0]

    print "Largest:"
    for info in query[:10]:
        print info.num_lines, info.path



class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('projects', nargs='+')

    def handle(self, *args, **options):
        projects = options['projects']
        if projects == ['all']:
            projects = SourceFile.projects()

        for project in projects:
            print 'PROJECT {}:'.format(project.upper())
            plot2(project)
