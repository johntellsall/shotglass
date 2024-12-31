from parse import parse

LINES = list(open('APKBUILD').readlines())


def test_simple():
    info = parse(LINES)
    assert info['pkgname'] == 'dnsmasq'
    assert info['pkgver'] == '2.90'

def test_string():
    info = parse(LINES)
    assert info['pkgdesc'] == "A lightweight DNS, DHCP, RA, TFTP and PXE server"