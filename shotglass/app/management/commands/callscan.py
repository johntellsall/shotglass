import re
import sys

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'beer'

    def add_arguments(self, parser):
        parser.add_argument('paths', nargs='+')
        # parser.add_argument('--index', action="store_true")

    def handle(self, *args, **options):
		call_pat = re.compile(r'(\w+)\(')
		for path in options['paths']:
			for lineno,line in enumerate(open(path).readlines()):
				print '\t', lineno, line.rstrip()
				call = call_pat.search(line)
        		if not call:
        			print '?', line.rstrip()
        			continue
        		use_type = 'CALL' if 'def' not in line else 'DEF'
        		print path, lineno, line, use_type, call.group(1)
