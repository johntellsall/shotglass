# get_source.py -- download Debian package source
# FIXME: tarballs, not Git repos with history

import re
import subprocess
import sys


def download_debian_source(pkgname):
    assert type(pkgname) is str
    cmd = ['apt-get', 'source', '--download-only'] + [pkgname]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    info = parse_archive_path(result.stdout)
    if not info:
        print(f'{pkgname} not found')
        print(result.stdout)
        return None
    return info


def extract_source(archive):
    cmd = ['tar', '-xvf', archive]
    print(cmd)
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return result.stdout


# FIXME: not always correct
def parse_archive_path(output):
    pat = re.compile(r'(?P<name>\S+)_(?P<version>.+?)\.orig\.tar\.gz')
    if m := pat.search(output):
        path = m.group().strip("'")
        name = m.group('name').strip("'")
        return dict(path=path, name=name, version=m.group('version'))
    return None

import click
@click.command()
@click.argument('pkgnames', nargs=-1)
def main(pkgnames):
    for pkgname in pkgnames:
        info = download_debian_source(pkgname)
        print(info)

if __name__=='__main__':
    main(sys.argv[1:])