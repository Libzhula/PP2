def filter_prime1(x):
    if x <= 1:
        return False
    for i in range(2, x//2+1):
        if (x % i) == 0:
            return False
    return True

x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
print(list(filter(lambda i: filter_prime1(i), x)))
