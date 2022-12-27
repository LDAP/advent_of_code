# --- Day 16: Proboscidea Volcanium ---
# The sensors have led you to the origin of the distress signal: yet another handheld device, just like the one the Elves gave you. However, you don't see any Elves around; instead, the device is surrounded by elephants! They must have gotten lost in these tunnels, and one of the elephants apparently figured out how to turn on the distress signal.

# The ground rumbles again, much stronger this time. What kind of cave is this, exactly? You scan the cave with your handheld device; it reports mostly igneous rock, some ash, pockets of pressurized gas, magma... this isn't just a cave, it's a volcano!

# You need to get the elephants out of here, quickly. Your device estimates that you have 30 minutes before the volcano erupts, so you don't have time to go back out the way you came in.

# You scan the cave for other options and discover a network of pipes and pressure-release valves. You aren't sure how such a system got into a volcano, but you don't have time to complain; your device produces a report (your puzzle input) of each valve's flow rate if it were opened (in pressure per minute) and the tunnels you could use to move between the valves.

# There's even a valve in the room you and the elephants are currently standing in labeled AA. You estimate it will take you one minute to open a single valve and one minute to follow any tunnel from one valve to another. What is the most pressure you could release?

# For example, suppose you had the following scan output:

# Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
# Valve BB has flow rate=13; tunnels lead to valves CC, AA
# Valve CC has flow rate=2; tunnels lead to valves DD, BB
# Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
# Valve EE has flow rate=3; tunnels lead to valves FF, DD
# Valve FF has flow rate=0; tunnels lead to valves EE, GG
# Valve GG has flow rate=0; tunnels lead to valves FF, HH
# Valve HH has flow rate=22; tunnel leads to valve GG
# Valve II has flow rate=0; tunnels lead to valves AA, JJ
# Valve JJ has flow rate=21; tunnel leads to valve II
# All of the valves begin closed. You start at valve AA, but it must be damaged or jammed or something: its flow rate is 0, so there's no point in opening it. However, you could spend one minute moving to valve BB and another minute opening it; doing so would release pressure during the remaining 28 minutes at a flow rate of 13, a total eventual pressure release of 28 * 13 = 364. Then, you could spend your third minute moving to valve CC and your fourth minute opening it, providing an additional 26 minutes of eventual pressure release at a flow rate of 2, or 52 total pressure released by valve CC.


import re

MINS = 30
valves = {}


def purge(not_open, m, current_released, best):
    opport = 0
    for i, o in enumerate(reversed(sorted([valves[v][0] for v in not_open]))):
        if MINS - m - 2 * i <= 0:
            break
        opport += o * (MINS - m - 2 * i)
    return opport + current_released < best


with open("input.txt") as f:
    for ln in f:
        split = re.split("[ =;,]+", ln.strip())
        valves[split[1]] = [int(split[5]), split[10:]]

current = set([("AA", frozenset(), frozenset(valve for valve in valves if valves[valve][0] > 0), 0)])  # valve, open, not_open, released
nxt = set()
current_best = (0, [])
for m in range(1, MINS + 2):
    print(m)
    for valve, opened, not_open, released in current:
        if valve in not_open:
            new_released = released + (MINS - m) * valves[valve][0]
            new_not_open = not_open - frozenset([valve])
            new_opened = opened | frozenset([(valve, m)])
            if new_released > current_best[0]:
                current_best = (new_released, new_opened)

            if new_not_open and not purge(new_not_open, m + 1, new_released, current_best[0]):
                nxt.add((valve, new_opened, new_not_open, new_released,))

        for neigh in valves[valve][1]:
            if not purge(not_open, m + 1, released, current_best[0]):
                nxt.add((neigh, opened, not_open, released,))

    del current
    current = nxt
    nxt = set()

print(current_best)
