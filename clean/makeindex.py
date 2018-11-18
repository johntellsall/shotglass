import subprocess
from pathlib import Path

# TODO: raise exception if command failed
def system(cmd):
    print(">>>", cmd)
    out_text = subprocess.getoutput(cmd)
    return out_text.split(r"\n")


class Repos:
    def __init__(self, git_dir):
        maybe_dir = Path(git_dir) / ".git"
        if maybe_dir.is_dir():
            git_dir = maybe_dir
        self.git_dir = git_dir

    def cmd(self, args):
        return ["git", f"--git-dir={self.git_dir}"] + list(args)

    def ls_files(self):
        return system(self.cmd(["ls-files"]))
