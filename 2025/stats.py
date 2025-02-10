import re


DULL_DIRS = ('contrib/', 'debian/', 'deps/', 'doc/', 'examples/', 'test/', 'tests/')


# FIXME: not always correct: xz suffix?
def parse_archive_path(output):
    split_pat = re.compile(r'(?P<name>\S+)_(?P<version>.+?)\.tar\.\S+')
    if m := split_pat.search(output):
        path = m.group().strip("'")
        name = m.group('name').strip("'")
        version = m.group('version')
        if version.endswith('.orig'):
            version = version[:-5]
        return dict(path=path, name=name, version=version)
    
    # NOTE: lacks archive path
    split_pat = re.compile(r'(?P<name>\S+)\s+(?P<version>\d+\.\d+).+\(tar\)')
    if m := split_pat.search(output):
        name = m.group('name').strip()
        version = m.group('version').strip()
        return dict(name=name, version=version)
    return None


def simplify(path):
    path = path.replace('src/', '')
    path = path.replace('.c', '')  # FIXME:
    return path

