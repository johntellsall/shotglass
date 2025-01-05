from collections import defaultdict
from email.policy import default
from pprint import pprint
from sqlmodel import select, Session
from model import SGAlpinePackage
import parse
from lib import get_engine
from sqlalchemy import text


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


def format_html_row(row):
    middle = ''.join(f"<td>{value}</td>" for value in row)
    return f"<tr>{middle}</tr>"


def format_html_table():
    # engine = get_engine() NOTE:
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
        html.append(format_html_row(row))
    html.append('</table>')
    return '\n'.join(html)


# FIXME: use database version of popcon
def report_popcon():
    debian_popcon = parse.parse_debian_popcon(open('dist/by_vote').read())
    print(f'Debian packages: {len(debian_popcon)}')

    engine = get_engine()
    query = select(SGAlpinePackage.pkgname).distinct()
    with Session(engine) as session:
        alpine_packages = session.exec(query).all()

    query = select(SGAlpinePackage.pkgname, SGAlpinePackage.pkgdesc)
    with Session(engine) as session:
        result = session.exec(query).all()
    alpine_pkgdesc = {pkgname: pkgdesc for pkgname, pkgdesc in result}

    print(f'Alpine packages (main only): {len(alpine_packages)}')

    raw_alpine_popcon = {pkgname: debian_popcon.get(pkgname) for pkgname in alpine_packages}
    alpine_popcon = {pkgname: vote for pkgname, vote in raw_alpine_popcon.items() if vote}
    print(f'Common packages: {len(alpine_popcon)}')

    print('Top 20 Alpine packages by Debian popularity:')
    for pkgname, vote in sorted(alpine_popcon.items(), key=lambda item: item[1], reverse=True)[:20]:
        desc = alpine_pkgdesc.get(pkgname, 'N/A')
        print(f'- {pkgname:22} {vote:6} {desc}')


def query_popular(engine):
    with open('popular-packages.sql', 'r') as file:
        popular_sql = file.read()
    # strip header
    select_index = popular_sql.index("SELECT ")
    popular_sql = popular_sql[select_index:]

    with Session(engine) as session:
        popular_ranked = session.exec(text(popular_sql)).all()
    popular_names = set(name for name,_ in popular_ranked)
    return popular_names


def query_sqlfile(engine, path):
    with open(path) as f:
        sql = f.read()

    with Session(engine) as session:
        return session.exec(text(sql)).all()


def query_popcon2(engine, releases):
    data = query_sqlfile(engine, 'pop_over_time.sql')

    # the row is determined by the latest release
    # column is release
    package_row_num = {}
    grid = []
    debug = False
    for drelease, dpkgname, _ in data:
        item = {'release': drelease, 'pkgname': dpkgname}
        if debug: print(f'{drelease} {dpkgname}')
        row_num = package_row_num.get(dpkgname)
        if row_num is None:
            package_row_num[dpkgname] = len(grid)
            grid.append({drelease: item})
            if debug: print(f'new row {grid[-1]}')
        else:
            if debug: print(f'- item {item} -> row {row_num}')  
            grid[row_num][drelease] = item
    return grid


def report_popcon2():
    """
    track popular packages across multiple Alpine releases
    """
    engine = get_engine()
    # FIXME: must match with pop_over_time.sql
    releases = ['3.0-stable', '3.10-stable', '3.21-stable']
    grid = query_popcon2(engine, releases)
    
    last_release = releases[-1]
    for num,row in enumerate(grid):
        item = list(row.values())[0]
        if len(row) == len(releases):
            print(f'--- {item["pkgname"]}')
        else:
            if last_release in row:
                print(f'NEW: {item["pkgname"]} -- {row}')
            else: 
                print(f'REMOVED: {item["pkgname"]} -- {row}')


def report_popcon3():
    """
    track popular packages across multiple Alpine releases
    - output HTML table
    - grid shows versions
    """
    engine = get_engine()
    # FIXME: must match with pop_over_time.sql
    releases = ['3.0-stable', '3.10-stable', '3.21-stable']
    grid = query_popcon2(engine, releases)
    
    table = []
    last_release = releases[-1]
    for row in grid:
        item = list(row.values())[0]
        cells = [item["pkgname"]]
        if len(row) == len(releases):
            cells += ['-'] * len(releases)
            table.append(format_html_row(cells))
        else:
            if last_release in row:
                print(f'NEW: {item["pkgname"]} -- {row}')
            else: 
                print(f'REMOVED: {item["pkgname"]} -- {row}')

    for row in table:
        print(row)
