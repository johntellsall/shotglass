from sqlmodel import select, delete, func, Field, Session, SQLModel, create_engine
from model import SGAlpinePackage
import parse
from lib import get_engine


def equery(engine, query):
    with Session(engine) as session:
        return session.exec(query).all()


def raw_query(engine, release, limit=False):
    query = select(SGAlpinePackage)
    if release:
        query = query.where(SGAlpinePackage.alpine_release == release)
    if limit:
        query = query.where(SGAlpinePackage.pkgname.startswith('d'))
    with Session(engine) as session:
        return session.exec(query).all()


def annotate_package_rank(packages):
    """
    convert to dict; add per-package metadata
    """
    for package in packages:
        rank = sum([package.sg_len_install, package.sg_len_parse_funcs, package.sg_len_subpackages])
        item = dict(package)
        item['_rank'] = rank
        yield item


def query(release, limit=False):
    engine = get_engine()
    packages = raw_query(engine, release=release, limit=limit)

    result = {}
    # result['package_count'] = len(packages)
    result['rows'] = list(annotate_package_rank(packages))
    return result
    # format1(result)


def print_stats(result):
    # print(f"Total packages: {result['package_count']}")
    print('Top 10 packages:')
    ranked_rows = sorted(result['rows'], key=lambda row: row['_rank'], reverse=True)
    for row in ranked_rows[:10]:
        print(row['_rank'], row['pkgname'])


def format_html_table():
    def format_row(row):
        middle = ''.join(f"<td>{value}</td>" for value in row)
        return f"<tr>{middle}</tr>"

    # engine = get_engine()
    releases = ['3.10-stable', '3.14-stable', '3.15-stable']
    data = {}
    for release in releases:
        raw_rows = query(release)['rows']
        rows = sorted(raw_rows, key=lambda row: row['_rank'], reverse=True)
        data[release] = rows[:10]

    html = []
    html.append('<table>')
    html.append('<tr>' + ''.join(f'<th>{release}</th>' for release in releases) + '</tr>')
    for i in range(10):
        def format_rel_package(pkg):
            return f"{pkg['pkgname']} ({pkg['_rank']})"
        row = [format_rel_package(data[rel][i]) for rel in releases]
        html.append(format_row(row))
    html.append('</table>')
    return '\n'.join(html)


def report_popcon():
    popcon = parse.parse_debian_popcon(open('dist/by_vote').read()):

