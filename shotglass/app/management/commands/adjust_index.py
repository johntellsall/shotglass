from django.core.management.base import BaseCommand

from app.models import SourceLine


class Command(BaseCommand):
    help = "beer"

    def add_arguments(self, parser):
        parser.add_argument("--project")
        # parser.add_argument('--prefix', default='')
        # parser.add_argument('--verbose', action='store_true')

    def handle(self, *args, **options):
        project = options["project"]
        lines = SourceLine.objects.filter(project=project).order_by("path")
        print(f"LINES: {project=}")
        for line in lines:
            print((vars(lines)))
        # prefix = options['prefix']
        # rows = []
        # while True:
        #     if entry['kind']:
        #         path = entry['file']
        #         if prefix and path.startswith(prefix):
        #             path = path[len(prefix):].lstrip('/')
        #         length = 123
        #         rows.append(SourceLine(name=entry['name'],
        #                                project=options['project'],
        #                                path=path,
        #                                line_number=entry['lineNumber'],
        #                                length=length,
        #                                kind=entry['kind']))
        #         if options['verbose']:
        #             print rows[-1].__dict__
        #     status = tagFile.findNext(entry)
        #     if not status:
        #         break
        # SourceLine.objects.bulk_create(rows)
