# get_source.py -- download Debian package source
# FIXME: tarballs, not Git repos with history

import re
import subprocess
import sys

import click


# FIXME: not always correct: xz suffix?
def parse_archive_path(output):
    split_pat = re.compile(r'(?P<name>\S+)_(?P<version>.+?)\.orig\.tar\.gz')
    if m := split_pat.search(output):
        path = m.group().strip("'")
        name = m.group('name').strip("'")
        return dict(path=path, name=name, version=m.group('version'))
    
    # NOTE: lacks archive path
    split_pat = re.compile(r'(?P<name>\S+)\s+(?P<version>\d+\.\d+).+\(tar\)')
    if m := split_pat.search(output):
        name = m.group('name').strip()
        version = m.group('version').strip()
        return dict(name=name, version=version)
    return None


def download_debian_source(pkgname, directory):
    """
    download Debian package contents: original source, patches, support files
    """
    assert type(pkgname) is str
    cmd = ['apt-get', 'source', '--download-only'] + [pkgname]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=directory)
    info = parse_archive_path(result.stdout)
    if not info:
        print(f'{pkgname} not found')
        print(result.stdout)
        return None
    return info


def extract_source(archive, dest):
    cmd = ['tar', '--extract', '--verbose', '--file', archive, '--directory', dest]
    print(cmd)
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return result.stdout


@click.command()
@click.argument('pkgnames', nargs=-1)
@click.option('-C', '--directory', default='.', help='Directory to extract the source into')
def main(pkgnames, directory):
    for pkgname in pkgnames:
        print(pkgname)
        info = download_debian_source(pkgname, directory)
        # if info:
        #     extract_source(info['path'], directory)
        print(info)


if __name__=='__main__':
    main(sys.argv[1:])