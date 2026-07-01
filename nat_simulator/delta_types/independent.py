def plugin(delta, step, data):
    delta.value = delta.value + step
    return delta.value