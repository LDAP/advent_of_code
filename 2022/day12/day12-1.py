# --- Day 12: Hill Climbing Algorithm ---
# You try contacting the Elves using your handheld device, but the river you're following must be too low to get a decent signal.

# You ask the device for a heightmap of the surrounding area (your puzzle input). The heightmap shows the local area from above broken into a grid; the elevation of each square of the grid is given by a single lowercase letter, where a is the lowest elevation, b is the next-lowest, and so on up to the highest elevation, z.

# Also included on the heightmap are marks for your current position (S) and the location that should get the best signal (E). Your current position (S) has elevation a, and the location that should get the best signal (E) has elevation z.

# You'd like to reach E, but to save energy, you should do it in as few steps as possible. During each step, you can move exactly one square up, down, left, or right. To avoid needing to get out your climbing gear, the elevation of the destination square can be at most one higher than the elevation of your current square; that is, if your current elevation is m, you could step to elevation n, but not to elevation o. (This also means that the elevation of the destination square can be much lower than the elevation of your current square.)

# For example:

# Sabqponm
# abcryxxl
# accszExk
# acctuvwj
# abdefghi
# Here, you start in the top-left corner; your goal is near the middle. You could start by moving down or right, but eventually you'll need to head toward the e at the bottom. From there, you can spiral around to the goal:

# v..v<<<<
# >v.vv<<^
# .>vv>E^^
# ..v>>>^^
# ..>>>>>^
# In the above diagram, the symbols indicate whether the path exits each square moving up (^), down (v), left (<), or right (>). The location that should get the best signal is still E, and . marks unvisited squares.

# This path reaches the goal in 31 steps, the fewest possible.

# What is the fewest steps required to move from your current position to the location that should get the best signal?


from string import ascii_lowercase
import sys

s = 0
e = 0
w = 0
field = []
with open("input.txt", "r") as f:
    for i, ln in enumerate(f):
        ln = ln.strip()
        w = len(ln)
        for j, c in enumerate(ln):
            if c == "S":
                s = i * w + j
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

visited = [False] * len(field)
dist = [0] * len(field)
parent = [-1] * len(field)

q = [s]
visited[s] = True

while q:
    cur = q.pop(0)

    if cur == e:
        print(dist[e])
        sys.exit(0)

    for c in graph[cur]:
        if not visited[c]:
            q.append(c)
            visited[c] = True
            parent[c] = cur
            dist[c] = dist[cur] + 1
