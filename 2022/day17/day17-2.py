# --- Part Two ---
# The elephants are not impressed by your simulation. They demand to know how tall the tower will be after 1000000000000 rocks have stopped! Only then will they feel confident enough to proceed through the cave.

# In the example above, the tower would be 1514285714288 units tall!


NUM_ROCKS = 1000000000000

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


def simulate(num_rocks):
    move_counter = 0

    def next_move():
        nonlocal move_counter
        move = MOVES[move_counter]
        move_counter = (move_counter + 1) % len(MOVES)
        return move

    top = 0
    bottom = 0
    chamber = {(i, 0) for i in range(W)}

    tops = [0] * (num_rocks + 1)

    def rock_g():
        for i in range(num_rocks):
            yield ROCKS[i % len(ROCKS)]

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

        # prune (searches for full lines, not working on example...)
        # keep = set()
        # for search_r in range(top - bottom + 1):
        #     line = {(w, top - search_r) for w in range(W)}
        #     keep = keep | line
        #     if len(line & chamber) == W:
        #         if chamber != (n := chamber & keep):
        #             chamber = n
        #             bottom = top - search_r
        #             # print(f"{i} {top - bottom}")
        #             break

        tops[i + 1] = top

    return tops


# Find period
period = 0
period_height = 0
MAX_PERIOD = 2000
MIN_PERIOD = 100
CHECKS = 6
tops = simulate(MAX_PERIOD * CHECKS)
for i in range(MIN_PERIOD, MAX_PERIOD + 1):
    cur = tops[i]
    diffs = set()
    for j in range(2, CHECKS + 1):
        diffs.add((tops[i * j] - cur) // (j - 1))
    if len(diffs) == 1:
        period = i
        period_height = diffs.pop()
        break

print(f"Found period {period}")
print(f"Height {(NUM_ROCKS // period) * period_height + tops[NUM_ROCKS % period]}")
