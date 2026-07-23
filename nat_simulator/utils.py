import os
from pathlib import Path
from .defs import *

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

def mapping_owner_key(nat_type, af, proto, src, dest):
    # Symmetric NATs are "endpoint dependent": a new destination
    # gets a new mapping, so the destination is part of the key.
    if nat_type == "symmetric":
        return FlowKey(af, proto, src, dest)

    # Everything else is endpoint independent: one mapping per
    # internal endpoint, reused regardless of destination.
    return ClientKey(af, proto, src)