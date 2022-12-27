# --- Part Two ---
# Due to some kind of monkey-elephant-human mistranslation, you seem to have misunderstood a few key details about the riddle.

# First, you got the wrong job for the monkey named root; specifically, you got the wrong math operation. The correct operation for monkey root should be =, which means that it still listens for two numbers (from the same two monkeys as before), but now checks that the two numbers match.

# Second, you got the wrong monkey for the job starting with humn:. It isn't a monkey - it's you. Actually, you got the job wrong, too: you need to figure out what number you need to yell so that root's equality check passes. (The number that appears after humn: in your input is now irrelevant.)

# In the above example, the number you need to yell to pass root's equality test is 301. (This causes root to get the same number, 150, from both of its monkeys.)

# What number do you yell to pass root's equality test?


with open("input.txt") as i:
    with open("temp.py", "w") as o:
        for ln in i:
            match ln.strip().split():
                case [var, num]:
                    o.write(f"""
def {var[:-1]}(humn):
    return {num}

""")
                case ["humn:", var1, op, var2]:
                    pass
                case ["root:", var1, op, var2]:
                    o.write(f"""
def root(humn):
    return {var1}(humn) - {var2}(humn)

""")
                case [var, var1, op, var2]:
                    o.write(f"""
def {var[:-1]}(humn):
    return {var1}(humn) {op} {var2}(humn)

""")

from temp import root

left = -(1 << 63)
right = +(1 << 63)

if root(lambda x: left) > 0:
    left, right = right, left

for i in range(200):
    m = (left + right) // 2
    if root(lambda x: m) > 0:
        right = m
    else:
        left = m

print(left)
print(root(lambda x: left))
