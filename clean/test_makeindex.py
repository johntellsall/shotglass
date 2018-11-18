from pathlib import Path

import makeindex

SOURCE_DIR = Path("/Users/johnmitchell/src/SOURCE")


def test_ls_files_py():
    out = makeindex.list_source_files(Path(".."))
    assert type(out) is list and len(out) > 0


def test_ls_files_c():
    out = makeindex.list_source_files(SOURCE_DIR / "redis")
    assert type(out) is list and len(out) > 0


def test_make_index():
    makeindex.make_index(["makeindex.py"])
