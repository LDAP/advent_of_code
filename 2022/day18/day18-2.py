# Something seems off about your calculation. The cooling rate depends on exterior surface area, but your calculation also included the surface area of air pockets trapped in the lava droplet.

# Instead, consider only cube sides that could be reached by the water and steam as the lava droplet tumbles into the pond. The steam will expand to reach as much as possible, completely displacing any air on the outside of the lava droplet but never expanding diagonally.

# In the larger example above, exactly one cube of air is trapped within the lava droplet (at 2,2,5), so the exterior surface area of the lava droplet is 58.

# What is the exterior surface area of your scanned lava droplet?



from operator import le, add, sub, ge

def neighbors(coord):
    for i in range(len(coord)):
        for d in [-1, 1]:
            yield (*coord[:i],coord[i] + d, *coord[i + 1:])


def tupop(tup1, tup2, op):
    return tuple(op(t1, t2) for t1, t2 in zip(tup1, tup2))


maxs = (-1000,) * 3
mins = (1000,) * 3


with open("input.txt") as f:
    lava = {tuple(map(int, s.strip().split(","))) for s in f}
    for d in lava:
        maxs = tupop(maxs, tupop(d, (1, 1, 1), add), max)
        mins = tupop(mins, tupop(d, (1, 1, 1), sub), min)


# BFS
outside = set()
visited = set([maxs])
q = [maxs]

while q:
    cur = q.pop(0)
    for n2 in neighbors(cur):
        if n2 not in lava and all(tupop(n2, maxs, le)) and all(tupop(n2, mins, ge)) and n2 not in visited:
            visited.add(n2)
            q.append(n2)

for v in visited:
    outside.add(v)

print(sum([len([n for n in neighbors(d) if n in outside]) for d in lava]))
