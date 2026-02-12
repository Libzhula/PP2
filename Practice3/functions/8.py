def create_stirng(nums):
    return "".join([str(x) for x in nums if x == 0 or x == 7])

def spy_game(some_array):
    a = create_stirng(some_array)
    return "True" if "007" in a else "False"

print(spy_game([1,2,4,0,0,7,5]))
print(spy_game([1,0,2,4,0,5,7]))
print(spy_game([1,7,2,0,4,5,0]))