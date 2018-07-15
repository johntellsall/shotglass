import make_ctags


def test_compile():
    df = make_ctags.compile(None, paths=['simple.py'])
    assert len(df) == 1
    assert df.columns.tolist() == ['path', 'name', 'ctags_raw', 'linecount']
