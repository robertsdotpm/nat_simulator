from .defs import *
from .utils import *

# Used by router class to do NAT mappings.
class NAT:
    def __init__(self):
        # Mapping dest list by mapping.
        # [MappingKey] -> MappingInfo
        self.mappings = {} 

        # Mapping dest list by reuse conditions.
        # [FlowKey|ClientKey] -> MappingInfo
        self.mapping_owners = {}
    
    def get_reused_mapping(self, owner_key, dest):
        if owner_key in self.mapping_owners:
            mapping_info = self.mapping_owners[owner_key]

            # Each mapping has a whitelist based on NAT type.
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
    
    def record_mapping(self, mapping_key, owner_key, dest):
        info = MappingInfo(owner_key.src, mapping_key.mapping, dest)
        self.mappings[mapping_key] = info
        self.mapping_owners[owner_key] = info
        
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
        self.record_mapping(mapping_key, owner_key, dest)
        return mapping