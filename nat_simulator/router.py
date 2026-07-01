from .defs import *
from .utils import *
from .delta import Delta

class Router:
    def __init__(self, nat_type, delta):
        self.delta = delta
        self.approve_plugin = load_plugin(("nat_types", nat_type))
        self.flows = {}

    def approve(self, af, proto, mapping, dest):
        return self.approve_plugin(self, af, proto, mapping, dest)

    def connect(self, af, proto, src, dest):
        flow = FlowKey(af, proto, *src, *dest)

        # Allocate a new NAT mapping based on the unique delta algorithm.
        mapping = self.delta.allocate()

        # The NAT decides on whether inbound mappings can enter.
        # Hence, filtering by destination is convenient.
        flow_key = (af, proto, mapping)
        self.flows[flow_key] = flow

delta = Delta("independent")
r = Router("full_cone", delta)
src = ("10.0.1.50", 5000)
dest = ("8.8.8.8", 53)
r.connect(IP4, UDP, src, dest)


#print(r.flows)

# Simulate accepting a con
ret = r.approve(IP4, UDP, 1, dest)
print(ret)