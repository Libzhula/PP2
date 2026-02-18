def fibo(n):
    a, b = 0, 1
    for i in range(0, n):
        yield a
        a, b = b, a+b

n = int(input())
first = 1
for i in fibo(n):
    if not first:
        print(",", end="")
    print(i, end = "")
    first = 0
