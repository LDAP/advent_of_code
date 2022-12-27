# --- Day 23: Unstable Diffusion ---
# You enter a large crater of gray dirt where the grove is supposed to be. All around you, plants you imagine were expected to be full of fruit are instead withered and broken. A large group of Elves has formed in the middle of the grove.

# "...but this volcano has been dormant for months. Without ash, the fruit can't grow!"

# You look up to see a massive, snow-capped mountain towering above you.

# "It's not like there are other active volcanoes here; we've looked everywhere."

# "But our scanners show active magma flows; clearly it's going somewhere."

# They finally notice you at the edge of the grove, your pack almost overflowing from the random star fruit you've been collecting. Behind you, elephants and monkeys explore the grove, looking concerned. Then, the Elves recognize the ash cloud slowly spreading above your recent detour.

# "Why do you--" "How is--" "Did you just--"

# Before any of them can form a complete question, another Elf speaks up: "Okay, new plan. We have almost enough fruit already, and ash from the plume should spread here eventually. If we quickly plant new seedlings now, we can still make it to the extraction point. Spread out!"

# The Elves each reach into their pack and pull out a tiny plant. The plants rely on important nutrients from the ash, so they can't be planted too close together.

# There isn't enough time to let the Elves figure out where to plant the seedlings themselves; you quickly scan the grove (your puzzle input) and note their positions.

# For example:

# ....#..
# ..###.#
# #...#.#
# .#...##
# #.###..
# ##.#.##
# .#..#..
# The scan shows Elves # and empty ground .; outside your scan, more empty ground extends a long way in every direction. The scan is oriented so that north is up; orthogonal directions are written N (north), S (south), W (west), and E (east), while diagonal directions are written NE, NW, SE, SW.

# The Elves follow a time-consuming process to figure out where they should each go; you can speed up this process considerably. The process consists of some number of rounds during which Elves alternate between considering where to move and actually moving.

# During the first half of each round, each Elf considers the eight positions adjacent to themself. If no other Elves are in one of those eight positions, the Elf does not do anything during this round. Otherwise, the Elf looks in each of four directions in the following order and proposes moving one step in the first valid direction:

# If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north one step.
# If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south one step.
# If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west one step.
# If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east one step.
# After each Elf has had a chance to propose a move, the second half of the round can begin. Simultaneously, each Elf moves to their proposed destination tile if they were the only Elf to propose moving to that position. If two or more Elves propose moving to the same position, none of those Elves move.

# Finally, at the end of the round, the first direction the Elves considered is moved to the end of the list of directions. For example, during the second round, the Elves would try proposing a move to the south first, then west, then east, then north. On the third round, the Elves would first consider west, then east, then north, then south.

# To make sure they're on the right track, the Elves like to check after round 10 that they're making good progress toward covering enough ground. To do this, count the number of empty ground tiles contained by the smallest rectangle that contains every Elf. (The edges of the rectangle should be aligned to the N/S/E/W directions; the Elves do not have the patience to calculate arbitrary rectangles.) In the above example, that rectangle is:

# ......#.....
# ..........#.
# .#.#..#.....
# .....#......
# ..#.....#..#
# #......##...
# ....##......
# .#........#.
# ...#.#..#...
# ............
# ...#..#..#..
# In this region, the number of empty ground tiles is 110.

# Simulate the Elves' process and find the smallest rectangle that contains the Elves after 10 rounds. How many empty ground tiles does that rectangle contain?


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


first_dir = 0
for _ in range(NUM_ROUNDS):
    prop_nums = {}
    props = []
    for elve in elves:
        proposed = False
        neighs = set(add(elve, d) for d in NEIGHBORS)
        if elves.isdisjoint(neighs):
            propose(elve, elve, prop_nums)
            proposed = True
            props.append(elve)
            continue
        for d in range(4):
            dir_index = (first_dir + d) % len(DIRS)
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
    first_dir += 1
    # print_elves(elves)
    # print()


maxs, mins = max_mins(elves)

print((abs(maxs[0] - mins[0]) + 1) * (abs(maxs[1] - mins[1]) + 1) - len(elves))
