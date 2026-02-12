class bankAccount:
    def __init__(self, owner, balance:int):
        if not isinstance(balance, int):
            raise TypeError("balance must be int")
        self.owner = owner
        self.balance = balance
    def deposit(self, amount:int):
        if not isinstance(amount, int):
            raise TypeError("balance must be int")
        self.balance += amount
    def withdraw(self, amount:int):
        if not isinstance(amount, int):
            raise TypeError("balance must be int")
        if amount > self.balance:
            raise ValueError("not enough money in your account")
        self.balance -= amount

if __name__ == "__main__":
    first = bankAccount("Mihail", 0)
    print(f"{first.owner} has a {first.balance} money in balance")
    first.deposit(1000)
    print("1000 added")
    print(f"{first.owner} has a {first.balance} money in balance after opeartion")
    first.withdraw(500)
    print("500 withdrawn")
    print(f"{first.owner} has a {first.balance} money in balance after opeartion")
    first.withdraw(600)