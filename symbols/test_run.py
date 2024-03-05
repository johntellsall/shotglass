import run

# TODO: can "roles" track function calls?
# Not in Python?

CTAGS_KEYS = {
    "_type",
    "name",
    "path",
    "access",
    "inherits",
    "language",
    "line",
    "kind",
    "roles",  # how a tag is referenced; "def" = defined
    "end",
}


def test_run_ctags():
    res = list(run.run_ctags(path="sample_code/sample.py"))
    assert set(res[0]) == CTAGS_KEYS


# {'_type': 'tag',
#  'access': 'public',
#  'end': 7,
#  'inherits': False,
#  'kind': 'class',
#  'language': 'Python',
#  'line': 5,
#  'name': 'Whiskey',
#  'path': 'sample_code/sample.py',
#  'roles': 'def'}
# ...
# {'_type': 'tag',
#   'access': 'private',
#   'end': 11,
#   'file': True,
#   'kind': 'function',
#   'language': 'Python',
#   'line': 10,
#   'name': 'inner',
#   'path': 'sample_code/sample.py',
#   'roles': 'def',
#   'scope': 'outer1',
#   'scopeKind': 'function',
#   'signature': '()'},
def test_run_ctags_detail():
    res = list(run.run_ctags(path="sample_code/sample.py"))
    res = res[0]
    assert res == {
        "_type": "tag",
        "access": "public",
        "end": 7,
        "inherits": False,
        "kind": "class",
        "language": "Python",
        "line": 5,
        "name": "Whiskey",
        "path": "sample_code/sample.py",
        "roles": "def",
    }
