#!/usr/bin/env python

import logging
import re
import sys

from django.core.management.base import BaseCommand

from app.models import DiagramSymbol


logging.basicConfig(
    format="%(asctime)-15s %(levelname)-8s %(message)s",
    stream=sys.stderr,
    level=logging.DEBUG)

# disable db query logs
logging.getLogger('django.db.backends').propagate = False
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'beer'

    def add_arguments(self, parser):
        pass # parser.add_argument('projects', nargs='+')

    def handle(self, *args, **options):
        symbols = DiagramSymbol.objects.order_by(
        'sourceline__name')
        for symbol in symbols:
            print symbol.color, symbol.sourceline.name
