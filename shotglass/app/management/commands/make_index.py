#!/usr/bin/env python

"""
make_index -- compile data from tree of source files
"""

from __future__ import print_function

import logging
import os
import re
import subprocess
import sys

import django.db
from django.core.management.base import BaseCommand

from app.models import SourceFile, Symbol


LANGUAGE_TYPES = {
    ".c": "c",
    ".cc": "c++",
    ".go": "golang",
    ".h": "c",
    ".py": "python",
}
BORING_DIRS = (".pc",)  # TODO: make configurable

logging.basicConfig(
    stream=sys.stderr,
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def format_project_name(project_dir):
    return os.path.basename(project_dir.rstrip("/"))


def test_format_project_name():
    assert format_project_name("/a/b/") == "b"


def walk_type(topdir, name_func):
    "don't scan boring directories"
    for root, dirs, names in os.walk(topdir, topdown=True):
        dirs[:] = [mydir for mydir in dirs if mydir not in BORING_DIRS]
        paths = [os.path.join(root, name) for name in names if name_func(name)]
        for path in paths:
            yield path


def count_lines(project_dir, paths):
    """
    list files in project, with line counts
    """
    cmd = ["wc", "-l"]
    pat = re.compile(r"\s*(\d+)\s+(.+)")

    def is_interesting(args):
        (line_count, path) = args
        return line_count != "0" and path != "total"

    result = subprocess.check_output(cmd + paths, text=True)
    lines = result.split("\n")
    matches = (pat.match(line) for line in lines)
    info = filter(is_interesting, (m.groups() for m in matches if m))
    for num_str, path in info:
        rel_path = path.split(project_dir)[-1].lstrip("/")
        yield int(num_str), rel_path


# TODO speed up by processing mult files at once
# TODO get more info from 'info' and/or more ctags options
# Example symbol:

# info={'kind': 'member', 'line': '288', 'language': 'Python', 'scope':
# 'class:TaggedJSONSerializer', 'access': 'public', 'signature': '(self,
# value)', 'roles': 'def', 'end': '298'}

CTAGS_COMMAND = ["ctags", "--fields=*-P", "--extras=*", "-f", "-",
"--output-format=json"]

def get_ctags_info(path):
    cmd = CTAGS_COMMAND + [path]
    lines = subprocess.check_output(cmd, text=True).split("\n")
    return lines
    
def get_symbols(file_obj, path):
    def parse_addr(symaddr):
        keyvals = symaddr.split(';"', 1)[-1].split("\t")
        keyvals.pop(0)
        return dict(item.split(":", 1) for item in keyvals)

    cmd = CTAGS_COMMAND + [path]
    lines = subprocess.check_output(cmd, text=True).split("\n")
    for line in filter(None, lines):
        try:
            tagname, _, tagaddr = line.split("\t", 2)
        except ValueError:
            sys.exit(f"Unknown line: {line}")
        info = parse_addr(tagaddr)
        yield Symbol(
            source_file=file_obj,
            label=tagname,
            line_number=info.get("line"),
        )


def index_files(project, project_dir, paths):
    num_path_iter = count_lines(project_dir, paths)
    for num, rel_path in num_path_iter:
        name = os.path.split(rel_path)[-1]
        SourceFile.objects.create(
            project=project, name=name, path=rel_path, num_lines=num
        )


def make_index(project, project_dir, replace=True):
    def is_source(path):
        return os.path.splitext(path)[-1] in LANGUAGE_TYPES

    if django.db.connection.vendor == "sqlite":
        django.db.connection.cursor().execute("PRAGMA synchronous=OFF")

    logger.info("project %s, directory %s", project, project_dir)
    if replace:
        logger.info("%s: zapping old data", project)
        SourceFile.objects.filter(project=project).delete()

    logger.info("%s: looking for source", project)
    paths = list(walk_type(project_dir, is_source))
    logger.info("%s: %d source files", project, len(paths))

    index_files(project, project_dir, paths)
    logger.info(
        "%s: indexed %d files",
        project,
        SourceFile.objects.filter(project=project).count(),
    )

    for src_file in SourceFile.objects.filter(project=project):
        src_path = os.path.join(project_dir, src_file.path)
        path_symbols = get_symbols(src_file, src_path)
        Symbol.objects.bulk_create(path_symbols)
    proj_syms = Symbol.objects.filter(source_file__project=project)
    logger.info("%s: indexed %d symbols", project, proj_syms.count())


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument("project_dirs", metavar="FILE", nargs="+")

    def handle(self, *args, **options):
        for project_dir in map(os.path.expanduser, options["project_dirs"]):
            if not os.path.isdir(project_dir):
                logger.warning("%s: project must be directory, skipping", project_dir)
                continue

            # X: doesn't support multiple dirs
            project_name = options.get("project") or format_project_name(project_dir)

            logger.info("%s: start", project_name)
            make_index(project_name, project_dir)

            logger.info("%s: done", project_name)
