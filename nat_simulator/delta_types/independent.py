"""
Independent means the NAT allocates new external ports regardless of variations
to source ports e.g. given 22, 2000, 80 -> 1, 2, 3...
"""
def plugin(delta, flow):
    delta.value = delta.value + delta.step
    return delta.value