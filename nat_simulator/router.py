"""
End-point independent means:
reuse mapping if same internal src_ip, port, regardless of dest.
"""
from .defs import *
from .utils import *
from .delta import Delta

class Router:
    def __init__(self, wan_ip, nat_type, delta):
        self.accept_plugin = load_plugin(("nat_types", nat_type))
        self.nat_type = nat_type
        self.wan_ip = wan_ip
        self.delta = delta
        self.flows = {}
        self.mappings = {}

    def accept(self, af, proto, mapping, src, dest):
        flow_key = (af, proto, mapping)
        if flow_key in self.flows:
            flow = self.flows[flow_key]
        else:
            flow = None

        return self.accept_plugin(self, src, dest, flow)
    
    def get_mapping(self, af, proto, src, dest):
        client_key = ClientKey(af, proto, src)

        # Allocate a new NAT mapping based on the unique delta algorithm.
        # Makes sure mapping isn't already used for this router.
        mapping = 0
        for attempt in range(0, MAX_PORT):
            # A mapping for this internal address already exists.
            mapping_key = MappingKey(af, proto, mapping)

            # Pre-existing mapping is found -- see if reuse permitted.
            by_client_key = client_key in self.mappings
            by_mapping_key = mapping_key in self.mappings
            if by_client_key or by_mapping_key:
                mapping_info = self.mappings[mapping_key]

                # If a NAT is "endpoint-independent": reuse is permitted.
                if self.nat_type != "symmetric":
                    mapping_info.dests.insert(dest)
                else:
                    continue


            mapping = int(self.delta.allocate(src.port) + attempt)
            self.mappings[mapping_key]

            

            return mapping

        # Check for mapping success.
        if not mapping:
            raise ValueError("No mappings left for router.")

    def connect(self, af, proto, src, dest):
        mapping_key = MappingKey(af, proto, src)
        flow = FlowKey(af, proto, src, dest)



        # Get a non-conflicting mapping from the router.
        mapping = self.get_mapping(mapping_key, dest)

        # The NAT decides on whether inbound mappings can enter.
        # Hence, filtering by destination is convenient.
        flow_key = (af, proto, mapping)
        self.flows[flow_key] = flow

        # Let caller know ultimate mapping.
        return mapping

"""
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
"""