import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime


majormin_pat = re.compile(
    r"(?P<pre>      .*?)"  # optional before major
    r"(?P<majormin> [0-9]+\.[0-9]+)"  # major.minor ex "1.2"
    r"(?P<post>     .*)",  # optional micro and afterwards
    re.VERBOSE,
)


@dataclass
class Release:
    raw_label: str
    majormin: str = field(init=False)
    pre: str = field(init=False)
    post: str = field(init=False)
    raw_date: str
    date: datetime = field(init=False, default=None)

    def __post_init__(self):
        self.majormin = None
        if match := majormin_pat.search(self.raw_label):
            # TODO: hoist so able to have custom ignore
            self.pre = match.group("pre")
            self.post = match.group("post")
            # if post and not post.startswith(".0"):
            #     # print(f"Ignore micro ({self.raw_label}=)")
            #     return
            self.majormin = match.group("majormin")
        else:
            print(f"No major.minor ({self.raw_label}=)")
            return

        self.date = datetime.strptime(self.raw_date, "%Y-%m-%d")


def count_release_files(path, release):
    # git ls-tree -r --name-only 1.0
    git_dir = path / ".git"
    cmd = ["git", "-C", git_dir, "ls-tree", "-r", "--name-only", release]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    # TODO: check, might be off by one
    return len(proc.stdout.split("\n"))
