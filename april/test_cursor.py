from cursor import Cursor

#  Note: slice endpoints are *exclusive*
# Example: 3-wide row, consume 2:
# - start at 0,0
# - move to 2,0 -- two spots consumed
# -> slice is ([0,0], [2,0]) -- end is exclusive
# -> draw [0,0] and [1,0] (two spots) don't draw [2,0]
# - next spot is [2,0]
      
def test_same_row():
    "move in same row"
    cursor = Cursor(3)
    assert cursor.xy == [0, 0]
    slices = cursor.skip(2)
    assert cursor.xy == [2, 0]
    assert slices == [[(0, 0), (2, 0)]]

def test_next_row():
    "jump to next row"
    cursor = Cursor(3)
    slices = cursor.skip(3)
    assert cursor.xy == [0, 1]
    assert slices == [[(0, 0), (3, 0)]]

def test_next_row_and_col():
    "move in X and Y"
    cursor = Cursor(3)
    slices = cursor.skip(5)
    # first row: all 3 spots consumed
    assert slices.pop(0) == [(0, 0), (3, 0)]
    # second row: 2 spots consumed
    assert slices.pop(0) == [(0, 1), (2, 1)]
    assert not slices
    assert cursor.xy == [2, 1]
