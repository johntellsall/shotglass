import subprocess
import sys


def cmd_import(path):
    cmd = "git ls-tree -r --long '2.0.0'"
    cmd = f"git -C {path} ls-tree  -r --long '2.0.0'"
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
    # if verbose:
    #     print(f"-- RAW\n{proc.stdout[:300]}\n-- ENDRAW")
    assert 0, proc.stdout


if __name__ == "__main__":
    cmd_import(sys.argv[1])
