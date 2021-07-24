import pygments.lexers
from pygments.token import Name, Punctuation

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "beer"

    def add_arguments(self, parser):
        parser.add_argument("paths", nargs="+")

    def handle(self, *args, **options):
        for path in options["paths"]:
            lex = pygments.lexers.get_lexer_for_filename(path)
            name = None
            for tokentype, value in lex.get_tokens(open(path).read()):
                if tokentype is Name:
                    name = value
                elif tokentype is Punctuation and value == "(":
                    print("NAME", name)
                    name = None
