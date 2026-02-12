class Shape:
    def __init__(self):
        self.length = 0
        self.width = 0
    def area(self):
        return 0
class Square(Shape):
    def __init__(self, length):
        if not isinstance(length, int):
            raise TypeError("length must be int")
        super().__init__()
        self.length = length
    def area(self):
        return self.length * self.length

if __name__ == "__main__":
    x = Shape()
    y = Square(5)
    print(x.area())
    print(y.area())