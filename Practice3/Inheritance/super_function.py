#super function

class person():
    def __init__(self, name):
        self.name = name

class student(person):
    def __init__ (self, name, university):
        super().__init__(name)
        self.university = university

stdnt = student("alex", "kbtu")
print(stdnt.name)
print(stdnt.university)

