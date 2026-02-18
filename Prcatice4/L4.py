class Animal(object):
    def __init__(self, age, name=None):
        self.years = age
        self.name = name
    def __str__(self):
        return "animal:"+str(self.name)+":"+str(self.years)
    def get_age(self):
        return self.years
    def set_age(self, newage):
        self.years = newage
    
def make_animals(l1, l2):
    animals = []
    for i in range(0, len(l1)):
        i1 = l1[i]
        i2 = l2[i]
        animals.append(Animal(i1, i2))
    return animals

l1 = [3, 5, 7]
l2 = ['grifith', 'buffalo', 'cow']

animals = make_animals(l1, l2)

print (animals)

for i in animals:
    print (i)
