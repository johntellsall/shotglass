import make_index


def test_compile():
    pd = make_index.compile(None, paths=['simple.py'])
    assert len(pd) == 1
