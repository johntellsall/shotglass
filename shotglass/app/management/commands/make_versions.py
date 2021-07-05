"""
make_versions -- index many versions of a project


USAGE:
* list project's tags that match patterns:

Ex: show each minor version of Django; just output tags. Hide RC, Alpha and micro-change versions:
./manage.py make_versions --info --exclude='([abc])' --include='\.1$' \
./SOURCE/django/ 

['1.0.1', '1.1', '1.1.1', ...  '1.10.1']
"""

import itertools
import re
import subprocess
import sys

import git
from django.core.management.base import BaseCommand
from natsort import natsorted

from app import models


class Project(object):
    def __init__(self, name, proj_dir, bad_tag_pat=None, good_tag_pat=None):
        self.name = name
        self.proj_dir = proj_dir
        self.good_tag_re = re.compile(good_tag_pat) if good_tag_pat else None
        self.bad_tag_re = re.compile(bad_tag_pat) if bad_tag_pat else None

    def get_tags(self):
        repos = git.Repo(self.proj_dir)
        tags = (tag.name for tag in repos.tags)
        if self.good_tag_re:
            tags = filter(self.good_tag_re.search, tags)
        if self.bad_tag_re:
            tags = itertools.ifilterfalse(self.bad_tag_re.search, tags)
        tags = natsorted(tags)
        return tags


def make_project(proj, dryrun=False, limit=None):
    tags = proj.get_tags()
    if limit:
        tags = tags[:limit]

    proj_prefix = "{}-".format(proj.name)
    proj_versions = set(
        models.SourceLine.objects.filter(project__startswith=proj_prefix).values_list(
            "project", flat=True
        )
    )
    have_tags = set(projvers.split("-", 1)[1] for projvers in proj_versions)
    have_tags = set()  # XX

    checkout_cmd = "cd {dir} ; git checkout {tag}"
    index_cmd = "./manage.py make_index --project={name}-{tag} {dir}"
    for tag in tags:
        if tag in have_tags:
            print "(have {}, skipping)".format(tag)
            continue
        cmd = checkout_cmd.format(dir=proj.proj_dir, tag=tag)
        print ">>>", cmd
        if subprocess.call(cmd, shell=True):
            sys.exit(0)
        cmd = index_cmd.format(dir=proj.proj_dir, name=proj.name, tag=tag)
        print ">>>", cmd
        if dryrun:
            continue
        out = subprocess.check_output(cmd, shell=True)
        print out


class Command(BaseCommand):
    help = "beer"

    def add_arguments(self, parser):
        parser.add_argument("projects", nargs=1)
        parser.add_argument("--dryrun", action="store_true")
        parser.add_argument("--info", action="store_true")
        parser.add_argument("--include")
        parser.add_argument("--exclude")
        parser.add_argument("--limit", type=int)
        parser.add_argument("--name")

    def handle(self, *args, **options):
        assert len(options["projects"]) == 1
        assert options["name"]

        projects = [
            Project(
                name=options["name"],
                proj_dir=options["projects"][0],
                good_tag_pat=options["include"],
                bad_tag_pat=options["exclude"],
            )
        ]

        if options["info"]:
            for proj in projects:
                print proj, ":"
                print proj.get_tags()
            return

        for proj in projects:
            make_project(proj, dryrun=options["dryrun"], limit=options["limit"])
