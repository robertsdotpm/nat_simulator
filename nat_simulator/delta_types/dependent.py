"""
The NAT starts off at a fixed value r. Then increases by step for every mapping,
however: only when src_port difference is preserved.
"""
def plugin(delta, flow):
    delta.value = delta.value + delta.step
    return delta.value + flow.src.port