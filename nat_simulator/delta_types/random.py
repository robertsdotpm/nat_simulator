import random

def plugin(delta, flow, mapping):
    return random.randrange(
        delta.ring.start,
        delta.ring.stop + 1
    )