# While you were choosing the best blueprint, the elephants found some food on their own, so you're not in as much of a hurry; you figure you probably have 32 minutes before the wind changes direction again and you'll need to get out of range of the erupting volcano.

# Unfortunately, one of the elephants ate most of your blueprint list! Now, only the first three blueprints in your list are intact.


from functools import reduce
from typing import List, Tuple


# Costs, Generates
Robot = Tuple[Tuple[int, int, int], int]
Blueprint = List[Robot]


def add(tup1, tup2):
    return tuple(a + b for a, b in zip(tup1, tup2))


def sub(tup1, tup2):
    return tuple(a - b for a, b in zip(tup1, tup2))


def can_buy(resources, robot: Robot):
    return all(tuple(a >= b for a, b in zip(resources, robot[0])))


def prune(geode, m):
    return geode + sum((MINUTES - r - 1) for r in range(m, MINUTES + 1)) < best_geode


MINUTES = 32
bps: List[Blueprint] = []
mats = ["ore", "clay", "obsidian", "geode"]

with open("input.txt") as f:
    for ln in f:
        bp = []
        for robot in ln.split(": ")[1].split(".")[:-1]:
            split = robot.split()
            costs = [0] * 4
            for i, c in enumerate(split[2:]):
                if c in mats:
                    costs[mats.index(c)] = int(split[i + 1])
            bp.append((tuple(costs), int(mats.index(split[1]))))
        bps.append(bp)


best_geodes = []
for i, bp in enumerate(bps[:3]):
    print(f"{i + 1} / 3 ")
    # Robots, Resources, geode
    states = {((1, 0, 0, 0), (0, 0, 0, 0), 0)}
    next_states = set()
    best_geode = 0

    for m in range(0, MINUTES + 1):
        print(f"{m} ", end="", flush=True)
        for robots, resources, geode in states:
            if prune(geode, m):
                continue

            # Do nothing
            if not prune(geode, m + 1):
                next_states.add((robots, add(resources, robots), geode))

            # Buy robots (only one robot can be built per minute)
            for robot in bp:
                if can_buy(resources, robot):
                    next_geode = geode + (MINUTES - m - 1) * (robot[1] == 3)
                    if prune(next_geode, m + 1):
                        continue
                    next_robots = (*robots[:robot[1]], robots[robot[1]] + 1, *robots[robot[1] + 1:])
                    next_resources = add(sub(resources, robot[0]), robots)
                    best_geode = max(best_geode, next_geode)
                    next_states.add((next_robots, next_resources, next_geode))

        states = next_states
        next_states = set()
    best_geodes.append(best_geode)
    print()


print(best_geodes)
print(reduce(lambda x, y: x * y, best_geodes))
