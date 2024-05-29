
# TODO: define xy as list of two numbers? Position?
class Cursor:
    def __init__(self, width):
        self.xy = [0, 0]
        self.width = int(width)

    def skip(self, num):
        """emit slices of consumed area
         """
        slices = []
        while num + self.xy[0] >= self.width:
            # consume full row
            old = tuple(self.xy)
            num -= self.width - self.xy[0]
            slice = [tuple(self.xy), (self.width, self.xy[1])]
            slices.append(slice)
            # move down one row
            self.xy = [0, self.xy[1] + 1]

        if num > 0 and num + self.xy[0] <= self.width:
            old = tuple(self.xy)
            self.xy[0] += num
            slices.append([old, tuple(self.xy)])

        return slices
       
