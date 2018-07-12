import make_index


def test_compile():
    df = make_index.compile(None, paths=['simple.py'])
    assert len(df) == 1
    assert df.columns.tolist() == ['path', 'name', 'ctags_raw', 'linecount']
