def plugin(delta, flow):
    if hasattr(delta, "flow"):
        dist = abs(delta.flow.src.port - flow.src.port)
    else:
        dist = 0

    delta.flow = flow
    return delta.value + dist