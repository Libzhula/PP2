import random
x = random.randrange(1, 19)
i = 1
print("Hello! What is your name?")
name = str(input())
print("Well, " + name + ", I am thinking of a number between 1 and 20.")
while True:
    print("Take a guess.")
    y = int(input())
    if y > x:
        print("\nYour guess is too much.")
        i+=1
    elif y < x:
        print("\nYour guess is too low.")
        i+=1
    else:
        print("\nGood job, " + name + "! You guessed my number in " + str(i) + " guesses!")
        break