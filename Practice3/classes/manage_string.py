class manageString:
    def __init__(self):
        self.string = ""
    def getString(self): # get string
        self.string = input()
    def printString(self): # string to upper
        print(self.string.upper())

x = manageString()
x.getString()
x.printString()