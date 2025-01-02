from sqlmodel import select, delete, func, Field, Session, SQLModel, create_engine
from model import SGAlpinePackage
from lib import get_engine


def format1(result):
    print(f"Total packages: {result['package_count']}")
    print('Top 10 packages:')
    ranked_rows = sorted(result['rows'], key=lambda row: row['_rank'], reverse=True)
    for row in ranked_rows[:10]:
        print(row['_rank'], row['pkgname'])


def render1(limit=False):
    engine = get_engine()
    query = select(SGAlpinePackage)
    if limit:
        query = query.where(SGAlpinePackage.pkgname.startswith('d'))
    with Session(engine) as session:
        packages = session.exec(query).all()

    result = {}
    result['package_count'] = len(packages)

    # FIXME: rewrite in SQL
    rows = []
    for package in packages:
        rank = sum([package.sg_len_install, package.sg_len_parse_funcs, package.sg_len_subpackages])
        row = dict(package)
        row['_rank'] = rank
        rows.append(row)

    result['rows'] = rows

    format1(result)