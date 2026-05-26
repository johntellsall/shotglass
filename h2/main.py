from pathlib import Path
import subprocess

from model import dbsetup, query, query1


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


# def git_ls_files(proj, tag, filepat):
#     cmd = f"git -C {proj} ls-files '{tag}' -- '{filepat}'"
#     return run(cmd)


class GitRepo:
    def __init__(self, path):
        self.path = path

    def ls_tree(self, release):
        return git_ls_tree(self.path, release)

    def tag_list(self):
        return git_tag_list(self.path)

    # def ls_files(self, tag, filepat):
    #     return git_ls_files(self.path, tag, filepat)
    

def main():
    db = dbsetup()
    repo = GitRepo('../SOURCE/dnsmasq')
    release = 'HEAD'

    query(db, 'insert into project (name) values ("dnsmasq")')
    project_id = query1(db, 'select id from project where name = "dnsmasq"')

    def is_interesting(path):
        suffix = Path(path).suffix
        return suffix in {'.c', '.h', '.go', '.py'}

    tree = repo.ls_tree(release)
    items = [item for item in tree if is_interesting(item['path'])]
    rows = [(item['path'], item['size_bytes']) for item in items]
    sql = ('insert into file'
           ' (project_id, release, path, num_bytes)'
           f' values ({project_id}, "{release}", ?, ?)'
    )
    db.executemany(sql, rows)
    db.commit()

    count = query1(db, 'select count(*) from file')
    print(f"Found {count} files in release {release}")


if __name__ == "__main__":
    main()
