# Normal func
def add(a, b):
    return a + b

# lambda equivalent
add_lambda = lambda a, b: a + b

print("Normal function:", add(2, 3))
print("Lambda function:", add_lambda(2, 3))


# lambda with one argument
square = lambda x: x * x
print("Square:", square(4))