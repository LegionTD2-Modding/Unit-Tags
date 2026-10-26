"""Hands out tag names from a list."""


def parse(text):
    """The names in a comma-separated setting, without blanks."""
    return [n.strip() for n in str(text).split(",") if n.strip()]


class Names:
    """Which fighter carries which name. A new fighter takes the first name in the list that no
    fighter carries, and keeps it through upgrades and waves until it is sold. Without ``loop``,
    fighters placed while every name is carried get no name; with it they reuse the names in
    order. The list is passed in at each call, so edits made during a game apply at once."""

    def __init__(self):
        self.carried = {}       # unit id -> name
        self.placed = []       # unit ids in the order they took a name
        self.reused = 0

    def take(self, unit, names, loop):
        """The name of fighter ``unit``, giving it one if it has none; None when none is left."""
        if unit in self.carried:
            return self.carried[unit]
        free = [n for n in names if n not in self.carried.values()]
        if free:
            name = free[0]
        elif loop and names:
            name = names[self.reused % len(names)]
            self.reused += 1
        else:
            return None
        self.carried[unit] = name
        self.placed.append(unit)
        return name

    def release(self, unit):
        """Fighter ``unit`` was sold: its name is free again. Returns the name, or None."""
        if unit in self.placed:
            self.placed.remove(unit)
        return self.carried.pop(unit, None)

    def retag(self, units, names, loop):
        """Hands the names out again after the list or ``loop`` changed, for the fighters ``units``.

        A fighter keeps its name while the list still has it (once per name without ``loop``); the
        others take free names in the order they were placed. Returns {unit: name or None}.
        """
        order = [u for u in self.placed if u in units] + sorted(u for u in units if u not in self.placed)
        before = self.carried
        self.carried, self.placed, self.reused = {}, [], 0
        for u in order:
            name = before.get(u)
            if name in names and (loop or name not in self.carried.values()):
                self.carried[u] = name
                self.placed.append(u)
        for u in order:
            self.take(u, names, loop)
        self.placed.sort(key=order.index)
        return {u: self.carried.get(u) for u in order}
