# --- Day 24: Blizzard Basin ---
# With everything replanted for next year (and with elephants and monkeys to tend the grove), you and the Elves leave for the extraction point.

# Partway up the mountain that shields the grove is a flat, open area that serves as the extraction point. It's a bit of a climb, but nothing the expedition can't handle.

# At least, that would normally be true; now that the mountain is covered in snow, things have become more difficult than the Elves are used to.

# As the expedition reaches a valley that must be traversed to reach the extraction site, you find that strong, turbulent winds are pushing small blizzards of snow and sharp ice around the valley. It's a good thing everyone packed warm clothes! To make it across safely, you'll need to find a way to avoid them.

# Fortunately, it's easy to see all of this from the entrance to the valley, so you make a map of the valley and the blizzards (your puzzle input). For example:

# #.#####
# #.....#
# #>....#
# #.....#
# #...v.#
# #.....#
# #####.#
# The walls of the valley are drawn as #; everything else is ground. Clear ground - where there is currently no blizzard - is drawn as .. Otherwise, blizzards are drawn with an arrow indicating their direction of motion: up (^), down (v), left (<), or right (>).

# The above map includes two blizzards, one moving right (>) and one moving down (v). In one minute, each blizzard moves one position in the direction it is pointing:

# #.#####
# #.....#
# #.>...#
# #.....#
# #.....#
# #...v.#
# #####.#
# Due to conservation of blizzard energy, as a blizzard reaches the wall of the valley, a new blizzard forms on the opposite side of the valley moving in the same direction. After another minute, the bottom downward-moving blizzard has been replaced with a new downward-moving blizzard at the top of the valley instead:

# #.#####
# #...v.#
# #..>..#
# #.....#
# #.....#
# #.....#
# #####.#
# Because blizzards are made of tiny snowflakes, they pass right through each other. After another minute, both blizzards temporarily occupy the same position, marked 2:

# #.#####
# #.....#
# #...2.#
# #.....#
# #.....#
# #.....#
# #####.#
# After another minute, the situation resolves itself, giving each blizzard back its personal space:

# #.#####
# #.....#
# #....>#
# #...v.#
# #.....#
# #.....#
# #####.#
# Finally, after yet another minute, the rightward-facing blizzard on the right is replaced with a new one on the left facing the same direction:

# #.#####
# #.....#
# #>....#
# #.....#
# #...v.#
# #.....#
# #####.#
# This process repeats at least as long as you are observing it, but probably forever.

# Here is a more complex example:

# #.######
# #>>.<^<#
# #.<..<<#
# #>v.><>#
# #<^v^^>#
# ######.#
# Your expedition begins in the only non-wall position in the top row and needs to reach the only non-wall position in the bottom row. On each minute, you can move up, down, left, or right, or you can wait in place. You and the blizzards act simultaneously, and you cannot share a position with a blizzard.

# What is the fewest number of minutes required to avoid the blizzards and reach the goal?


# coords: (right, down)
from collections.abc import Callable
from typing import List, Tuple
import operator


RIGHT, DOWN, LEFT, UP = (1, 0), (0, 1), (-1, 0), (0, -1)
DIRS = [RIGHT, DOWN, LEFT, UP]
DIR_CHAR = [">", "v", "<", "^"]


Vec = Tuple[int, int]


def tupop(tup1: Vec, tup2: Vec, op: Callable[[int, int], int]) -> Vec:
    return tuple([op(t1, t2) for t1, t2 in zip(tup1, tup2)])


def add(tup1: Vec, tup2: Vec) -> Vec:
    return tupop(tup1, tup2, operator.add)


def mod(tup1: Vec, tup2: Vec) -> Vec:
    return tupop(tup1, tup2, operator.mod)


with open("input.txt") as f:
    lines = f.read().splitlines(False)
    SIZE = (len(lines[0]) - 2, len(lines) - 2)
    blizzards, next_blizzards, dirs = [], [], []
    for y, line in enumerate(lines[1:-1]):
        for x, c in enumerate(line[1:-1]):
            if c in DIR_CHAR:
                dr = DIRS[DIR_CHAR.index(c)]
                ps = (x, y)
                blizzards.append(ps)
                dirs.append(dr)
                next_blizzards.append(ps)


START = (0, -1)
END = add(SIZE, (-1, 0))


def step(blizzards: List[Vec], dirs: List[Vec], next_blizzards: List[Vec]):
    for i, blizzard in enumerate(blizzards):
        next_blizzards[i] = mod(add(blizzard, dirs[i]), SIZE)


def outside(tup: Vec):
    return any(t < 0 for t in tup) or tup[0] >= SIZE[0] or tup[1] >= SIZE[1]


positions = set([START])
next_positions = set()

found = False
minute = 0
while not found:
    step(blizzards, dirs, next_blizzards)
    next_blizzards_set = set(next_blizzards)

    for position in positions:
        for d in DIRS + [(0, 0)]:
            maybe_next = add(position, d)
            if maybe_next == END:
                found = True
                break
            if not outside(maybe_next) and maybe_next not in next_blizzards:
                next_positions.add(maybe_next)

    minute += 1
    next_blizzards, blizzards = blizzards, next_blizzards
    positions = next_positions
    next_positions = set()

print(minute)
