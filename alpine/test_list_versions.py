import list_versions as lv


def test_has_micro():
    assert lv.parse_semver("1.2.3") == (1, 2, 3)


def test_no_micro():
    assert lv.parse_semver("1.2") == (1, 2, 0)


def test_strip_prefix():
    assert lv.parse_semver("v1.2.3") == (1, 2, 3)
