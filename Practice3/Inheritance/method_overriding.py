#method overriding
class animal():
    def speak(self):
        print("animal made sound")

class cat(animal):
    def speak(self):
        print("meow")

anim = animal()
ct = cat()

anim.speak()

ct.speak()


