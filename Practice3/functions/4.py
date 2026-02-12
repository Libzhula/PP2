def filter_prime1(list): #loop
    for x in list:
        if x > 1:
            for i in range(2, x//2+1):
                if (x % i) != 0:
                    print(x)
                    break
        if x == 2 or x == 3:
            print(x)

def filter_prime2(list, j = 2, i = 0): #recursion
    if i >= len(list):
        return #stoper
    
    if list[i] < 2:
        return filter_prime2(list, j, i+1)
    elif j < list[i]//2+1:
        if list[i] % j == 0:
            return filter_prime2(list, 2, i + 1)
        else:
            return filter_prime2(list, j + 1, i)
    else:
        print(list[i])
        return filter_prime2(list, j, i+1)

list = [-1, 0, 2, 3, 4, 5, 7, 11] # len = 8
filter_prime1(list)
print("\n")
filter_prime2(list)