"""
NAT routers allocate across a fixed range from m - n. Usually, they skip the first
1024 since it maps to protected services. On top of that, they have different
algorithms for choosing how to do mappings. Mostly, they will do some mathematical
op on a previous mapping. But the expectation is you want to wrap around a fixed
allowed range.
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class RingInt:
    start: int
    stop: int
    value: int

    def __post_init__(self):
        width = self.stop - self.start
        if width <= 0:
            raise ValueError("stop must be greater than start")

        wrapped = self.start + ((self.value - self.start) % width)
        object.__setattr__(self, "value", wrapped)

    def __add__(self, other: int):
        return RingInt(self.value + other, self.start, self.stop)

    def __sub__(self, other: int):
        return RingInt(self.value - other, self.start, self.stop)

    def __int__(self):
        return self.value

    def __repr__(self):
        return str(self.value)
    
n = RingInt(