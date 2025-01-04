import os
from pathlib import Path
from pprint import pprint
import re
import subprocess
import sys
from sqlmodel import select, delete, func, Field, Session, SQLModel, create_engine
from model import SGAlpinePackage
from parse import parse
from lib import get_engine
from sqlalchemy.exc import OperationalError


def db_delete_all(engine):
    """
    WARNING: Remove all existing SGAlpinePackage entries
    """
    try:
        with Session(engine) as session:
            statement = delete(SGAlpinePackage)
            session.exec(statement)
            session.commit()
    except OperationalError as e:
        print(f"OperationalError: {e}") # FIXME:


def extract_apk_dir(topdir, release, session):
    path = Path(topdir) / 'APKBUILD'
    if not path.exists():
        print(f"{path}: path not found", file=sys.stderr)
        return
    info = parse(open(path), label=path)
    info = SGAlpinePackage.annotate(info)
    package = SGAlpinePackage(alpine_release=release, **info)
    session.add(package)


def extract(paths, release, verbose=True):
    engine = get_engine()

    if 0:
        db_delete_all(engine) # FIXME:

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        for num,topdir in enumerate(paths):
            dirname = Path(topdir).name
            if (verbose and num % 10 == 1):
                print(dirname, end=' ')
            extract_apk_dir(topdir, release, session)
            # commit the first item to find errors more quickly
            if num == 0:
                session.commit()

        session.commit()
        if verbose:
            print()

    # with Session(engine) as session:
    #     count = session.scalar(select(func.count()).select_from(SGAlpinePackage))
    #     print(f"Release: {release} -- Total packages: {count}")


def git_checkout(branch):
    checkout_cmd = ["git", "-C", "aports", "checkout", "--quiet", f"remotes/origin/{branch}"]
    result = subprocess.run(checkout_cmd, capture_output=True, text=True)
    if result.returncode != 0: # FIXME: more here
        print(f"Failed to checkout branch {branch}: {result.stderr}", file=sys.stderr)


# TODO: ignore stderr
def git_list_branches():
    cmd = ["git", "-C", "aports", "branch", "-a"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    releases = re.compile(r'remotes/origin/(\d+\.\d+-stable)').findall(result.stdout)
    # FIXME:
    if 1:
        releases = [rel for rel in releases if rel.startswith('3.')]
        return releases[-3:]
    return releases


def extract2():
    engine = get_engine()
    releases = git_list_branches()
    print(f'Found {len(releases)} releases')
    for release in releases:
        print(f'{release}:')
        git_checkout(release)
        topdirs = [str(f) for f in Path('aports/main').iterdir() if f.is_dir()]
        print(f'- {len(topdirs)} main directories')
        extract(topdirs, release, verbose=False)
        with Session(engine) as session:
            count = session.scalar(select(func.count()).select_from(SGAlpinePackage))
        print(f'- {count} total packages')
