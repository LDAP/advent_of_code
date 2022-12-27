# It seems you're on the right track. Finish simulating the process and figure out where the Elves need to go. How many rounds did you save them?

# In the example above, the first round where no Elf moved was round 20:

# .......#......
# ....#......#..
# ..#.....#.....
# ......#.......
# ...#....#.#..#
# #.............
# ....#.....#...
# ..#.....#.....
# ....#.#....#..
# .........#....
# ....#......#..
# .......#......
# Figure out where the Elves need to go. What is the number of the first round where no Elf moves?


import operator

NUM_ROUNDS = 10

# Right, Up
DIRS = [(0, 1), (0, -1), (-1, 0), (1, 0)]


def tupop(tup1, tup2, op):
    return tuple([op(t1, t2) for t1, t2 in zip(tup1, tup2)])


def add(tup1, tup2):
    return tupop(tup1, tup2, operator.add)


def get_neighbors_in_dir(tup, dir):
    for i in [-1, 0, 1]:
        yield add(add(tup, dir), (abs(dir[1]) * i, abs(dir[0]) * i))


def propose(elve, pos, d: dict):
    # print(f"Elve {elve} proposes {pos}")
    if pos in d:
        d[pos] += 1
    else:
        d[pos] = 1


def max_mins(elves):
    maxs = (-(1 << 31),) * 2
    mins = (+(1 << 31),) * 2

    for elve in elves:
        maxs = tupop(elve, maxs, max)
        mins = tupop(elve, mins, min)

    return maxs, mins


def print_elves(elves):
    maxs, mins = max_mins(elves)
    for y in reversed(range(mins[1], maxs[1] + 1)):
        for x in range(mins[0], maxs[0] + 1):
            if (x, y) in elves:
                print("#", end="")
            else:
                print(".", end="")
        print()


NEIGHBORS = list(set([i for sl in [list(get_neighbors_in_dir((0, 0), d)) for d in DIRS] for i in sl]))
NEIGHBORS_FOR_DIR = [set(get_neighbors_in_dir((0, 0), d)) for d in DIRS]

elves = set()

with open("input.txt") as f:
    y = 0
    for ln in f:
        for x, c in enumerate(ln.strip()):
            if c == "#":
                elves.add((x, y))
        y -= 1


# print_elves(elves)
# print()


i = 0
while True:
    prop_nums = {}
    props = []
    moved = False
    for elve in elves:
        proposed = False
        neighs = set(add(elve, d) for d in NEIGHBORS)
        if elves.isdisjoint(neighs):
            propose(elve, elve, prop_nums)
            proposed = True
            props.append(elve)
            continue
        moved = True
        for d in range(4):
            dir_index = (i + d) % len(DIRS)
            neigh_in_dir = set(add(elve, d) for d in NEIGHBORS_FOR_DIR[dir_index])
            if elves.isdisjoint(neigh_in_dir):
                pos = add(elve, DIRS[dir_index])
                propose(elve, pos, prop_nums)
                props.append(pos)
                proposed = True
                break
        if not proposed:
            propose(elve, elve, prop_nums)
            props.append(elve)

    new_elves = set()
    for elve, pos in zip(elves, props):
        if prop_nums[pos] == 1:
            new_elves.add(pos)
        else:
            new_elves.add(elve)
    elves = new_elves
    i += 1
    if not moved:
        break
    # print_elves(elves)
    # print()


maxs, mins = max_mins(elves)

print((abs(maxs[0] - mins[0]) + 1) * (abs(maxs[1] - mins[1]) + 1) - len(elves))
print(i)
