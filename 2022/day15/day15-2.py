# --- Part Two ---
# Your handheld device indicates that the distress signal is coming from a beacon nearby. The distress beacon is not detected by any sensor, but the distress beacon must have x and y coordinates each no lower than 0 and no larger than 4000000.

# To isolate the distress beacon's signal, you need to determine its tuning frequency, which can be found by multiplying its x coordinate by 4000000 and then adding its y coordinate.

# In the example above, the search space is smaller: instead, the x and y coordinates can each be at most 20. With this reduced search area, there is only a single position that could have a beacon: x=14, y=11. The tuning frequency for this distress beacon is 56000011.

# Find the only possible position for the distress beacon. What is its tuning frequency?


import re


def man(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


MAX = 4000000
ss = []
with open("input.txt") as f:
    for ln in f:
        sp = re.split(r"[ ,=:\n]", ln)
        s, b = (int(sp[3]), int(sp[6])), (int(sp[13]), int(sp[16]))
        r = man(s, b)
        ss.append([s, b, r])

becon = None
for y in range(MAX + 1):
    if becon:
        break

    intvs = []
    for s in ss:
        dy = abs(s[0][1] - y)
        dx = s[2] - dy
        if dx >= 0 and s[0][0] + dx + 1 > 0:
            intvs.append((s[0][0] - dx, "a"))
            intvs.append((s[0][0] + dx + 1, "z"))
    intvs.sort()

    if intvs[0][0] > 0:
        becon = (0, y)
        break

    count = 0
    for intv in intvs:
        match intv:
            case c, "a":
                count += 1
            case c, "z":
                count -= 1

                if count == 0 and c < MAX:
                    becon = (c, y)
                    break

if becon:
    print(becon[0] * 4000000 + becon[1])
