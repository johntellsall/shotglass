"""
draw: plot codebase into an image
"""
# pylint: disable=no-member

from django.core.management.base import BaseCommand

from app import draw
from app.models import SourceLine


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument(
            '--draw',
            default='simple',
            help='Set drawing style',
        )
        # DRAW_STYLES.keys()
        #  = {"boundingbox": BoundingBoxDraw, "simple": SimpleDraw}

        parser.add_argument("projects", nargs="+")

    def get_projects(self, projects):
        if projects != ["all"]:
            return projects
        return SourceLine.projects()

    def handle(self, *args, **options):
        themeClass = draw.ThemeRainbow
        themeClass = draw.ThemeZebra
        drawClass = draw.DRAW_STYLES[options['draw']]
        drawFunc = drawClass().draw

        for project in self.get_projects(options["projects"]):
            print("***", project)
            print(f"- draw style: {options['draw']}")
            # grid = draw.SimpleDraw().draw(project, theme=themeClass())
            grid = drawFunc(project, theme=themeClass())

            depth = None
            argname = "path"
            detail = "_{}".format(depth) if depth else ""
            argname2 = argname.split("_")[0]
            path = "{}_{}{}.png".format(project, argname2, detail)
            grid.render(path)
            print(path)
