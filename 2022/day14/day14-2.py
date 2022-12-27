# --- Part Two ---
# You realize you misread the scan. There isn't an endless void at the bottom of the scan - there's floor, and you're standing on it!

# You don't have time to scan the floor, so assume the floor is an infinite horizontal line with a y coordinate equal to two plus the highest y coordinate of any point in your scan.

# In the example above, the highest y coordinate of any point is 9, and so the floor is at y=11. (This is as if your scan contained one extra rock path like -infinity,11 -> infinity,11.) With the added floor, the example above now looks like this:

#         ...........+........
#         ....................
#         ....................
#         ....................
#         .........#...##.....
#         .........#...#......
#         .......###...#......
#         .............#......
#         .............#......
#         .....#########......
#         ....................
# <-- etc #################### etc -->
# To find somewhere safe to stand, you'll need to simulate falling sand until a unit of sand comes to rest at 500,0, blocking the source entirely and stopping the flow of sand into the cave. In the example above, the situation finally looks like this after 93 units of sand come to rest:

# ............o............
# ...........ooo...........
# ..........ooooo..........
# .........ooooooo.........
# ........oo#ooo##o........
# .......ooo#ooo#ooo.......
# ......oo###ooo#oooo......
# .....oooo.oooo#ooooo.....
# ....oooooooooo#oooooo....
# ...ooo#########ooooooo...
# ..ooooo.......ooooooooo..
# #########################
# Using your scan, simulate the falling sand until the source of the sand becomes blocked. How many units of sand come to rest?


source = (500, 0)


def add(coord1, coord2):
    return tuple(a + b for a, b in zip(coord1, coord2))


with open("input.txt") as f:
    sps = [[k.split(",") for k in p] for p in [sp.split(" -> ") for sp in f]]
paths = [[(int(x), int(y)) for x, y in p] for p in sps]

cave = {}
mins = source
maxs = source
for path in paths:
    for i, coord in enumerate(path[:-1]):
        next_coord = path[i + 1]
        x_range = sorted([coord[0], next_coord[0]])
        y_range = sorted([coord[1], next_coord[1]])

        mins = (min(mins[0], x_range[0]), min(mins[1], y_range[0]))
        maxs = (max(maxs[0], x_range[1]), max(maxs[1], y_range[1]))

        for x in range(x_range[0], x_range[1] + 1):
            for y in range(y_range[0], y_range[1] + 1):
                cave[(x, y)] = "#"

count = 0
void = False
while current := source:
    if current in cave:
        break
    while True:
        if (n := add(current, (0, 1))) not in cave and n[1] < maxs[1] + 2:
            current = n
        elif (n := add(current, (-1, 1))) not in cave and n[1] < maxs[1] + 2:
            current = n
        elif (n := add(current, (1, 1))) not in cave and n[1] < maxs[1] + 2:
            current = n
        else:
            cave[current] = "o"
            count += 1
            break

print(count)
