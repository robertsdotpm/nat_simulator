def plugin(delta, flow):
    if hasattr(delta, "flow"):
        dist = abs(delta.flow.src_port - flow.src_port)
    else:
        dist = 0

    delta.flow = flow
    return delta.value + dist