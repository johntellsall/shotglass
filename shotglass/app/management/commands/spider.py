"""
label.py -- 
"""
# pylint: disable=W0640

# list files in Git branch
# git ls-tree --name-status --full-tree -r v4.0.0

import re
import subprocess

from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw

IMAGE_WIDTH = IMAGE_HEIGHT = 1000
COL_WIDTH, COL_HEIGHT = 100, 1000
# COL_GAP = 10


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
        raise NotImplmentedError

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


def render(path):
    hlines = render_highlight(path)
    im = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color='white')
    rend = RenderSource(draw=ImageDraw.Draw(im), x=0, y=0)
    for line in hlines:
        rend.add_line(line)
        if rend.y >= IMAGE_HEIGHT:
            rend.y = 0
            rend.x += COL_WIDTH
    return im


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('paths', nargs='+')

    def handle(self, *args, **options):
        for path in options['paths']:
            img = render(path)
            img.save('{}.png'.format('z'))
