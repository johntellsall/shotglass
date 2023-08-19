# test_scan_lines.py
# NOTE: very superficial; add tests when needed

import pytest
from scan_lines import main

@pytest.mark.skip(reason="FIXME: needs work")
def test_scan_lines():
    dbpath = "../shotglass.db"  # FIXME: remove hardcoding
    repos = "../SOURCE/flask"  # FIXME: remove hardcoding
    main([dbpath, repos])
    # doesn't crash
