import subprocess
from pathlib import Path


class Repos:
    def __init__(self, git_dir):
        maybe_dir = Path(git_dir) / ".git"
        if maybe_dir.is_dir():
            git_dir = maybe_dir
        self.git_dir = git_dir

    def cmd(self, args):
        return ["git", f"--git-dir={self.git_dir}"] + list(args)

    def ls_files(self):
        return subprocess.getoutput(cmd=self.cmd(["ls-files"]))
