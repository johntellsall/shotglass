# main2.py -- import file info only
from collections import defaultdict
from pathlib import Path
import state

CONFIG = {
    "SourceTypes": {".py"} #  FIXME:
}


def db_add_files(con, project_id, file_data):
    insert_file = (
        "insert into file (project_id, path, num_lines, size_bytes)"
        f" values ({project_id}, :path, :num_lines, :size_bytes)"
    )
    res = con.executemany(insert_file, file_data)
    con.commit()
    return res.rowcount


def show_stats(db):
    num_files = state.query1(db, table="file")
    print(f"Number of files in the database: {num_files}")


# NOTE: compare with "git ls-files"
# NOTE: no release info
def scan_project_files(project_root):
    proj = Path(project_root)

    # get all files in tree, indexed by suffix
    by_suffix = defaultdict(set)
    files = (file for file in proj.rglob("*") if file.is_file())
    for file in files:
        by_suffix[file.suffix].add(file)

    # find paths with interesting suffixes
    proj_files = set()
    for suffix in CONFIG["SourceTypes"]:
        proj_files.update(by_suffix[suffix])

    # return list of interesting paths relative to project root
    return [file.relative_to(proj) for file in proj_files]


def calc_fileinfo(project_root, relpath):
    file_path = Path(project_root) / relpath
    size_bytes = file_path.stat().st_size
    num_lines = sum(1 for _ in file_path.open())
    return {
        "path": str(relpath),
        "size_bytes": size_bytes,
        "num_lines": num_lines,
    }


def main(project_dirs):
    db = state.get_db(temporary=True)
    db.execute('insert into project (id, name) values (1, "temp")')
    for project_dir in project_dirs:
        proj_files = scan_project_files(project_dir)
        proj_data = [calc_fileinfo(project_dir, relpath) for relpath in proj_files]
        db_add_files(db, 1, proj_data)

    show_stats(db)

if __name__ == "__main__":
    import sys
    project_dirs = sys.argv[1:]
    main(project_dirs)
