class flyer:
    def fly(self):
        print("Flying")

class swimmer:
    def swim(self):
        print("Swimming")

class duck(flyer, swimmer):
    pass

donald = duck()
donald.fly()
donald.swim()
