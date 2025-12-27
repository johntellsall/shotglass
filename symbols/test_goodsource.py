from goodsource import GoodTagFilter


def test_filter_latest():
    gtf = GoodTagFilter("../SOURCE/flask")
    gtf.set_good_pat("latest")
    tags = gtf.get_tags()
    assert tags == ['upstream/3.1.2']


def test_filter_debian():
    gtf = GoodTagFilter("../SOURCE/flask")
    gtf.set_good_pat("debian")
    tags = gtf.get_tags()
    assert 'debian/3.1.2-1' in tags