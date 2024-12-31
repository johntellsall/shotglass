from parse import parse

LINES = list(open('APKBUILD').readlines())[:10]


def test_parse():
    info = parse(LINES)
    assert 0, info