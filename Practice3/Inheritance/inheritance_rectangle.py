from classes.shape_and_square import Shape
class Rectangle(Shape):
    def __init__(self, length: int, width: int):
        if not isinstance(length, int) or not isinstance(width, int):
            raise TypeError("length and width must be int")
        self.length = length
        self.width = width
    def area(self):
        return self.length * self.width
if __name__ == "__main__":
    z = Rectangle(3, 4)
    print(z.area())