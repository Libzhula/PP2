def solve1(numheads, numlegs):
    for num_rabs in range(numheads):
        num_chicks = numheads - num_rabs
        if (2*num_chicks + 4*num_rabs) == numlegs:
            return num_rabs, num_chicks


def solve2(numheads, numlegs, num_rabs=0):
    num_chicks = numheads - num_rabs
    if (2 * num_chicks + 4 * num_rabs) == numlegs:
        return num_rabs, num_chicks
    elif num_rabs < numheads:
        return solve2(numheads, numlegs, num_rabs + 1)
    else:
        return None

print(*solve1(35, 94))
print("\n")
print(*solve2(35, 94))