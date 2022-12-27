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
    s = f.read().replace("\n\n", "\n") + "\n[[2]]\n[[6]]"
    s = s.replace("[", "plist([").replace("]", "])")
    s = re.sub(r"\d+", lambda m: f"pint({m.group()})", s)
    packets = [eval(x) for x in s.split("\n")]

    d1 = packets[-1]
    d2 = packets[-2]

    packets.sort()

    print((packets.index(d1) + 1) * (packets.index(d2) + 1))
