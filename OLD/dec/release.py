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
    """
    for given project and Git release tag, count how many files

    See also: git ls-tree -r --name-only 1.0
    """
    git_dir = path / ".git"
    cmd = ["git", "-C", git_dir, "ls-tree", "-r", "--name-only", release]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    # TODO: check, might be off by one
    return len(proc.stdout.split("\n"))


def get_git_date(proj_path, file_path, release="HEAD"):
    """
    return file's date (Author)
    Returns None if file not found.
    """
    git_dir = proj_path / ".git"
    cmd = ["git", "-C", str(git_dir), "log", "--format=%ai", "-1", "--", file_path]
    print(f">>> {' '.join(cmd)}")
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    lines = proc.stdout.split("\n")
    # detect file not found
    if lines == [""]:
        return None
    assert len(lines) == 2
    assert not lines[-1]
    date_str = lines[0].split(" ", 1)[0]
    return datetime.strptime(date_str, "%Y-%m-%d")


# X: doesn't work:
# return datetime.fromisoformat(date_iso)
