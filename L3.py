class coordinate(object):
    def __init__ (self, xval, yval):
        self.x = xval
        self.y = yval
    def distance (self, other):
        x_diff_sq = (self.x - other.x) ** 2
        y_diff_sq = (self.y - other.y) ** 2
        return (x_diff_sq + y_diff_sq) ** 0.5

home = coordinate(0,0)
job = coordinate(2147483647, 2147483647)
uni = coordinate(10, 31)

print(home.distance(uni))
print(uni.distance(job))

