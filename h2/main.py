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


def git_get_file(project_path, release, file_path) -> list[str]:
    "get contents of a file in a given release -- lines"
    cmd = f"git -C {project_path} show '{release}:{file_path}'"
    return run(cmd)


# def git_ls_files(proj, tag, filepat):
#     cmd = f"git -C {proj} ls-files '{tag}' -- '{filepat}'"
#     return run(cmd)


class GitRepo:
    def __init__(self, path):
        self.path = path
        self.name = Path(path).name

    def ls_tree(self, release):
        return git_ls_tree(self.path, release)

    def tag_list(self):
        return git_tag_list(self.path)

    # def ls_files(self, tag, filepat):
    #     return git_ls_files(self.path, tag, filepat)
    

def import_project(db, repo, release):
    """
    - project record (name)
    - file records (project_id, release, path, num_bytes)
    """
    query(db, f'insert into project (name) values ("{repo.name}")')
    db.commit()
    project_id = query1(db, f'select id from project where name = "{repo.name}"')

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


def project_mod_numlines(repo, db, project_id, release):
    path_id_map = query(db, f'select path, id from file where project_id = {project_id} and release = "{release}"')
    path_id_map = dict(path_id_map)
    
    for path, path_id in path_id_map.items():
        lines = git_get_file(repo.path, release, path)
        num_lines = len(lines)
        query(db, f'update file set num_lines = {num_lines} where id = {path_id}')
    db.commit()


def main():
    db = dbsetup()
    repo = GitRepo('../SOURCE/dnsmasq')
    proj_name = repo.name
    release = 'HEAD'

    import_project(db, repo, release)

    count = query1(db, 'select count(*) from file')
    size = query1(db, 'select sum(num_bytes) from file')
    print(f"Found {count} files in release {release}, total size {size} bytes")

    project_id = query1(db, f'select id from project where name = "{proj_name}"')
    project_mod_numlines(repo, db, project_id, release)

    total = query1(db, 'select sum(num_lines) from file')
    print(f"Total lines of code in release {release}: {total}")

    min_lines, max_lines = query(db, 'select min(num_lines), max(num_lines) from file')[0]
    print(f"Min lines: {min_lines}, Max lines: {max_lines}")

    
if __name__ == "__main__":
    main()
