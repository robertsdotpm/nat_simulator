def load_func(source: str, name: str):
    ns = {}
    exec(source, ns)
    return ns[name]