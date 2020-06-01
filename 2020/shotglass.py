import csv
import glob
import re
import subprocess
import sys
from pathlib import Path


def source(name):
    return Path(f'../SOURCE/{name}')


def system(cmd):
    return subprocess.run(cmd,
                          capture_output=True,
                          check=True,
                          universal_newlines=True)


def format_cmd_git(project_dir):
    git_dir = Path(project_dir) / ".git"
    if not git_dir.exists():
        raise ValueError("Git dir missing")
    return ['git', f'--git-dir={git_dir}']


def cmd_git(project_dir, *args):
    return format_cmd_git(project_dir) + list(args)


def cmd_git_list_all_directories(project_dir, tag):
    return format_cmd_git(project_dir) + ['ls-tree', '-dr', tag]


def cmd_git_list_all_files(project_dir, tag):
    return format_cmd_git(project_dir) + ['ls-tree', '-r', tag]


def cmd_git_list_date_tags(project_dir):
    return format_cmd_git(project_dir) + [
        'log', '--date-order', '--graph', '--tags', '--simplify-by-decoration',
        '--pretty=format:"%ai %d"'
    ]


def parse_git_list(proc):
    date_tag_pat = re.compile(
        r'[^0-9]* (?P<date>[0-9-]{10}) .+'
        r' tag:. (?P<tag>[^,)]+)', re.VERBOSE)
    lines = proc.stdout.splitlines()
    matches = map(date_tag_pat.search, lines)
    return [m.groupdict() for m in matches if m]
