def plugin(delta, src_port):
    if hasattr(delta, "src_port"):
        dist = abs(delta.src_port - src_port)
    else:
        dist = 0

    delta.src_port = src_port
    return delta.value + dist