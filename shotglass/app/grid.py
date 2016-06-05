import math

from django.db.models import Sum
from PIL import Image, ImageDraw

from app.models import SourceLine


def calc_width(project):
    lines_total = SourceLine.objects.filter( # pylint: disable=no-member
        project=project).aggregate(Sum('length'))['length__sum']
    if not lines_total:
        print 'WARNING: {} is empty'.format(project)
        return 0
    return int(math.sqrt(lines_total) + 1)


class Grid(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, xy, color):
        print 'draw: {}, {}'.format(xy, color)

    def drawto(self, xy, color):
        print 'drawto: {}, {}'.format(xy, color)

    def get_symbol_color(self, symbol):
        return symbol.name[0]

    def finalize(self):
        pass

    def moveto(self, xy):
        pass

    def render(self, *args):
        pass

class TextGrid(Grid):
    def __init__(self, width, height):
        self.blank_row = ['.'] * width
        self.data = []
        super(TextGrid, self).__init__(width, height)

    def draw(self, xy, color):
        x,y = xy
        if y >= len(self.data):
            self.data.append(self.blank_row[:])
        try:
            self.data[y][x] = color
        except IndexError:
            pass

    def render(self, *args):
        for row in self.data:
            print ''.join(row)


class ImageGrid(Grid):
    @classmethod
    def FromProject(cls, project):
        size = calc_width(project)
        size *= 4  # XX?
        return cls(size, size)

    def __init__(self, width, height):
        self.im = Image.new('RGB', (width, height))
        self.im_draw = ImageDraw.Draw(self.im)
        self.last = (0, 0)
        super(ImageGrid, self).__init__(width, height)

    def moveto(self, xy):
        self.last = (xy[0]*2, xy[1]*2)

    def draw(self, xy, pen):
        self.im_draw.point((xy[0]*2, xy[1]*2), pen)

    def drawto(self, xy, pen):
        xy = (xy[0]*2, xy[1]*2)
        if self.last:
            self.im_draw.line((self.last, xy), pen)
        self.last = xy

    def draw_many(self, xy_iter, pen):
        self.moveto(xy_iter.next())
        for xy in xy_iter:
            self.drawto(xy, pen)

    def finalize(self):
        self.im = self.im.crop(self.im.getbbox())

    def render(self, path, *args):
        self.im.save(path)

