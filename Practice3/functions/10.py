def make_unique(list):
    return [x for x in list if list.count(x) == 1]
print(make_unique([1, 1, 2, 3]))