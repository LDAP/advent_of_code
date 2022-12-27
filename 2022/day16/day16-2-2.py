# You're worried that even with an optimal approach, the pressure released won't be enough. What if you got one of the elephants to help you?

# It would take you 4 minutes to teach an elephant how to open the right valves in the right order, leaving you with only 26 minutes to actually execute your plan. Would having two of you working together be better, even if it means having less time? (Assume that you teach the elephant before opening any valves yourself, giving you both the same full 26 minutes.)


import re

MINS = 26
valves = {}


def get_valves(s: int):
    for i in range(64):
        p = (1 << i)
        if p & s > 0:
            yield p


def purge(not_open: int, m, current_released, best):
    opport = 0
    for i, o in enumerate(reversed(sorted([valves[v][0] for v in get_valves(not_open)]))):
        if MINS - m - 2 * i <= 0:
            break
        opport += o * (MINS - m - 2 * i)
    return opport + current_released < best


valve_to_int = {"AA": 1}
counter = 2


# Bitsets ;)
def get_int(valve):
    global counter
    if valve not in valve_to_int:
        valve_to_int[valve] = counter
        counter *= 2
    return valve_to_int[valve]


with open("input.txt") as f:
    for ln in f:
        split = re.split("[ =;,]+", ln.strip())
        valves[get_int(split[1])] = [int(split[5]), [get_int(v) for v in split[10:]]]

current = set([(1, 0, sum(valve for valve in valves if valves[valve][0] > 0), 0)])  # valve, open, not_open, released
nxt = set()
current_bests = {}
current_best = 0
for m in range(1, MINS + 2):
    print(m)
    for valve, opened, not_open, released in current:
        if (valve & not_open) > 0:
            new_released = released + (MINS - m) * valves[valve][0]
            new_not_open = not_open ^ valve
            new_opened = opened ^ valve

            current_bests[new_opened] = max(new_released, current_bests.get(new_opened, 0))
            if new_released > current_best:
                current_best = new_released

            if new_not_open and not purge(new_not_open, m + 1, new_released, current_best):
                nxt.add((valve, new_opened, new_not_open, new_released,))

        for neigh in valves[valve][1]:
            if not purge(not_open, m + 1, released, current_best):
                nxt.add((neigh, opened, not_open, released,))

    del current
    current = nxt
    nxt = set()


best_sum = 0
for s1, v1 in current_bests.items():
    for s2, v2 in current_bests.items():
        if (s := v1 + v2) > best_sum and s1 & s2 == 0:
            best_sum = s

print(best_sum)
