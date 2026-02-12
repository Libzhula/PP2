#lambda with filters

nums = [i for i in range(1,10)]

print ("Original", nums)

even = list(filter(lambda x: x % 2 == 0, nums))

print ("Evens", even)