import json
import os
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


def git_get_file_by_hash(project_path, file_hash) -> str:
    "get contents of a file by hash -- blob"
    cmd = f"git -C {project_path} cat-file -p '{file_hash}'"
    return run_blob(cmd)


def git_extract_file(project_path, file_hash, suffix) -> Path:
    """
    extract a file by hash
    - caller responsible for deleting the file when done
    """
    output_path = Path(f"/tmp/{file_hash}{suffix}")
    cmd = f"git -C {project_path} cat-file -p '{file_hash}' > '{output_path}'"
    subprocess.run(cmd, shell=True, check=True)
    return output_path


# Universal Ctags
CTAGS_ARGS = "ctags --output-format=json --fields=*-P -o -".split()


def run_ctags(path: Path, verbose=False):
    "Ctags command output -- iter of dictionaries, one per symbol"
    cmd = CTAGS_ARGS + [str(path)]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    assert proc.returncode == 0
    if verbose:
        print(f"-- RAW\n{proc.stdout[:300]}\n-- ENDRAW")

    return map(json.loads, filter(None, proc.stdout.rstrip().split("\n")))


class GitRepo:
    def __init__(self, path):
        self.path = path
        self.name = Path(path).name

    def ls_tree(self, release):
        return git_ls_tree(self.path, release)

    def tag_list(self):
        return git_tag_list(self.path)


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
    rows = [(item['path'], item['size_bytes'], item['hash']) for item in items]
    sql = ('insert into file'
           ' (project_id, release, path, num_bytes, hash)'
           f' values ({project_id}, "{release}", ?, ?, ?)'
    )
    db.executemany(sql, rows)
    db.commit()


def project_mod_numlines(repo, db, project_id, release):
    path_id_map = query(db, f'select path, id from file where project_id = {project_id} and release = "{release}"')
    path_id_map = dict(path_id_map)
    
    tree = repo.ls_tree(release)

    for path, path_id in path_id_map.items():
        lines = git_get_file(repo.path, release, path)
        num_lines = len(lines)
        query(db, f'update file set num_lines = {num_lines} where id = {path_id}')
    db.commit()


def project_add_symbols(repo, db, project_id, release):
    path_list = query(db, f'select path, id, hash from file where project_id = {project_id} and release = "{release}"')

    for path, path_id, filehash in path_list:
        suffix = Path(path).suffix
        outpath = git_extract_file(repo.path, filehash, suffix)
        symbols = run_ctags(outpath)
        os.unlink(outpath)

        rows = []
        for sym in symbols:
            kind = sym.get('kind')
            start_line = sym.get('line')
            end_line = sym.get('end')
            rows.append((path_id, kind, start_line, end_line))
        sql = ('insert into symbol'
               ' (file_id, kind, start_line, end_line)'
               ' values (?, ?, ?, ?)'
        )
        db.executemany(sql, rows)
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

    project_add_symbols(repo, db, project_id, release)

    total = query1(db, 'select count(*) from symbol')
    print(f"Total symbols in release {release}: {total}")

    
if __name__ == "__main__":
    main()
