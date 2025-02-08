from pathlib import Path
import re
import subprocess
import sys
from sqlmodel import select, delete, func, Session, SQLModel
from model import DebianPopContest, SGAlpinePackage
import parse
from lib import get_engine
from sqlalchemy.exc import OperationalError
from lib import git_checkout, git_list_branches


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
    """
    for a single package, parse it and create SGAlpinePackage entry
    """
    path = Path(topdir) / 'APKBUILD'
    if not path.exists():
        raise ValueError(f"{path}: path not found")
    info = parse.parse(path.open(), label=path)
    info = SGAlpinePackage.annotate(info)
    package = SGAlpinePackage(alpine_release=release, **info)
    session.add(package)
    return info


def extract(paths, release, verbose=False):
    """
    extract list of packages into database
    - single version of Alpine in "release"
    """
    engine = get_engine()

    if 0:
        db_delete_all(engine) # FIXME:

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        for num,topdir in enumerate(paths):
            if num > 10:
                break
            dirname = Path(topdir).name
            if (verbose and num % 10 == 1):
                print(dirname, end=' ')
            try:
                info = extract_apk_dir(topdir, release, session)
                if verbose:
                    print(info)
            except ValueError as e:
                print(f"{dirname}: {e}")
                continue
            # commit the first item to find errors more quickly
            if num == 0:
                session.commit()

        session.commit()
        if verbose:
            print()

    # with Session(engine) as session:
    #     count = session.scalar(select(func.count()).select_from(SGAlpinePackage))
    #     print(f"Release: {release} -- Total packages: {count}")

def extract2(paths):
    """
    import all Alpine packages from all branches/releases
    
    Paths given: testing mode
    - import one release only
    - import packages listed in paths
    """
    engine = get_engine()
    releases = git_list_branches()
    verbose = False

    if not paths:
        print(f'Found {len(releases)} releases')
        for release in releases:
            print(f'{release}:')
            git_checkout(release)
            topdirs = [str(f) for f in Path('aports/main').iterdir() if f.is_dir()]
            print(f'- {len(topdirs)} main directories')
            extract(topdirs, release)
    else:
        # paths given: testing mode, parse those repos only
        # NOTE: release is random, not latest
        for release in [releases[-1]]:
            print(f'{release}:')
            git_checkout(release)
            topdirs = paths
            print(f'- {len(topdirs)} main directories')
            extract(topdirs, release)

    with Session(engine) as session:
        count = session.scalar(select(func.count()).select_from(SGAlpinePackage))
    print(f'- {count} total packages')



def extract_popcon():
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
    popcon = parse.parse_debian_popcon()
    with Session(engine) as session:
        for num,package in enumerate(popcon.values()):
            deb_pkg = DebianPopContest(**package)
            session.add(deb_pkg)
            if num == 0: # make bugs show early
                session.commit()
        session.commit()

    with Session(engine) as session:
        count = session.scalar(select(func.count()).select_from(DebianPopContest))
    print(f"DebianPopContest packages: {count}")