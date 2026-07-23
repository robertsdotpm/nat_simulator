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

        # Mapping dest list by mapping.
        # [MappingKey] -> MappingInfo
        self.mappings = {} 

        # Mapping dest list by reuse conditions.
        # [FlowKey|ClientKey] -> MappingInfo
        self.mapping_owners = {}

    def accept(self, af, proto, mapping, dest):
        mapping_key = MappingKey(af, proto, mapping)

        # None = no mapping exists; only open_internet accepts that.
        mapping_info = self.mappings.get(mapping_key)
        return self.accept_plugin(self, dest, mapping_info)
    
    def record_mapping(self, mapping_key, owner_key, mapping_info):
        self.mappings[mapping_key] = mapping_info
        self.mapping_owners[owner_key] = mapping_info

    def get_reused_mapping(self, owner_key, dest):
        if owner_key in self.mapping_owners:
            mapping_info = self.mapping_owners[owner_key]

            # Each mapping has a whitelist that it consults based on NAT type.
            # Even if reusable -- whitelist can still prevent inbound.
            mapping_info.whitelist(dest)

            # Return pre-existing mapping.
            return mapping_info.mapping
    
    def get_free_mapping(self, af, proto, src):
        base = self.delta.allocate(src.port)
        for attempt in range(0, self.delta.ring.width):
            mapping = int(base + attempt)
            mapping_key = MappingKey(af, proto, mapping)

            # Port belongs to another internal endpoint -- try the next.
            if mapping_key in self.mappings:
                continue
            
            # Return computed mapping.
            return mapping, mapping_key
        
        raise Exception("Router out of mappings.")
        
    def get_mapping(self, af, proto, src, dest):
        # Existing mapping for this endpoint (or flow) -- reuse it.
        owner_key = mapping_owner_key(self.nat_type, af, proto, src, dest)
        reused_mapping = self.get_reused_mapping(owner_key, dest)
        if reused_mapping:
            return reused_mapping

        # Otherwise allocate. The delta chooses the port -- advance it
        # once, then probe forward past any port already handed out.
        mapping, mapping_key = self.get_free_mapping(af, proto, src)

        # Record mapping info by allocation and owner.
        mapping_info = MappingInfo(src, mapping, dest)
        self.record_mapping(mapping_key, owner_key, mapping_info)
        return mapping

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