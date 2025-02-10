#!/usr/bin/env python3
# 
# get_source.py -- download Debian package source
# FIXME: tarballs, not Git repos with history

from pathlib import Path
import re
import subprocess
import sys

import click
from stats import parse_archive_path



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
@click.option('--extract', is_flag=True, help='Extract source code')
@click.option('-C', '--directory', default='.', help='Directory to extract the source into')
def main(extract, pkgnames, directory):
    for pkgname in pkgnames:
        print(pkgname)
        info = download_debian_source(pkgname, directory)
        if extract:
            path = Path(directory) / info['path']
            extract_source(str(path), directory)
        print(info)


if __name__=='__main__':
    main(sys.argv[1:])