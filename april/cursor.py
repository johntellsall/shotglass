
# TODO: define xy as list of two numbers? Position?
class Cursor:
    def __init__(self, width):
        self.xy = [0, 0]
        self.width = int(width)

    def skip(self, num):
        """emit slices of consumed area
        Note: slice endpoints are *exclusive*
        Ex: 3-wide row, consume 2:
        - start at 0,0
        - move to 2,0 -- two spots consumed
        -> slice is ([0,0], [2,0]) -- end is exclusive
        -> draw [0,0] and [1,0] (two spots) don't draw [2,0]
        FIXME: slices are lists of tuples, for PIL.ImageDraw
        """
        slices = []
        if num + self.xy[0] <= self.width:
            old = tuple(self.xy)
            self.xy[0] += num
            slices.append([old, tuple(self.xy)])
        # else:
        #     # consume full row
        #     end = self.xy[0] + self.width
        #     slices.append((self.xy, [end, self.xy[1]] )
        #     self.xy = [0, self.xy[1] + 1]
        #     # consume rest of row
        #     end = self.xy[0] + num - self.width
        #     slices.append((self.xy, [end, self.xy[1]] )
        #     self.xy = [end, self.xy[1]]
        return slices
       
