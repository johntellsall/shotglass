from pathlib import Path

from . import make_index

DIR = '/Users/johnmitchell/jsrc/shotglass/shotglass/app/management/commands'

FIRST_FUNC = {
    '_type': 'tag', 'name': 'clone', 'path': 'xx',
    'access': 'public', 'language': 'Python', 'line': 28,
    'signature': '(url)', 'kind': 'function', 'roles': 'def', 'end': 34}


def test_get_ctags_info():
    path = Path(DIR) / 'sample.py'
    assert path.exists()
    full = make_index.get_ctags_info(path)
    tags = [item for item in full if item['_type'] != 'ptag']
    funcs = [item for item in tags if item['kind'] == 'function']
    funcs[0]['path'] = 'xx'
    assert funcs[0] == FIRST_FUNC
    assert 3 == len(funcs)
