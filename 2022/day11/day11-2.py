# --- Part Two ---
# You're worried you might not ever get your items back. So worried, in fact, that your relief that a monkey's inspection didn't damage an item no longer causes your worry level to be divided by three.

# Unfortunately, that relief was all that was keeping your worry levels from reaching ridiculous levels. You'll need to find another way to keep your worry levels manageable.

# At this rate, you might be putting up with these monkeys for a very long time - possibly 10000 rounds!

# With these new rules, you can still figure out the monkey business after 10000 rounds. Using the same example above:

# == After round 1 ==
# Monkey 0 inspected items 2 times.
# Monkey 1 inspected items 4 times.
# Monkey 2 inspected items 3 times.
# Monkey 3 inspected items 6 times.

# == After round 20 ==
# Monkey 0 inspected items 99 times.
# Monkey 1 inspected items 97 times.
# Monkey 2 inspected items 8 times.
# Monkey 3 inspected items 103 times.

# == After round 1000 ==
# Monkey 0 inspected items 5204 times.
# Monkey 1 inspected items 4792 times.
# Monkey 2 inspected items 199 times.
# Monkey 3 inspected items 5192 times.

# == After round 2000 ==
# Monkey 0 inspected items 10419 times.
# Monkey 1 inspected items 9577 times.
# Monkey 2 inspected items 392 times.
# Monkey 3 inspected items 10391 times.

# == After round 3000 ==
# Monkey 0 inspected items 15638 times.
# Monkey 1 inspected items 14358 times.
# Monkey 2 inspected items 587 times.
# Monkey 3 inspected items 15593 times.

# == After round 4000 ==
# Monkey 0 inspected items 20858 times.
# Monkey 1 inspected items 19138 times.
# Monkey 2 inspected items 780 times.
# Monkey 3 inspected items 20797 times.

# == After round 5000 ==
# Monkey 0 inspected items 26075 times.
# Monkey 1 inspected items 23921 times.
# Monkey 2 inspected items 974 times.
# Monkey 3 inspected items 26000 times.

# == After round 6000 ==
# Monkey 0 inspected items 31294 times.
# Monkey 1 inspected items 28702 times.
# Monkey 2 inspected items 1165 times.
# Monkey 3 inspected items 31204 times.

# == After round 7000 ==
# Monkey 0 inspected items 36508 times.
# Monkey 1 inspected items 33488 times.
# Monkey 2 inspected items 1360 times.
# Monkey 3 inspected items 36400 times.

# == After round 8000 ==
# Monkey 0 inspected items 41728 times.
# Monkey 1 inspected items 38268 times.
# Monkey 2 inspected items 1553 times.
# Monkey 3 inspected items 41606 times.

# == After round 9000 ==
# Monkey 0 inspected items 46945 times.
# Monkey 1 inspected items 43051 times.
# Monkey 2 inspected items 1746 times.
# Monkey 3 inspected items 46807 times.

# == After round 10000 ==
# Monkey 0 inspected items 52166 times.
# Monkey 1 inspected items 47830 times.
# Monkey 2 inspected items 1938 times.
# Monkey 3 inspected items 52013 times.
# After 10000 rounds, the two most active monkeys inspected items 52166 and 52013 times. Multiplying these together, the level of monkey business in this situation is now 2713310158.

# Worry levels are no longer divided by three after each item is inspected; you'll need to find another way to keep your worry levels manageable. Starting again from the initial state in your puzzle input, what is the level of monkey business after 10000 rounds?


from functools import reduce
import re
from operator import mul
from typing import List

monkeys = {}
modulo = 1

with open("input.txt") as f:
    while (ln := f.readline()) != "":
        monkey = int(ln[7:-2])
        monkeys[monkey] = [
            list(map(int, re.split(", ", f.readline()[18:].strip()))),
            f.readline()[19:].strip(),
            int(f.readline()[21:].strip()),
            int(f.readline()[29:].strip()),
            int(f.readline()[30:].strip()),
            0
        ]
        f.readline()
        modulo *= monkeys[monkey][2]

for r in range(10000):
    for monkey in sorted(monkeys):
        items: List[int] = monkeys[monkey][0]
        while items:
            item = items.pop(0)
            new = eval(monkeys[monkey][1], {"old": item}) % modulo
            if new % monkeys[monkey][2] == 0:
                monkeys[monkeys[monkey][3]][0].append(new)
            else:
                monkeys[monkeys[monkey][4]][0].append(new)
            monkeys[monkey][5] += 1

print(reduce(mul, sorted([monkeys[m][5] for m in monkeys])[-2:]))
