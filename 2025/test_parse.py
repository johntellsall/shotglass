import pprint
import parse
import pytest

LINES = list(open('APKBUILD').readlines())


def test_simple():
    info = parse.parse(LINES)
    assert info['pkgname'] == 'dnsmasq'
    assert info['pkgver'] == '2.90'

def test_string():
    info = parse.parse(LINES)
    assert info['pkgdesc'] == "A lightweight DNS, DHCP, RA, TFTP and PXE server"

def test_multiline():
    info = parse.parse(LINES)
    value = info['makedepends']
    assert value[:2] == ['coreutils', 'dbus-dev']
    assert value[-2:] == ['nettle-dev', 'nftables-dev']

def test_function():
    info = parse.parse(LINES)
    assert(info['_parse_functions'] == ['build', 'check', 'package', 'dnssec', 'nftset', 'dbus', 'common', 'openrc', 'utils', 'utils_doc'])

# def test_alt():
#     lines = open('aports/main/dnstop/APKBUILD')
#     info = parse(lines)
#     assert 0, pprint.pformat(info)

@pytest.mark.xfail
def test_list_quote():
    lines = open('test-data/list-quote.dat')
    info = parse(lines)
    assert 0, pprint.pformat(info)


raw_popcon_data = '''#<no-files> is the number of people whose entry didn't contain enough
#           information (atime and ctime were 0).
#rank name                            inst  vote   old recent no-files (maintainer)
1     libacl1                        138898 126117     2 12764    15 (Guillem Jover)                 
2     libpcre2-8-0                   138890 126112     3 12762    13 (Matthew Vernon)'''

def test_parse_popcon_raw():
    packages = parse.parse_debian_popcon_raw(raw_popcon_data)
    assert packages[0] == {'rank': 1, 'name': 'libacl1', 'inst': 138898, 'vote': 126117, 'old': 2, 'recent': 12764, 'no_files': 15, 'maintainer': 'Guillem Jover'}
    assert len(packages) == 2


def test_parse_popcon():
    raw = "1     libacl1                        138898 126117     2 12764    15 (Guillem Jover)   "              
    value = {'libacl1': {'rank': 1, 'name': 'libacl1', 'inst': 138898, 'vote': 126117, 'old': 2, 'recent': 12764, 'no_files': 15, 'maintainer': 'Guillem Jover'}}
    assert parse.parse_debian_popcon(raw) == value
