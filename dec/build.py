"""
USAGE

shotglass.py <command> <project path>
"""

import logging
import sys
from datetime import datetime

import git

from cmd_index import cmd_ctags, cmd_index, cmd_setup  # pylint: disable=unused-import
from cmd_releases import cmd_releases  # pylint: disable=unused-import
from cmd_info_show import cmd_info, cmd_pinfo, cmd_show  # pylint: disable=unused-import
from cmd_render import cmd_render  # pylint: disable=unused-import

# Universal Ctags
CTAGS_ARGS = "ctags --output-format=json --fields=*-P -o -".split()

logging.basicConfig(format="%(asctime)-15s %(message)s", level=logging.INFO)


def format_summary(tags):
    return {"num_tags": len(tags)}


def format_tstamp(ts):
    return datetime.fromtimestamp(ts).strftime("%c")


def get_usage():
    cmd_list = [name for name in globals() if name.startswith("cmd_")]
    usage = [__doc__, f"Commands: {cmd_list}"]
    return "\n".join(usage)


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


def cmd_dec(project_path):
    def is_release(tag):
        return tag.name.startswith("v")

    repo = git.Repo(project_path)
    release_tags = filter(is_release, repo.tags)
    names = [t.name for t in release_tags]
    assert "v4.5.1" in names
    assert len(names) > 10
    print("okay")


def main():
    try:
        cmd = sys.argv[1]
        project = sys.argv[2]
        cmd_func = globals()[f"cmd_{cmd}"]
    except (KeyError, IndexError):
        sys.exit(get_usage())

    cmd_func(project)


if __name__ == "__main__":
    main()
