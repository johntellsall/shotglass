from parse import parse

LINES = list(open('APKBUILD').readlines())[:10]


def test_simple():
    info = parse(LINES)
    assert info['pkgname'] == 'dnsmasq'