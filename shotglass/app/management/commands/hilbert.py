import math
import sys
from collections import Counter

import ctags
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Avg, Max, Sum
from PIL import Image, ImageColor, ImageDraw

from app.models import SourceLine

# from http://fundza.com/algorithmic/space_filling/hilbert/basics/index.html
# Andrew Cumming
def hilbert(x, y, xi, xj, yi, yj, n, lineto):
    # x and y are the coordinates of the bottom left corner
    # xi & xj are the i & j components of the unit x vector of the frame
    # similarly yi and yj
    if n <= 0:
        lineto(x + (xi + yi)/2., y + (xj + yj)/2.)
        return
    hilbert(x,           y,           yi/2., yj/2.,  xi/2.,  xj/2., n-1, lineto)
    hilbert(x+xi/2.,      y+xj/2. ,     xi/2., xj/2.,  yi/2.,  yj/2., n-1, lineto)
    hilbert(x+xi/2.+yi/2., y+xj/2.+yj/2, xi/2., xj/2.,  yi/2.,  yj/2., n-1, lineto)
    hilbert(x+xi/2.+yi,   y+xj/2.+yj,  -yi/2.,-yj/2., -xi/2., -xj/2., n-1, lineto)

class Command(BaseCommand):
    help = 'beer'

    def handle(self, *args, **options):
        def lineto_print(x, y):
            print x,y
        num = 1
        hilbert(0., 0., 1., 0., 0., 1.,
                num, lineto_print)
