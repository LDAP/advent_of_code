# --- Day 19: Not Enough Minerals ---
# Your scans show that the lava did indeed form obsidian!

# The wind has changed direction enough to stop sending lava droplets toward you, so you and the elephants exit the cave. As you do, you notice a collection of geodes around the pond. Perhaps you could use the obsidian to create some geode-cracking robots and break them open?

# To collect the obsidian from the bottom of the pond, you'll need waterproof obsidian-collecting robots. Fortunately, there is an abundant amount of clay nearby that you can use to make them waterproof.

# In order to harvest the clay, you'll need special-purpose clay-collecting robots. To make any type of robot, you'll need ore, which is also plentiful but in the opposite direction from the clay.

# Collecting ore requires ore-collecting robots with big drills. Fortunately, you have exactly one ore-collecting robot in your pack that you can use to kickstart the whole operation.

# Each robot can collect 1 of its resource type per minute. It also takes one minute for the robot factory (also conveniently from your pack) to construct any type of robot, although it consumes the necessary resources available when construction begins.

# The robot factory has many blueprints (your puzzle input) you can choose from, but once you've configured it with a blueprint, you can't change it. You'll need to work out which blueprint is best.

# The elephants are starting to look hungry, so you shouldn't take too long; you need to figure out which blueprint would maximize the number of opened geodes after 24 minutes by figuring out which robots to build and when to build them.


from itertools import count
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


MINUTES = 24
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
for i, bp in enumerate(bps):
    print(f"{i + 1} / {len(bps)}")
    # Robots, Resources, geode
    states = {((1, 0, 0), (0, 0, 0), 0)}
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
                    next_robots = tuple(robots[i] + (robot[1] == i) for i in range(3))
                    next_resources = add(sub(resources, robot[0]), robots)
                    best_geode = max(best_geode, next_geode)
                    next_states.add((next_robots, next_resources, next_geode))

        states = next_states
        next_states = set()
    best_geodes.append(best_geode)
    print()


print(best_geodes)
print(sum([a * b for a, b in zip(best_geodes, count(1))]))
