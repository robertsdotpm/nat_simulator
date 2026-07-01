class RingInt:
    def __init__(self, start: int, stop: int, offset: int = 0):
        if stop <= start:
            raise ValueError("stop must be greater than start")

        self.start = start
        self.stop = stop
        self.width = stop - start
        self.offset = offset % self.width

    @property
    def value(self) -> int:
        return self.start + self.offset

    def __add__(self, other: int):
        return RingInt(self.start, self.stop, self.offset + other)

    def __sub__(self, other: int):
        return RingInt(self.start, self.stop, self.offset - other)

    def __iadd__(self, other: int):
        self.offset = (self.offset + other) % self.width
        return self

    def __isub__(self, other: int):
        self.offset = (self.offset - other) % self.width
        return self

    def __int__(self):
        return self.value

    def __index__(self):
        return self.value

    def __repr__(self):
        return str(self.value)