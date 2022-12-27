import re


class plist(list):
    def __lt__(self, other):
        if isinstance(other, list):
            return super().__lt__(other)
        else:
            return super().__lt__(plist([other]))

    def __eq__(self, other):
        if isinstance(other, list):
            return super().__eq__(other)
        else:
            return super().__eq__(plist([other]))


class pint(int):
    def __lt__(self, other):
        if isinstance(other, int):
            return super().__lt__(other)
        else:
            return plist([self]) < other

    def __eq__(self, other):
        if isinstance(other, int):
            return super().__eq__(other)
        else:
            return plist([self]) == other


with open("input.txt") as f:
    s = f.read()
    s = s.replace("[", "plist([").replace("]", "])")
    s = re.sub(r"\d+", lambda m: f"pint({m.group()})", s)
    pairs = [x.split() for x in s.split("\n\n")]
    points = lambda i, le, r: i + 1 if eval(le) < eval(r) else 0
    print(sum([points(i, le, r) for i, (le, r) in enumerate(pairs)]))
