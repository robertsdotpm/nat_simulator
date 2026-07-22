import random

def plugin(delta, src_port):
    return random.randrange(
        delta.ring.start,
        delta.ring.stop + 1
    )