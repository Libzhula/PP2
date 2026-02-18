n = int(input())
arr = list(map(int, input().split()))

q = int(input())
ops = []

for _ in range(q):
    parts = input().split()
    
    if parts[0] == "add":
        x = int(parts[1])
        ops.append(lambda a, x=x: a + x)
        
    elif parts[0] == "multiply":
        x = int(parts[1])
        ops.append(lambda a, x=x: a * x)
        
    elif parts[0] == "power":
        x = int(parts[1])
        ops.append(lambda a, x=x: a ** x)
        
    elif parts[0] == "abs":
        ops.append(lambda a: abs(a))

for f in ops:
    arr = list(map(f, arr))

print(*arr)
