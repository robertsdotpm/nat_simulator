from .defs import *
from .utils import *
from .delta import Delta

class Router:
    def __init__(self, nat_type, delta):
        self.approve_plugin = load_plugin(("nat_types", nat_type))
        self.delta = delta
        self.flows = {}
        self.dest_whitelist = {}

    def approve(self, af, proto, mapping, src, dest):
        flow_key = (af, proto, mapping)
        if flow_key in self.flows:
            flow = self.flows[flow_key]
        else:
            flow = None

        return self.approve_plugin(self, src, dest, flow)
    
    def get_mapping(self, flow):
        # Allocate a new NAT mapping based on the unique delta algorithm.
        # Makes sure mapping isn't already used for this router.
        mapping = 0
        for attempt in range(0, MAX_PORT):
            mapping = int(self.delta.allocate(flow) + attempt)
            flow_key = (flow.af, flow.proto, mapping)

            # Mapping already allocated, try again.
            if flow_key in self.flows:
                mapping = 0
                continue

            return mapping

        # Check for mapping success.
        if not mapping:
            raise ValueError("No mappings left for router.")

    def connect(self, af, proto, src, dest):
        flow = FlowKey(af, proto, src, dest)

        # For endpoint independent.
        self.dest_whitelist[dest.ip] = 1 # By IP
        self.dest_whitelist[dest] = 1 # By IP and port.

        # Get a non-conflicting mapping from the router.
        mapping = self.get_mapping(flow)

        # The NAT decides on whether inbound mappings can enter.
        # Hence, filtering by destination is convenient.
        flow_key = (af, proto, mapping)
        self.flows[flow_key] = flow

        # Let caller know ultimate mapping.
        return mapping

delta = Delta("dependent", 1)

r = Router("full_cone", delta)

dest = AddrKey("8.8.8.8", 53)
dest_b = AddrKey("8.8.8.8", 53)

for i in range(1, 10):
    src = AddrKey("10.0.1.50", 1024 + (3 * i))
    mapping = r.connect(IP4, UDP, src, dest)
    print(mapping)



exit(0)

#print(mapping)

#exit(0)
#print(r.flows)

# Simulate accepting a con
ret = r.approve(IP4, UDP, 1025, dest)
print(ret)