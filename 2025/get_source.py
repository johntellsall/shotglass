import re
import subprocess


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

# def extract_source(archive, suffixes=None):
#     suffixes = ['*.py', '*.c'] # FIXME:
#     assert type(suffixes) is list
#     cmd = ['tar', '-xvf', archive, '--wildcards'] + suffixes
#     print(cmd)
#     result = subprocess.run(cmd, check=True, capture_output=True, text=True)
#     return result.stdout

def extract_source(archive):
    cmd = ['tar', '-xvf', archive]
    print(cmd)
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return result.stdout

def parse_archive_path(output):
    pat = re.compile(r'(?P<name>\S+)_(?P<version>.+?)\.orig\.tar\.gz')
    if m := pat.search(output):
        path = m.group().strip("'")
        name = m.group('name').strip("'")
        return dict(path=path, name=name, version=m.group('version'))
    return None
    
if __name__=='__main__':
    result = download_debian_source(['hello'])
    print(result)
    print()
    # result = extract_source('hello_2.10.orig.tar.gz')
    # print(result)