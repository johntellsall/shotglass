from pathlib import Path

import makeindex

SOURCE_DIR = Path("/Users/johnmitchell/src/SOURCE")


def test_ls_files_py():
    out = makeindex.main(Path(".."))
    print(out)
    assert type(out) is list and len(out) > 0


def test_ls_files_c():
    out = makeindex.main(SOURCE_DIR / "redis")
    print(out)
    assert type(out) is list and len(out) > 0
