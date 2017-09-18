#!/usr/bin/env python

'''
sparklines -- XX
'''

# pylint: disable=bad-builtin

import logging
import sys

import django.db
import numpy as np
import sparklines
from bokeh import plotting as bplot
from bokeh.models import HoverTool
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from django.core.management.base import BaseCommand

from app import render
from app.models import SourceFile


logging.basicConfig(
    stream=sys.stderr,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


def s_color(project):
    TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"

    query = SourceFile.objects.filter(project=project)
    sizes = query.values_list('num_lines', flat=True)
    from django.db.models import Max
    size_max = query.all().aggregate(Max('num_lines')).get(
        'num_lines__max')
    def mysize(num):
        return min(num, 500) # XX

    N = len(sizes)
    print 'num: {}, max: {}'.format(N, size_max)
    hover = HoverTool(tooltips=[
        ("name", "@name"),
        ("lines", "@num_lines"),
        ])
    x = np.random.random(size=N) * 100
    y = np.random.random(size=N) * 100
    radii = [mysize(sizes[i])/500*3 for i in range(N)]
    colors = [
        "#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(50+2*x, 30+2*y)
    ]
    # XX hover?
    source = ColumnDataSource(data=dict(
        x=x,
        y=y,
        fill_color=colors,
        num_lines=query.values_list('num_lines', flat=True),
        name=query.values_list('name', flat=True),
        radius=radii
        ))
    # XX p = figure(tools=TOOLS)
    p = figure(tools=[hover])

    p.scatter(
        'x', 'y', 
        fill_color='fill_color',
        name='name',
        radius='radius',
        source=source,
        fill_alpha=0.6,
        line_color=None,
        )

    outpath = "{}.html".format(project)
    output_file(outpath, title="{}".format(project))
    show(p)


def s_plot(project):
    query = SourceFile.objects.filter(
        project=project).order_by('path')
    num_lines = query.order_by('-num_lines').values_list('num_lines', flat=True)

    outpath = "{}.html".format(project)
    bplot.output_file(outpath)

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
    print(outpath)


def s_spark(project):
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
        parser.add_argument('--style', default='color')

    def handle(self, *args, **options):
        projects = options['projects']
        if projects == ['all']:
            projects = SourceFile.projects()

        try:
            style_fname = 's_{}'.format(options['style'])
            plotfunc = globals()[style_fname]
        except KeyError:
            sys.exit("{}: unknown style".format(options['style']))

        for project in projects:
            print 'PROJECT {}:'.format(project.upper())
            plotfunc(project)
