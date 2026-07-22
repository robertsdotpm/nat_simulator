"""
End-point independent means:
reuse mapping if same internal src_ip, port, regardless of dest.

RFC 4787 endpoint independent vs dependent

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

        # The external port space: what an inbound packet keys on.
        self.mappings = {}

        # Which mapping an outbound flow already owns.
        self.reuse = {}

    def accept(self, af, proto, mapping, dest):
        mapping_key = MappingKey(af, proto, mapping)

        # None = no mapping exists; only open_internet accepts that.
        return self.accept_plugin(self, dest, self.mappings.get(mapping_key))

    def reuse_key(self, af, proto, src, dest):
        # Symmetric NATs are "endpoint dependent": a new destination
        # gets a new mapping, so the destination is part of the key.
        if self.nat_type == "symmetric":
            return FlowKey(af, proto, src, dest)

        # Everything else is endpoint independent: one mapping per
        # internal endpoint, reused regardless of destination.
        return ClientKey(af, proto, src)

    def get_mapping(self, af, proto, src, dest):
        # Existing mapping for this endpoint (or flow) -- reuse it.
        reuse_key = self.reuse_key(af, proto, src, dest)
        if reuse_key in self.reuse:
            mapping_info = self.reuse[reuse_key]
            mapping_info.allow(dest)
            return mapping_info.mapping

        # Otherwise allocate. The delta chooses the port -- advance it
        # once, then probe forward past any port already handed out.
        base = self.delta.allocate(src.port)
        for attempt in range(0, self.delta.ring.width):
            mapping = int(base + attempt)
            mapping_key = MappingKey(af, proto, mapping)

            # Port belongs to another internal endpoint -- try the next.
            if mapping_key in self.mappings:
                continue

            # Record mapping info.
            mapping_info = MappingInfo(src, mapping)
            mapping_info.allow(dest)
            self.mappings[mapping_key] = mapping_info
            self.reuse[reuse_key] = mapping_info
            return mapping

        # Check for mapping success.
        raise ValueError("No mappings left for router.")

    def connect(self, af, proto, src, dest):
        # Get a non-conflicting mapping from the router.
        mapping = self.get_mapping(af, proto, src, dest)

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