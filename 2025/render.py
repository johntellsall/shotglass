from sqlmodel import select, delete, func, Field, Session, SQLModel, create_engine
from model import SGAlpinePackage
from lib import get_engine


def format1(result):
    print(f"Total packages: {result['package_count']}")
    print('Top 10 packages:')
    ranked_rows = sorted(result['rows'], key=lambda row: row['_rank'], reverse=True)
    for row in ranked_rows[:10]:
        print(row['_rank'], row['pkgname'])


def query(engine, limit=False):
    query = select(SGAlpinePackage)
    if limit:
        query = query.where(SGAlpinePackage.pkgname.startswith('d'))
    with Session(engine) as session:
        return session.exec(query).all()


def annotate_rank_result(packages):
    for package in packages:
        rank = sum([package.sg_len_install, package.sg_len_parse_funcs, package.sg_len_subpackages])
        item = dict(package)
        item['_rank'] = rank
        yield item


def render1(limit=False):
    engine = get_engine()
    packages = query(engine, limit=limit)

    result = {}
    result['package_count'] = len(packages)
    result['rows'] = list(annotate_rank_result(packages))

    format1(result)