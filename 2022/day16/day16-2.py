# You're worried that even with an optimal approach, the pressure released won't be enough. What if you got one of the elephants to help you?

# It would take you 4 minutes to teach an elephant how to open the right valves in the right order, leaving you with only 26 minutes to actually execute your plan. Would having two of you working together be better, even if it means having less time? (Assume that you teach the elephant before opening any valves yourself, giving you both the same full 26 minutes.)


import re

MINS = 26
valves = {}
current_best = 0


def purge(not_open, m, current_released, best):
    opport = 0
    for i, o in enumerate(reversed(sorted([valves[v][0] for v in not_open]))):
        if MINS - m - 2 * (i // 2) <= 0:
            break
        opport += o * (MINS - m - 2 * (i // 2))
    return opport + current_released < best


def process(valve, valve2, not_open, released, into: set):
    global current_best
    if valve in not_open:
        new_released = released + (MINS - m) * valves[valve][0]
        new_not_open = not_open - frozenset([valve])
        current_best = max(current_best, new_released)

        if new_not_open and not purge(new_not_open, m + 1, new_released, current_best):
            into.add((valve, valve2, new_not_open, new_released,))

    for neigh in valves[valve][1]:
        if not purge(not_open, m + 1, released, current_best):
            into.add((neigh, valve2, not_open, released,))


with open("input.txt") as f:
    for ln in f:
        split = re.split("[ =;,]+", ln.strip())
        valves[split[1]] = [int(split[5]), split[10:]]

current = set([("AA", "AA", frozenset(valve for valve in valves if valves[valve][0] > 0), 0)])  # valve, valve2, not_open, released
nxt = set()

for m in range(1, MINS + 2):
    print(m)
    current2 = set()
    for valve, valve2, not_open, released in current:
        process(valve, valve2, not_open, released, current2)

    del current

    for valve2, valve, not_open, released in current2:
        process(valve, valve2, not_open, released, nxt)

    del current2

    current = nxt
    nxt = set()

print(current_best)
