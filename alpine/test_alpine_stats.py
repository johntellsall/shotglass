import pathlib

import pytest

import alpine_stats


def test_parse():
    out = alpine_stats.parse_apkbuild(pathlib.Path("test-data/axel.apkbuild"))
    out.pop("options")
    out.pop("sha512sums")
    assert out == {
        "arch": "all",
        "makedepends": "openssl-dev>3",
        "pkgdesc": "A multiple-connection concurrent downloader",
        "pkgname": "axel",
        "pkgrel": "1",
        "pkgver": "2.17.11",
        "source": "$url/releases/download/v$pkgver/axel-$pkgver.tar.xz",
        "subpackages": "$pkgname-doc",
        "url": "https://github.com/axel-download-accelerator/axel",
    }


@pytest.mark.xfail
def test_parse2():
    "these keys aren't parsed yet: options, sha512sums"
    out = alpine_stats.parse_apkbuild(pathlib.Path("test-data/axel.apkbuild"))
    assert out.pop("options") == '"!check"', "should strip comments"
    assert len(out.pop("sha512sums")) > 50
