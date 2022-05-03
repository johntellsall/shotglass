# run.py


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
    if 1:
        # return map(json.loads, proc.stdout.rstrip().split("\n"))
        return map(json.loads, filter(None, proc.stdout.rstrip().split("\n")))

    else:

        def safe_loads(json_str):
            try:
                return json.loads(json_str)
            except json.decoder.JSONDecodeError:
                assert 0, json_str
                print(f"??? {json_str[:50]}")

        return filter(None, map(safe_loads, proc.stdout.rstrip().split("\n")))


def run_blob(cmd):
    proc = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, check=True
    )  # noqa: E501
    return proc.stdout


def run(cmd):
    out_blob = run_blob(cmd)
    out_lines = out_blob.rstrip("\n").split("\n")
    return out_lines
