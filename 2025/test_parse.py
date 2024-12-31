LINES = open('APKBUILD').readlines()

def test_parse():
    lines = LINES.copy()
    assert 0, lines[0]