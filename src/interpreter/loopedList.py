class LoopedList:
    h = []
    l = []

    def __init__(self, l, h=None):
        self.l = l
        self.h = h if h is not None else []

    def __str__(self):
        return str(self[0:50])

    def __getitem__(self, i):
        if isinstance(i, slice):
            return [self.__getitem__(x) for x in range(i.start if i.start else 0, i.stop if i.stop else 50, i.step if i.step else 1)]
        if isinstance(i, tuple):
            return [self.__getitem__(x) for x in i]
        if i < len(self.h):
            return self.h[i]
        i -= len(self.h)
        i %= len(self.l)
        return self.l[i]

    def __len__(self):
        return len(self.l) + len(self.h)