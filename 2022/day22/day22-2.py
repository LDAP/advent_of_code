# --- Part Two ---
# As you reach the force field, you think you hear some Elves in the distance. Perhaps they've already arrived?

# You approach the strange input device, but it isn't quite what the monkeys drew in their notes. Instead, you are met with a large cube; each of its six faces is a square of 50x50 tiles.

# To be fair, the monkeys' map does have six 50x50 regions on it. If you were to carefully fold the map, you should be able to shape it into a cube!

# In the example above, the six (smaller, 4x4) faces of the cube are:

#         1111
#         1111
#         1111
#         1111
# 222233334444
# 222233334444
# 222233334444
# 222233334444
#         55556666
#         55556666
#         55556666
#         55556666
# You still start in the same position and with the same facing as before, but the wrapping rules are different. Now, if you would walk off the board, you instead proceed around the cube. From the perspective of the map, this can look a little strange. In the above example, if you are at A and move to the right, you would arrive at B facing down; if you are at C and move down, you would arrive at D facing up:

#         ...#
#         .#..
#         #...
#         ....
# ...#.......#
# ........#..A
# ..#....#....
# .D........#.
#         ...#..B.
#         .....#..
#         .#......
#         ..C...#.
# Walls still block your path, even if they are on a different face of the cube. If you are at E facing up, your movement is blocked by the wall marked by the arrow:

#         ...#
#         .#..
#      -->#...
#         ....
# ...#..E....#
# ........#...
# ..#....#....
# ..........#.
#         ...#....
#         .....#..
#         .#......
#         ......#.
# Using the same method of drawing the last facing you had with an arrow on each tile you visit, the full path taken by the above example now looks like this:

#         >>v#
#         .#v.
#         #.v.
#         ..v.
# ...#..^...v#
# .>>>>>^.#.>>
# .^#....#....
# .^........#.
#         ...#..v.
#         .....#v.
#         .#v<<<<.
#         ..v...#.
# The final password is still calculated from your final position and facing from the perspective of the map. In this example, the final row is 5, the final column is 7, and the final facing is 3, so the final password is 1000 * 5 + 4 * 7 + 3 = 5031.

# Fold the map into a cube, then follow the path given in the monkeys' notes. What is the final password?


import re

with open("input.txt") as f:
    lines = f.read().splitlines(keepends=False)

splitter = lines.index("")
mp = lines[:splitter]
dirs = lines[splitter + 1]

rows = []
columns = []

max_row = max([len(s) for s in mp])

for i in range(len(mp)):
    rows.append((mp[i].count(" "), len(mp[i])))
    mp[i] += " " * (max_row - len(mp[i]))


mp_t = list("".join(s) for s in zip(*mp))
for i in range(len(mp_t)):
    columns.append((mp_t[i].rstrip().count(" "), len(mp_t[i].rstrip())))

# down, right
RIGHT, DOWN, LEFT, UP = 0, 1, 2, 3  # d_down, d_right
CW = 50

moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
current_move = 0
current_pos = (0, rows[0][0])

# lambda -> (blockdr, coord_dr, move), down, right
magic_moves = {
    (0, 1): {
        LEFT: lambda d, r: ((2, 0), (CW - d - 1, 0), RIGHT),
        UP: lambda d, r: ((3, 0), (r, 0), RIGHT),
    },
    (0, 2): {
        UP: lambda d, r: ((3, 0), (CW - 1, r), UP),
        RIGHT: lambda d, r: ((2, 1), (CW - d - 1, CW - 1), LEFT),
        DOWN: lambda d, r: ((1, 1), (r, CW - 1), LEFT),
    },
    (1, 1): {
        LEFT: lambda d, r: ((2, 0), (0, d), DOWN),
        RIGHT: lambda d, r: ((0, 2), (CW - 1, d), UP),
    },
    (2, 0): {
        UP: lambda d, r: ((1, 1), (r, 0), RIGHT),
        LEFT: lambda d, r: ((0, 1), (CW - 1 - d, 0), RIGHT),
    },
    (2, 1): {
        RIGHT: lambda d, r: ((0, 2), (CW - 1 - d, CW - 1), LEFT),
        DOWN: lambda d, r: ((3, 0), (r, CW - 1), LEFT),
    },
    (3, 0): {
        RIGHT: lambda d, r: ((2, 1), (CW - 1, d), UP),
        DOWN: lambda d, r: ((0, 2), (0, r), DOWN),
        LEFT: lambda d, r: ((0, 1), (0, d), DOWN),
    },
}


def wrap(i, rc):
    return ((i - rc[0]) % (rc[1] - rc[0])) + rc[0]


def nxt(current_pos, current_move: int):
    next_row_not_wrapped = current_pos[0] + moves[current_move][0]
    next_col_not_wrapped = current_pos[1] + moves[current_move][1]

    next_row = wrap(next_row_not_wrapped, columns[current_pos[1]])
    next_col = wrap(next_col_not_wrapped, rows[current_pos[0]])

    if next_row != next_row_not_wrapped or next_col != next_col_not_wrapped:
        # Wrap
        current_block = (current_pos[0] // CW, current_pos[1] // CW)
        current_block_coords = (current_pos[0] % CW, current_pos[1] % CW)
        next_block, next_block_coords, next_move = magic_moves[current_block][current_move](*current_block_coords)
        return (next_block[0] * CW + next_block_coords[0], next_block[1] * CW + next_block_coords[1]), next_move
    else:
        return (next_row, next_col), current_move


def do_move():
    global current_move, current_pos, moves, mp
    maybe_next, maybe_next_move = nxt(current_pos, current_move)
    if mp[maybe_next[0]][maybe_next[1]] == ".":
        current_pos = maybe_next
        current_move = maybe_next_move


for m in re.findall(r"(\d+|R|L)", dirs):
    match m:
        case "R":
            current_move = (current_move + 1) % len(moves)
        case "L":
            current_move = (current_move - 1) % len(moves)
        case c:
            for i in range(int(c)):
                do_move()

print(1000 * (current_pos[0] + 1) + 4 * (current_pos[1] + 1) + current_move)
