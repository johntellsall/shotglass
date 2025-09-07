# run.py
"run commands, especially Ctags"

import json
import re
import subprocess

# Universal Ctags
CTAGS_ARGS = "ctags --output-format=json --fields=*-P -o -".split()


def run_ctags(paths, verbose=False):
    "Ctags command output -- iter of dictionaries, one per symbol"
    if type(paths) == str:
        paths = [paths]
    cmd = CTAGS_ARGS + list(paths)
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    assert proc.returncode == 0
    if verbose:
        print(f"-- RAW\n{proc.stdout[:300]}\n-- ENDRAW")

    return map(json.loads, filter(None, proc.stdout.rstrip().split("\n")))


def run_blob(cmd):
    "run command, return stdout as string"
    proc = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, check=True
    )  # noqa: E501
    return proc.stdout


def run(cmd):
    "run command, return stdout split into lines"
    out_blob = run_blob(cmd)
    out_lines = out_blob.rstrip("\n").split("\n")
    return out_lines


def git_ls_tree(project_path, release):
    """
    get Git info about all files in given release
    """

    def to_item(row):
        pre, path = row.split("\t")
        _mode, _type, filehash, size_bytes = pre.split()
        return dict(hash=filehash, path=path, size_bytes=size_bytes)

    cmd = f"git -C {project_path} ls-tree  -r --long '{release}'"
    try:
        return map(to_item, run(cmd))
    except subprocess.CalledProcessError as error:
        print(f"?? {cmd} -- {error}")
        return []


def git_tag_list(project_path):
    "list Git tags (~ releases)"
    return run(f"git -C {project_path} tag --list")


def git_ls_tree2(proj, tag, filepat):
    cmd = f"git -C {proj} ls-tree -r --name-only '{tag}' {filepat}"
    return run(cmd)


def git_diff_stat(proj, tag1, tag2, filepat):
    cmd = f"git -C {proj} diff --stat '{tag1}' '{tag2}' -- {filepat}"
    # Sample input: ' src/arp.c            |    8 +-'
    stat_pat = re.compile(
        r"""
                          (?P<path>\S+) 
                          [\s|]+ # whitespace or pipe
                          (?P<diff>\d+)
                          """,
        re.VERBOSE,
    )

    def parse(line):
        if "changed," in line:
            return None
        match = stat_pat.search(line)
        if match:
            return match.groupdict()
        return None

    lines = run(cmd)
    result = [parse(line) for line in lines]
    result = [item for item in result if item is not None]
    return result


def git_count_lines(proj, tag, path):
    """
    count lines in file at given tag
    - 0 = file empty
    - None = file does not exist
    """
    cmd = f"git -C {proj} show '{tag}:{path}'"
    try:
        lines = run(cmd)
        return len(lines)
    except subprocess.CalledProcessError as error:
        if error.returncode == 128:
            # file does not exist
            return None
        raise