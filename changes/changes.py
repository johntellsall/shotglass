# changes.py -- show file changes over time
# - Dnsmasq, 20 samples over 90 releases

import re
import subprocess
import sys
from itertools import pairwise

import run
import state


def is_tag_interesting(tag):
    return re.fullmatch("v[0-9.]+", tag) is not None


def git_tag_list(proj):
    tags = run.git_tag_list(proj)
    tags = [tag for tag in tags if is_tag_interesting(tag)]
    return tags
    # # Pick every tenth tag
    # sampled_tags = tags[::10] # FIXME:
    # return sampled_tags


def count_lines(proj, tag, path):
    """
    count lines in file at given tag
    - 0 = file empty
    - None = file does not exist
    """
    cmd = f"git -C {proj} show '{tag}:{path}'"
    try:
        lines = run.run(cmd)
        return len(lines)
    except subprocess.CalledProcessError as error:
        if error.returncode == 128:
            # file does not exist
            return None
        raise


def git_tag_list_dates(proj):
    """
    get Git tags with dates
    """
    cmd = f"git -C {proj} tag --list --format='%(refname:short) %(creatordate:short)'"
    # Sample input: 'v2.85 2023-10-01'
    lines = run.run(cmd)
    tag_date = {tag: date for tag, date in (line.split() for line in lines)}
    return tag_date


def val_or_sep(value):
    return value if value is not None else "-"


def lines_or_sep(value):
    return f"{value}L" if value is not None else "-"


def OLD_main(paths):
    proj = paths[0]
    tags = git_tag_list(proj)
    print(tags)

    final_tag = tags[-1]
    final_paths = run.git_ls_tree2(proj, final_tag, "src")

    path_linecount = {}
    for path in final_paths:
        path_linecount[path] = count_lines(proj, final_tag, path)

    tag_date = git_tag_list_dates(proj)

    # Dnsmasq: skip tags without dates
    first_tag = tags[0]
    good_index = tags.index("v2.60")
    tags = [first_tag] + tags[good_index:]

    limit_tags = True
    if limit_tags:
        tags = tags[-10:]

    print(f"Tags: {tags}")

    # FIXME: ensure "first version lines" case is handled
    # tag_pairs = list(pairwise(tags))
    # path_rel_diff = {}
    # for src_tag, dest_tag in tag_pairs:
    #     result = git_diff_stat(proj, src_tag, dest_tag, 'src')
    #     for diff in result:
    #         key = (diff['path'], src_tag)
    #         path_rel_diff[key] = diff['diff']

    # change count:
    # - first col is number of lines in first version
    # - other col are number of changes
    # - line change = *two* according to Git: one add, one remove
    first_count = {}
    for path in final_paths:
        first_count[path] = count_lines(proj, first_tag, path)

    if first_tag not in tags:  # FIXME:
        tags = [first_tag] + tags
    tag_pairs = list(pairwise(tags))
    path_rel_diff = {}
    for src_tag, dest_tag in tag_pairs:
        result = run.git_diff_stat(proj, src_tag, dest_tag, "src")
        for diff in result:
            key = (diff["path"], dest_tag)
            path_rel_diff[key] = diff["diff"]

def main(paths):
    db = state.get_db(temporary=True)
    state.setup(db)

    proj = paths[0]
    tags = git_tag_list(proj)
    print(tags)

    final_tag = tags[-1]
    final_paths = run.git_ls_tree2(proj, final_tag, "src")

    path_linecount = {}
    for path in final_paths:
        path_linecount[path] = count_lines(proj, final_tag, path)

    breakpoint()

    tag_date = git_tag_list_dates(proj)

    # Dnsmasq: skip tags without dates
    first_tag = tags[0]
    good_index = tags.index("v2.60")
    tags = [first_tag] + tags[good_index:]

    limit_tags = True
    if limit_tags:
        tags = tags[-10:]

    print(f"Tags: {tags}")

    # FIXME: ensure "first version lines" case is handled
    # tag_pairs = list(pairwise(tags))
    # path_rel_diff = {}
    # for src_tag, dest_tag in tag_pairs:
    #     result = git_diff_stat(proj, src_tag, dest_tag, 'src')
    #     for diff in result:
    #         key = (diff['path'], src_tag)
    #         path_rel_diff[key] = diff['diff']

    # change count:
    # - first col is number of lines in first version
    # - other col are number of changes
    # - line change = *two* according to Git: one add, one remove
    first_count = {}
    for path in final_paths:
        first_count[path] = count_lines(proj, first_tag, path)

    if first_tag not in tags:  # FIXME:
        tags = [first_tag] + tags
    tag_pairs = list(pairwise(tags))
    path_rel_diff = {}
    for src_tag, dest_tag in tag_pairs:
        result = run.git_diff_stat(proj, src_tag, dest_tag, "src")
        for diff in result:
            key = (diff["path"], dest_tag)
            path_rel_diff[key] = diff["diff"]

    SEP = "-"

    # header: tags
    print(f"{"":20}", end=" ")
    for tag in tags:
        print(f"{tag:>6}", end=" ")
    print()

    # header 2nd row: first version line count
    print(f"{"path":20}", end=" ")
    print(f'{"LOC":>6}', end=" ")

    # header 2nd row: dates
    for tag in tags[:-1]:
        date = tag_date.get(tag)
        if date == "2012-01-05":  # NOTE: Dnsmasq special case
            date = None
        if date:
            year_month = "".join(date.split("-")[:2])
            print(f"{year_month}", end=" ")
        else:
            print(f"{SEP:>6}", end=" ")

    # header 2nd row: final line count
    print(f'{"LOC":>6}', end=" ")
    print()

    limit = False
    paths = sorted(final_paths)
    if limit:
        paths = paths[:10]
    for path in paths:
        # first col: file path
        print(f"{path:20}", end=" ")

        # next col: first version line count
        first = first_count.get(path)
        print(f"{lines_or_sep(first):>6}", end=" ")

        # middle: releases with change count
        for tag in tags[:-1]:
            diff = path_rel_diff.get((path, tag))
            if diff:
                print(f"{diff:>6}", end=" ")
            else:
                print(f"{SEP:>6}", end=" ")

        # last col: final version line count
        linecount = path_linecount.get(path, 0)
        print(f"{linecount:>6}L", end=" ")

        print()


if __name__ == "__main__":
    main(sys.argv[1:])
