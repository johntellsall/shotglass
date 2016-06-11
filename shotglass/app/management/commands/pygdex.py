import sys

import pygments.lexers
from pygments.token import Name, Punctuation

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'beer'

    def add_arguments(self, parser):
        parser.add_argument('paths', nargs='+')
        # parser.add_argument('--index', action="store_true")

    def handle(self, *args, **options):
        for path in options['paths']:
			lex = pygments.lexers.get_lexer_for_filename(path)
			name = None
			for tokentype, value in lex.get_tokens(open(path).read()):
				if tokentype is Name:
					name = value
				elif tokentype is Punctuation and value == '(':
					print 'NAME', name
					name = None


			# import ipdb ; ipdb.set_trace()

