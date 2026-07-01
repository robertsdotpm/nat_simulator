def plugin(delta, flow):
    delta.value = delta.value + delta.step
    return delta.value