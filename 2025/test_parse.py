from parse import parse

LINES = list(open('APKBUILD').readlines())


def test_simple():
    info = parse(LINES)
    assert info['pkgname'] == 'dnsmasq'
    assert info['pkgver'] == '2.90'

def test_string():
    info = parse(LINES)
    assert info['pkgdesc'] == "A lightweight DNS, DHCP, RA, TFTP and PXE server"

def test_multiline():
    info = parse(LINES)
    value = info['makedepends']
    assert value[:2] == ['coreutils', 'dbus-dev']
    assert value[-2:] == ['nettle-dev', 'nftables-dev']