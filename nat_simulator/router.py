import os
from .defs import *
from .utils import load_func

class Router:
    def __init__(self, nat_type):
        file_path = os.path.join("nat_types", nat_type + ".py")
        code = open(file_path, "r").read()
        self.approve_plugin = load_func(code, "approve")
        self.flows = {}

    def approve(self, af, proto, mapping, dest):
        return self.approve_plugin(self, af, proto, mapping, dest)

    def connect(self, af, proto, src, dest):
        flow = FlowKey(af, proto, *src, *dest)

        mapping = 1 # temporary

        # The NAT decides on whether inbound mappings can enter.
        # Hence, filtering by destination is convenient.
        flow_key = (af, proto, mapping)
        self.flows[flow_key] = flow


r = Router("full_cone")
src = ("10.0.1.50", 5000)
dest = ("8.8.8.8", 53)
r.connect(IP4, UDP, src, dest)


#print(r.flows)

# Simulate accepting a con
ret = r.approve(IP4, UDP, 2, dest)
print(ret)