from sqlmodel import select, delete, func, Field, Session, SQLModel, create_engine
from model import SGAlpinePackage
from lib import get_engine


def render1(limit=False):
    engine = get_engine()
    query = select(SGAlpinePackage)
    if limit:
        query = query.where(SGAlpinePackage.pkgname.startswith('d'))
    with Session(engine) as session:
        results = session.exec(query).all()

    package_count = len(results)

    # FIXME: rewrite in SQL
    rows = []
    for package in results:
        rank = sum([package.sg_len_install, package.sg_len_parse_funcs, package.sg_len_subpackages])
        row = dict(package)
        row['_rank'] = rank
        rows.append(row)

    print(f"Total packages: {package_count}")
    print('Top 10 packages:')
    rows.sort(key=lambda row: row['_rank'], reverse=True)
    for row in rows[:10]:
        print(row['_rank'], row['pkgname'])