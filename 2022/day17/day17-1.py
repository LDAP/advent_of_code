# --- Day 17: Pyroclastic Flow ---
# Your handheld device has located an alternative exit from the cave for you and the elephants. The ground is rumbling almost continuously now, but the strange valves bought you some time. It's definitely getting warmer in here, though.

# The tunnels eventually open into a very tall, narrow chamber. Large, oddly-shaped rocks are falling into the chamber from above, presumably due to all the rumbling. If you can't work out where the rocks will fall next, you might be crushed!

# The five types of rocks have the following peculiar shapes, where # is rock and . is empty space:

# ####

# .#.
# ###
# .#.

# ..#
# ..#
# ###

# #
# #
# #
# #

# ##
# ##
# The rocks fall in the order shown above: first the - shape, then the + shape, and so on. Once the end of the list is reached, the same order repeats: the - shape falls first, sixth, 11th, 16th, etc.

# The rocks don't spin, but they do get pushed around by jets of hot gas coming out of the walls themselves. A quick scan reveals the effect the jets of hot gas will have on the rocks as they fall (your puzzle input).

# For example, suppose this was the jet pattern in your cave:

# >>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
# In jet patterns, < means a push to the left, while > means a push to the right. The pattern above means that the jets will push a falling rock right, then right, then right, then left, then left, then right, and so on. If the end of the list is reached, it repeats.

# The tall, vertical chamber is exactly seven units wide. Each rock appears so that its left edge is two units away from the left wall and its bottom edge is three units above the highest rock in the room (or the floor, if there isn't one).

# After a rock appears, it alternates between being pushed by a jet of hot gas one unit (in the direction indicated by the next symbol in the jet pattern) and then falling one unit down. If any movement would cause any part of the rock to move into the walls, floor, or a stopped rock, the movement instead does not occur. If a downward movement would have caused a falling rock to move into the floor or an already-fallen rock, the falling rock stops where it is (having landed on something) and a new rock immediately begins falling.


NUM_ROCKS = 2022
W = 7
DL = 2
DB = 4
ROCKS = [
    {(0, 0), (1, 0), (2, 0), (3, 0)},
    {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)},
    {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},
    {(0, 0), (0, 1), (0, 2), (0, 3)},
    {(0, 0), (0, 1), (1, 0), (1, 1)}
]  # right, up
DOWN = (0, -1)

with open("input.txt", "r") as f:
    MOVES = [(1 if c == ">" else -1, 0) for c in f.read().strip()]


def add(rock, tup):
    return {(r[0] + tup[0], r[1] + tup[1]) for r in rock}


def illegal(rock):
    return any(r < 0 or r >= W for r, _ in rock)


def rock_g():
    for i in range(NUM_ROCKS):
        yield ROCKS[i % len(ROCKS)]


def print_chamber(chamber):
    top = max(h for _, h in chamber)
    bottom = min(h for _, h in chamber)
    for h in reversed(range(bottom, top + 1)):
        for w in range(W):
            if (w, h) in chamber:
                print("#", end="")
            else:
                print(".", end="")
        print()


move_counter = 0


def next_move():
    global move_counter
    move = MOVES[move_counter]
    move_counter = (move_counter + 1) % len(MOVES)
    return move


top = 0
chamber = {(i, 0) for i in range(W)}


for i, rock in enumerate(rock_g()):
    rock = add(rock, (DL, top + DB))

    while True:
        nxt = add(rock, next_move())
        if nxt.isdisjoint(chamber) and not illegal(nxt):
            rock = nxt
        nxt = add(rock, DOWN)
        if nxt.isdisjoint(chamber):
            rock = nxt
        else:
            chamber = chamber | rock
            top = max(max(u for _, u in rock), top)
            break

    # prune
    keep = set()
    for search_r in range(4):
        line = {(w, top - search_r) for w in range(W)}
        keep = keep | line
        if len(line & chamber) == W:
            chamber = chamber & keep
            break

print(top)
