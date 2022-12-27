# --- Part Two ---
# As you walk up the hill, you suspect that the Elves will want to turn this into a hiking trail. The beginning isn't very scenic, though; perhaps you can find a better starting point.

# To maximize exercise while hiking, the trail should start as low as possible: elevation a. The goal is still the square marked E. However, the trail should still be direct, taking the fewest steps to reach its goal. So, you'll need to find the shortest path from any square at elevation a to the square marked E.

# Again consider the example from above:

# Sabqponm
# abcryxxl
# accszExk
# acctuvwj
# abdefghi
# Now, there are six choices for starting position (five marked a, plus the square marked S that counts as being at elevation a). If you start at the bottom-left square, you can reach the goal most quickly:

# ...v<<<<
# ...vv<<^
# ...v>E^^
# .>v>>>^^
# >^>>>>>^
# This path reaches the goal in only 29 steps, the fewest possible.

# What is the fewest steps required to move starting from any square with elevation a to the location that should get the best signal?


from string import ascii_lowercase

e = 0
w = 0
field = []
with open("input.txt", "r") as f:
    for i, ln in enumerate(f):
        ln = ln.strip()
        w = len(ln)
        for j, c in enumerate(ln):
            if c == "S":
                c = "a"
            if c == "E":
                e = i * w + j
                c = "z"
            if c in ascii_lowercase:
                field.append(ascii_lowercase.index(c))

graph = [[] for _ in range(len(field))]


def connect(i, j):
    if 0 <= i < len(field) and 0 <= j < len(field):
        if field[i] + 1 >= field[j]:
            graph[i].append(j)


for i, _ in enumerate(field):
    connect(i, i - w)
    connect(i, i + w)
    connect(i, i - 1)
    connect(i, i + 1)

min_dist = len(field) ** 3

for s in [i for i, f in enumerate(field) if f == 0]:
    visited = [False] * len(field)
    dist = [0] * len(field)
    parent = [-1] * len(field)

    q = [s]
    visited[s] = True

    while q:
        cur = q.pop(0)

        if cur == e:
            min_dist = min(min_dist, dist[e])
            break

        for c in graph[cur]:
            if not visited[c]:
                q.append(c)
                visited[c] = True
                parent[c] = cur
                dist[c] = dist[cur] + 1

print(min_dist)
