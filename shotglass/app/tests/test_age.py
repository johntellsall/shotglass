import itertools

from app.management.commands import age

def test_serpentine_iter():
    height, width = 4, 3
    rows = itertools.islice(age.serpentine_iter(width), width*height)
    assert list(rows) == [
        (0, 0), (1, 0), (2, 0), 
        (2, 1), (1, 1), (0, 1),
        (0, 2), (1, 2), (2, 2),
        (2, 3), (1, 3), (0, 3)]