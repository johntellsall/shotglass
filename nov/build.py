"""
USAGE

shotglass.py <command> <project path>
"""

import logging
import re
import subprocess
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

import git


CTAGS_ARGS = "ctags --fields=+zK --excmd=number -o -".split()
# Example: "asbool settings.py 6; kind:function"
CTAGS_PAT = re.compile(
    r"(?P<name> \S+) .*? " + r"(?P<line_num> \d+) ;.+ " + r"kind:(?P<kind> \S+)",
    re.VERBOSE,
)
logging.basicConfig(format="%(asctime)-15s %(message)s", level=logging.INFO)


def show_details(db):
    for row in db.execute("select * from files order by 1"):
        print(row)


def run_ctags(path):
    cmd = CTAGS_ARGS + [path]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.stdout


def parse_ctags(blob):
    tag_iter = CTAGS_PAT.finditer(blob)
    return tag_iter


def list_paths(repo):
    return repo.git.ls_files().split("\n")


# TODO make more general
def is_source_path(path):
    return path.endswith(".py")


# TODO make more general
def is_interesting(path):
    return not re.search(r"(docs|migrations|tests)/", path)


def is_interesting_source(path):
    return is_source_path(path) and is_interesting(path)


def format_summary(tags):
    return {"num_tags": len(tags)}


def parse_entry(entry, project_dir):
    file_info = {"path": entry.path, "num_bytes": entry.size}
    fullpath = project_dir / entry.path
    ctags_text = run_ctags(fullpath)
    tags = list(parse_ctags(ctags_text))
    file_info.update(format_summary(tags))
    return dict(file_info=file_info, tags=tags)


def print_project(project_dir, source_paths):
    p_name = project_dir.name
    num_source = len(source_paths)
    print(f"PROJECT:{p_name} {num_source} source files")


def get_project(repo):
    try:
        tree = repo.heads.master.commit.tree
    except AttributeError as err:
        attrs = [attr for attr in dir(repo.heads) if not attr.startswith("_")]
        sys.exit(f"tags?? {attrs}\n{err}")
    paths = filter(is_source_path, list_paths(repo))
    paths = filter(is_interesting, paths)
    paths = list(paths)
    return tree, paths


def get_usage():
    cmd_list = [name for name in globals() if name.startswith("cmd_")]
    usage = [__doc__, f"Commands: {cmd_list}"]
    return "\n".join(usage)


def setup_db(db):
    db.execute("drop table if exists files")
    db.execute(
        """
    create table files (path text, byte_count int)
    """
    )


def get_db():
    con = sqlite3.connect("main.db")
    cur = con.cursor()
    return con, cur


def select1(db, sql):
    db.execute(sql)
    return db.fetchone()[0]


def format_tstamp(ts):
    return datetime.fromtimestamp(ts).strftime("%c")


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


def cmd_index(project_path):
    project_dir = Path(project_path)
    print(project_dir)

    repo = git.Repo(project_dir)
    tree, source_paths = get_project(repo)
    con, cur = get_db()

    setup_db(cur)

    issues = []
    for path in source_paths:
        try:
            info = parse_entry(tree[path], project_dir)
        except KeyError as err:
            issues.append((path, err))
            continue
        finfo = info["file_info"]
        values = (finfo["path"], finfo["num_bytes"])
        cur.execute("insert into files values (?, ?)", values)

    con.commit()

    show_details(con)
    con.close()
    if issues:
        print(f"NOTE: {len(issues)} issues found")


def cmd_info(project_path):
    _, db = get_db()
    num_files = select1(db, "select count(*) from files")
    print(f"NUM FILES: {num_files}")


# def cmd_render(project_path):
#     WIDTH, HEIGHT = [1000, 500]
#     VERBOSE = False

#     pg.display.init()
#     screen = pg.display.set_mode(size=[WIDTH, HEIGHT])
#     _, db = get_db()

#     total = select1(db, "select sum(byte_count) from files")
#     print(f"TOTAL: {total} bytes")

#     def num_to_xy(num):
#         y = int(num / WIDTH)
#         x = num % WIDTH
#         return x, y

#     num = 0
#     rows = db.execute("select path, byte_count from files order by 1")
#     coords = []
#     for row in rows:
#         xy = num_to_xy(num)
#         coords.append(xy)
#         num += row[1]

#     white = pg.Color("white")
#     colors = iter_color()
#     for i in range(len(coords) - 1):
#         color = next(colors)
#         xy1, xy2 = coords[i], coords[i + 1]
#         width = xy2[0] - xy1[0]
#         height = xy2[1] - xy1[1]
#         if VERBOSE:
#             print(f"{i}\t{xy1}\t{xy2}\tw={width}\th={height}\tc={color}")
#         rect = pg.Rect(xy1[0], xy1[1], width, height)
#         rect.normalize()
#         pg.draw.rect(screen, color, rect)
#         if False:
#             print(f"\t{rect}")
#             rect.width = rect.height = 20
#             pg.draw.rect(screen, white, rect)

#     pg.image.save(screen, "main.png")


def cmd_releases(project_path):
    project_dir = Path(project_path)
    print(project_dir)
    repo = git.Repo(project_dir)

    def is_interesting_release(tag):
        return re.match(r"^[0-9.]+$", tag.name) is not None

    if False:
        tags = filter(is_interesting_release, repo.tags)
    else:
        tags = repo.tags

    # TODO sort semver
    for tagref in list(tags):
        cool = is_interesting_release(tagref)
        if not cool:
            print("-", end=" ")
        summary = tagref.commit.summary
        tag_tree = tagref.commit.tree
        com_date = tagref.commit.committed_date
        com_datestr = format_tstamp(com_date)
        total_files = len(list(tag_tree.traverse()))
        com_count = sum(1 for _ in tag_tree.traverse())
        com_size = sum(c.size for c in tag_tree.traverse())
        file_list = [x.path for x in tag_tree.traverse()]
        source_list = [path for path in file_list if is_interesting_source(path)]
        print(f"{tagref.name} files={len(file_list)} source={len(source_list)}")
        print(f"\t{com_datestr}")
        print(f"\t{com_count} commits, {com_size} size")
        print(f"\t{summary}")
        print(f"\t{total_files} total files")

    print()


def cmd_show(project_path):
    project_dir = Path(project_path)
    print(project_dir)
    repo = git.Repo(project_dir)
    tree, source_paths = get_project(repo)
    print_project(project_dir, source_paths)
    print(f"{'PATH':50}\tBYTES\tTAGS")
    for path in source_paths:
        info = parse_entry(tree[path], project_dir)
        info = info["file_info"]
        print(f"{path:50}\t{info['num_bytes']}\t{info['num_tags']}")
    print("DONE")


def cmd_nov(project_path):
    def is_release(tag):
        return tag.name.startswith("v")

    repo = git.Repo(project_path)
    release_tags = filter(is_release, repo.tags)
    names = [t.name for t in release_tags]
    assert "v4.5.1" in names
    assert len(names) > 10
    print("okay")


def main():
    try:
        cmd = sys.argv[1]
        project = sys.argv[2]
        cmd_func = globals()[f"cmd_{cmd}"]
    except (KeyError, IndexError):
        sys.exit(get_usage())

    cmd_func(project)


if __name__ == "__main__":
    main()
