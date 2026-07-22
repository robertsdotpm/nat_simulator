"""
1. Reuse mapping on same src ip:port.
2. No filtering: A full cone NAT lets any destination connect back providing an existing mapping exists.
"""
def plugin(router, dest, mapping_info):
    # No filtering, but a mapping still has to exist.
    return mapping_info is not None