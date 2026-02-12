#inheritance basics

class Animal:
    def speak(self):
        print("animal makes a sound")

class Dog(Animal):
    def bark(self):
        print("Dog barks")

dog = Dog()

dog.speak()
dog.bark()
