import math
def find_volume_of_sphere(radius):
    return 4/3 * math.pi * math.pow(radius, 3)
print(find_volume_of_sphere(int(input())))