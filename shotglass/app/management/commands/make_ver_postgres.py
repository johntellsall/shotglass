"""
make_versions -- index many versions of a project

ALPHA code, will need modification for general use.
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
    def __init__(self, name, bad_tag_pat=None, good_tag_pat=None):
        self.name = name
        self.proj_dir = "SOURCE/{}".format(name)
        self.good_tag_re = re.compile(good_tag_pat)
        self.bad_tag_re = re.compile("never-match")
        if bad_tag_pat:
            self.bad_tag_re = re.compile(bad_tag_pat)

    def get_tags(self):
        repos = git.Repo(self.proj_dir)
        tags = filter(self.good_tag_re.search, (tag.name for tag in repos.tags))
        tags = itertools.ifilterfalse(self.bad_tag_re.search, tags)
        tags = natsorted(tags)
        return tags


class Command(BaseCommand):
    help = "beer"

    # def add_arguments(self, parser):
    #     parser.add_argument('projects', nargs='*')
    #     parser.add_argument('--index', action="store_true")

    def handle(self, *args, **options):
        proj = Project(
            "postgres",
            good_tag_pat="^REL",
            bad_tag_pat="(ALPHA|BETA|RC|REL2_0"
            "|[^9]_._[^0]"  # < v9.0, skip micro changes
            ")",
        )
        tags = proj.get_tags()
        # tags = tags[:3]

        proj_versions = set(
            models.SourceLine.objects.filter(
                project__startswith="postgres-"
            ).values_list("project", flat=True)
        )
        have_tags = set(projvers.split("-", 1)[1] for projvers in proj_versions)

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
            out = subprocess.check_output(cmd, shell=True)
            print out
