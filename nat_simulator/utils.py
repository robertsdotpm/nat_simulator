import os

def load_func(source: str, name: str):
    ns = {}
    exec(source, ns)
    return ns[name]

def load_plugin(path):
    path = list(path)
    path[-1] += ".py"
    path = os.path.join(*path)
    code = open(path, "r").read()
    return load_func(code, "plugin")