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
    
    def get_mapping(self, flow):
        # Allocate a new NAT mapping based on the unique delta algorithm.
        # Makes sure mapping isn't already used for this router.
        mapping = None
        for attempt in range(0, MAX_PORT):
            mapping = int(self.delta.allocate(flow) + attempt)
            flow_key = (flow.af, flow.proto, mapping)

            # Mapping already allocated, try again.
            if flow_key in self.flows:
                continue

            return mapping

        # Check for mapping success.
        if mapping is None:
            raise ValueError("No mappings left for router.")

    def connect(self, af, proto, src, dest):
        flow = FlowKey(af, proto, *src, *dest)

        # Get a non-conflicting mapping from the router.
        mapping = self.get_mapping(flow)

        # The NAT decides on whether inbound mappings can enter.
        # Hence, filtering by destination is convenient.
        flow_key = (af, proto, mapping)
        self.flows[flow_key] = flow

        # Let caller know ultimate mapping.
        return mapping

delta = Delta("independent", 1)
r = Router("full_cone", delta)
src = ("10.0.1.50", 5000)
dest = ("8.8.8.8", 53)
mapping = r.connect(IP4, UDP, src, dest)

#print(mapping)

#exit(0)
#print(r.flows)

# Simulate accepting a con
ret = r.approve(IP4, UDP, 1025, dest)
print(ret)