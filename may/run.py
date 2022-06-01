# run.py
"run commands, espectially Ctags"

import json
import subprocess

# Universal Ctags
CTAGS_ARGS = "ctags --output-format=json --fields=*-P -o -".split()


def run_ctags(path, verbose=False):
    "Ctags command output -- iter of dictionaries, one per symbol"
    cmd = CTAGS_ARGS + [path]
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
