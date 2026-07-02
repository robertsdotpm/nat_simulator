import random

def plugin(delta, flow):
    return random.randrange(
        delta.ring.start,
        delta.ring.stop + 1
    )