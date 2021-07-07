# pylint: disable=no-member

from django.core.management.base import BaseCommand

from app import draw
from app.models import SourceLine


class Command(BaseCommand):
    help = "beer"

    def add_arguments(self, parser):
        parser.add_argument("projects", nargs="+")

    def get_projects(self, projects):
        if projects != ["all"]:
            return projects
        return SourceLine.projects()

    def handle(self, *args, **options):
        themeClass = draw.ThemeRainbow
        for project in self.get_projects(options["projects"]):
            print("***", project)
            grid = draw.SimpleDraw().draw(project, theme=themeClass())

            depth = None
            argname = "path"
            detail = "_{}".format(depth) if depth else ""
            argname2 = argname.split("_")[0]
            path = "{}_{}{}.png".format(project, argname2, detail)
            grid.render(path)
            print(path)
