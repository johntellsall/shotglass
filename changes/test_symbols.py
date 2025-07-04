import symbols


def test_main():
    symfile = symbols.parse_path("sample_code/sample.py")
    assert symfile.path == "sample_code/sample.py"
    assert symfile.num_lines == 23
    assert len(symfile.symbols) == 8
