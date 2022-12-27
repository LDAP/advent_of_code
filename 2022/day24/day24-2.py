# --- Part Two ---
# As the expedition reaches the far side of the valley, one of the Elves looks especially dismayed:

# He forgot his snacks at the entrance to the valley!

# Since you're so good at dodging blizzards, the Elves humbly request that you go back for his snacks. From the same initial conditions, how quickly can you make it from the start to the goal, then back to the start, then back to the goal?

# In the above example, the first trip to the goal takes 18 minutes, the trip back to the start takes 23 minutes, and the trip back to the goal again takes 13 minutes, for a total time of 54 minutes.

# What is the fewest number of minutes required to reach the goal, go back to the start, then reach the goal again?


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

positions = set([END])
next_positions = set()

found = False
while not found:
    step(blizzards, dirs, next_blizzards)
    next_blizzards_set = set(next_blizzards)

    for position in positions:
        for d in DIRS + [(0, 0)]:
            maybe_next = add(position, d)
            if maybe_next == START:
                found = True
                break
            if not outside(maybe_next) and maybe_next not in next_blizzards:
                next_positions.add(maybe_next)

    next_positions.add(END)
    minute += 1
    next_blizzards, blizzards = blizzards, next_blizzards
    positions = next_positions
    next_positions = set()

positions = set([START])
next_positions = set()

found = False
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

    next_positions.add(START)
    minute += 1
    next_blizzards, blizzards = blizzards, next_blizzards
    positions = next_positions
    next_positions = set()

print(minute)
