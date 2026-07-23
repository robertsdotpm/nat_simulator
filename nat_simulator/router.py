"""
End-point independent means:
reuse mapping if same internal src_ip, port, regardless of dest.

RFC 4787 endpoint independent vs dependent

"""
from .defs import *
from .utils import *
from .delta import Delta
from .nat import NAT

# Uses NAT class to support mappings.
class Router(NAT):
    def __init__(self, wan_ip, nat_type, delta):
        self.accept_plugin = load_plugin(("nat_types", nat_type))
        self.nat_type = nat_type
        self.wan_ip = wan_ip
        self.delta = delta

    def accept(self, af, proto, mapping, dest):
        mapping_key = MappingKey(af, proto, mapping)

        # None = no mapping exists; only open_internet accepts that.
        mapping_info = self.mappings.get(mapping_key)
        return self.accept_plugin(self, dest, mapping_info)

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