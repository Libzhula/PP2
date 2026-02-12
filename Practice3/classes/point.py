from math import sqrt
class Point:
    def __init__(self):
        self.x = 0
        self.y = 0
    def show(self):
        return self.x, self.y
    def move(self, x:int, y:int):
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("coords must be int")
        self.x = x
        self.y = y
    def dist_to(self, other):
        return sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

if __name__ == "__main__":
    A = Point()
    B = Point()
    A.move(1, 1)
    B.move(3, 1)
    print(A.dist_to(B))