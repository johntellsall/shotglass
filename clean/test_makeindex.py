import makeindex


def test_ls_files():
    out = makeindex.Repos("..").ls_files()
    print(out)
    assert type(out) is list and len(out) > 0
