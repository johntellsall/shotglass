"""
label.py -- 
"""
# pylint: disable=W0640

# list files in Git branch
# git ls-tree --name-status --full-tree -r v4.0.0

import itertools
import os
import re
import subprocess

from django.core.management.base import BaseCommand
from palettable import colorbrewer
from PIL import Image, ImageDraw, ImageFont

IMAGE_WIDTH = IMAGE_HEIGHT = 1000
COL_WIDTH, COL_HEIGHT = 100, 1000
COL_GAP = 10


def serpentine_iter(width):
    y = 0
    while True:
        for x in xrange(width):
            yield x, y
        for x in xrange(width):
            yield width - x - 1, y + 1
        y += 2


def render_highlight(path):
    output = subprocess.check_output(
        ['source-highlight', '-i', path])
    output = re.compile('^.+<pre><tt>', re.DOTALL).sub('', output)
    return output.split('\n')


class Render(object):
    def __init__(self, draw, x, y):
        self.draw = draw
        self.x, self.y = x, y
        self.symbol_re = re.compile('<(.+?)>([^<]*)')
        self.colors = ['black']

    def add_text(self, text):
        raise NotImplementedError

    def add_line(self, line):
        line = '<x>' + line # process text before HTML
        mgroups = (match.groups() for match in self.symbol_re.finditer(line))
        for sym, text in mgroups:
            if sym.startswith('font '):
                self.colors.append(sym.split('"')[1])
            elif sym == '/font':
                self.colors.pop()
            if text:
                self.add_text(text)
        self.y += 1


# TODO: trim lines outside column (~80)

class RenderSource(Render):
    """
    draw individual source code lines with colors + indent
    """
    def __init__(self, *args, **kwargs):
        self.relx = None
        super(RenderSource, self).__init__(*args, **kwargs)

    def add_line(self, line):
        self.relx = 0
        super(RenderSource, self).add_line(line)

    def add_text(self, text):
        if text.startswith(' '):
            orig_len = len(text)
            text = text.lstrip(' ')
            self.relx += orig_len - len(text)
        self.draw.line(
            (self.x+self.relx,self.y, 
                self.x+self.relx+len(text),self.y),
            fill=self.colors[-1])
        self.relx += len(text) + 1


class RenderFile(Render):
    def add_line(self, line):
        self.draw.line(
            (self.x, self.y, 
                self.x + COL_WIDTH - COL_GAP, self.y),
            fill=self.colors[-1])
        self.y += 1


def render_file(path, renderObj):
    hlines = render_highlight(path)
    for line in hlines:
        renderObj.add_line(line)
        if renderObj.y >= IMAGE_HEIGHT:
            renderObj.y = 0
            renderObj.x += COL_WIDTH


def render_blocks(paths):
    im = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color='white')
    if 1:
        CMAP_OBJ = colorbrewer.qualitative.Set3_12
        CMAP_COLORS = map(tuple, CMAP_OBJ.colors)
        colormap = itertools.cycle(CMAP_COLORS)
        renderClass = RenderFile
        draw = ImageDraw.Draw(im)
        rend = renderClass(draw=draw, x=0, y=0)
        # X: size in points, not pixels
        fnt = ImageFont.truetype('Umpush-Light.ttf', size=14)
    text_color = (0,0,0, 128)
    for path in paths:
        text_args = dict(
            xy=(rend.x, rend.y),
            text=os.path.basename(path),
            font=fnt,
            fill=text_color)
        rend.colors = [colormap.next()]
        render_file(path, rend)
        draw.text(**text_args)
    return im

# XX merge render_source and render_files

def render_source(paths):
    im = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color='white')
    renderClass = RenderSource
    draw = ImageDraw.Draw(im)
    rend = renderClass(draw=draw, x=0, y=0)
    for path in paths:
        render_file(path, rend)
    return im

class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('--style')
        parser.add_argument('paths', nargs='+')

    def handle(self, *args, **options):
        render = render_source
        if options['style'] == 'blocks':
            render = render_blocks
        img = render(paths=options['paths'])
        img.save('{}.png'.format('z'))
