# test_scan_lines.py 
# NOTE: very superficial; add tests when needed

from scan_lines import main

def test_scan_lines():
    dbpath = '../shotglass.db' # FIXME: remove hardcoding
    repos = '../SOURCE/flask' # FIXME: remove hardcoding
    main([dbpath, repos])
    