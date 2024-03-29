"""
spider.py --
"""
# pylint: disable=W0640

# list files in Git branch
# git ls-tree --name-status --full-tree -r v4.0.0


import itertools
import os
import re
import subprocess

import click
from palettable import colorbrewer
from PIL import Image, ImageDraw

IMAGE_WIDTH = 1000
IMAGE_HEIGHT = 1000
COL_WIDTH, COL_HEIGHT = 100, 1000
COL_GAP = 10

# https://www.gnu.org/software/src-highlite/
CMD_SOURCE_HIGHLIGHT = "source-highlight"


def render_highlight(path):
    cmd = [CMD_SOURCE_HIGHLIGHT, "-i", path]
    output = subprocess.check_output(cmd, text=True)
    output = re.compile("^.+<pre><tt>", re.DOTALL).sub("", output)
    return output.split("\n")


def get_colormap():
    cmap_obj = colorbrewer.qualitative.Set3_12
    cmap_colors = list(map(tuple, cmap_obj.colors))
    return itertools.cycle(cmap_colors)


class Render(object):
    def __init__(self, draw, x, y):
        self.draw = draw
        self.x, self.y = x, y
        self.symbol_re = re.compile("<(.+?)>([^<]*)")
        self.colors = ["black"]

    def add_text(self, text):
        raise NotImplementedError

    def add_line(self, line):
        line = "<x>" + line  # process text before HTML
        mgroups = (match.groups() for match in self.symbol_re.finditer(line))
        for sym, text in mgroups:
            if sym.startswith("font "):
                self.colors.append(sym.split('"')[1])
            elif sym == "/font":
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
        if text.startswith(" "):
            orig_len = len(text)
            text = text.lstrip(" ")
            self.relx += orig_len - len(text)
        self.draw.line(
            (self.x + self.relx, self.y, self.x + self.relx + len(text), self.y),
            fill=self.colors[-1],
        )
        self.relx += len(text) + 1


class RenderFile(Render):
    def add_line(self, line):
        self.draw.line(
            (self.x, self.y, self.x + COL_WIDTH - COL_GAP, self.y), fill=self.colors[-1]
        )
        self.y += 1


def render_file(path, renderObj):
    hlines = render_highlight(path)
    for line in hlines:
        renderObj.add_line(line)
        if renderObj.y >= IMAGE_HEIGHT:
            renderObj.y = 0
            renderObj.x += COL_WIDTH


def render_blocks(image, paths):
    """
    draw each file as a colored block, annotated with filename
    """
    if 1:
        CMAP_OBJ = colorbrewer.qualitative.Set3_12
        CMAP_COLORS = list(map(tuple, CMAP_OBJ.colors))
        colormap = itertools.cycle(CMAP_COLORS)
        renderClass = RenderFile
        draw = ImageDraw.Draw(image)
        rend = renderClass(draw=draw, x=0, y=0)
        # X: size in points, not pixels
        # fnt = ImageFont.truetype("Umpush-Light.ttf", size=14)
        fnt = None
    text_color = (0, 0, 0, 128)
    for path in paths:
        text_args = dict(
            xy=(rend.x, rend.y), text=os.path.basename(path), font=fnt, fill=text_color
        )
        rend.colors = [next(colormap)]
        render_file(path, rend)
        draw.text(**text_args)
    return image


# TODO: merge render_* functions


def render_source(image, paths):
    """
    draw each line of source one pixel high, syntaxed colored, like a compressed minimap
    """
    renderClass = RenderSource
    draw = ImageDraw.Draw(image)
    rend = renderClass(draw=draw, x=0, y=0)
    for path in paths:
        render_file(path, rend)


@click.command()
@click.option("--output", default="z.png")
@click.option("--style", default="source")
@click.argument("paths", nargs=-1)
def spider(output, style, paths):
    click.secho("Hello!", fg="yellow")
    im = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), color="white")
    render = render_source
    if style == "blocks":
        render = render_blocks

    render(image=im, paths=paths)
    im.save(output)
    print(f"{output}: image written")


if __name__ == "__main__":
    spider()
