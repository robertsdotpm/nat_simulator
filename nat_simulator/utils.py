import os
from pathlib import Path


def load_func(source: str, name: str):
    ns = {}
    exec(source, ns)
    return ns[name]

def load_plugin(path):
    # Add file extension to path.
    path = list(path)
    path[-1] += ".py"

    # Prepend absolute path.
    script_path = Path(__file__).resolve().parent
    path = os.path.join(script_path, *path)

    # Resolve any symbolic garbage.
    path = os.path.realpath(path)

    # Open the final code file.
    code = open(path, "r").read()
    return load_func(code, "plugin")